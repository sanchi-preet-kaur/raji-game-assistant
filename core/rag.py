from functools import lru_cache
import os
import pickle
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv(override=True)


class RajiRetriever:
    """Raji: An Ancient Epic assistant combining TF-IDF retrieval with Groq LLM."""

    def __init__(
        self,
        kb_dir: str = "data/knowledge_base",
        store_dir: str = "data/store",
        threshold: float = 0.08,
        model_name: Optional[str] = None,
    ):
        self.kb_dir = Path(kb_dir)
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.store_dir / "tfidf_index.pkl"
        self.threshold = threshold
        self.model_name = model_name
        self.last_api_error: Optional[str] = None
        self._resolved_model: Optional[str] = model_name

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=8000,
        )
        self.chunks: List[Dict[str, str]] = []
        self.tfidf_matrix = None

        if not self.load_index():
            self.rebuild_index()

    def _get_client(self) -> Optional[Groq]:
        load_dotenv(override=True)
        api_key = os.getenv("GROQ_API_KEY", "").strip().strip('"').strip("'")
        if not api_key:
            try:
                import streamlit as st
                api_key = str(st.secrets.get("GROQ_API_KEY", "")).strip()
            except Exception:
                api_key = ""
        return Groq(api_key=api_key) if api_key else None

    def _get_candidate_models(self, client: Groq) -> List[str]:
        """Discover available chat models from Groq API with reliable fallbacks."""
        candidates: List[str] = []

        if self._resolved_model:
            candidates.append(self._resolved_model)
        if self.model_name and self.model_name not in candidates:
            candidates.append(self.model_name)

        try:
            models_resp = client.models.list()
            skip_prefixes = ("whisper", "orpheus", "prompt-guard", "safeguard")
            for m in getattr(models_resp, "data", []):
                mid = getattr(m, "id", "") or ""
                if not mid or mid in candidates:
                    continue
                if any(tag in mid.lower() for tag in skip_prefixes):
                    continue
                candidates.append(mid)
        except Exception:
            pass

        for fallback_id in [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
            "qwen/qwen3.8-27b",
            "llama-3.1-8b-instant",
        ]:
            if fallback_id not in candidates:
                candidates.append(fallback_id)

        return candidates

    @staticmethod
    def clean_text(text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _chunk_text(
        self, text: str, source_name: str, chunk_size: int = 550, overlap: int = 80
    ) -> List[Dict[str, str]]:
        cleaned = self.clean_text(text)
        if not cleaned:
            return []

        paragraphs = [p.strip() for p in cleaned.split("\n\n") if p.strip()]
        chunks: List[Dict[str, str]] = []
        current = ""

        for para in paragraphs:
            if len(current) + len(para) + 2 <= chunk_size:
                current = f"{current}\n\n{para}".strip()
            else:
                if current and len(current) >= 60:
                    chunks.append({"source": source_name, "text": current})
                    current = ""
                if len(para) > chunk_size:
                    step = max(1, chunk_size - overlap)
                    for start in range(0, len(para), step):
                        piece = para[start : start + chunk_size].strip()
                        if len(piece) >= 60:
                            chunks.append({"source": source_name, "text": piece})
                    current = ""
                else:
                    current = f"{current}\n\n{para}".strip() if current else para

        if current and len(current) >= 40:
            chunks.append({"source": source_name, "text": current})

        return chunks

    def _read_knowledge_files(self) -> List[Dict[str, str]]:
        all_chunks: List[Dict[str, str]] = []
        if not self.kb_dir.exists():
            return all_chunks

        for root, _, files in os.walk(self.kb_dir):
            for fname in sorted(files):
                fpath = Path(root) / fname
                if fpath.suffix.lower() in {".txt", ".md"}:
                    try:
                        content = fpath.read_text(encoding="utf-8", errors="ignore")
                        all_chunks.extend(self._chunk_text(content, fname))
                    except Exception:
                        continue
        return all_chunks

    def rebuild_index(self) -> int:
        self.chunks = self._read_knowledge_files()
        if not self.chunks:
            self.tfidf_matrix = None
            return 0

        corpus = [item["text"] for item in self.chunks]
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

        with open(self.index_path, "wb") as f:
            pickle.dump(
                {
                    "vectorizer": self.vectorizer,
                    "chunks": self.chunks,
                    "matrix": self.tfidf_matrix,
                },
                f,
            )
        return len(self.chunks)

    def load_index(self) -> bool:
        if not self.index_path.exists():
            return False
        try:
            with open(self.index_path, "rb") as f:
                payload = pickle.load(f)
            self.vectorizer = payload["vectorizer"]
            self.chunks = payload["chunks"]
            self.tfidf_matrix = payload["matrix"]
            return bool(self.chunks) and self.tfidf_matrix is not None
        except Exception:
            return False

    def _generate_llm_reply(
        self,
        query: str,
        context: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Optional[str]:
        client = self._get_client()
        if not client:
            self.last_api_error = "GROQ_API_KEY not found in .env or Streamlit secrets."
            return None

        system_prompt = (
            "You are the official AI Game & Player Support Assistant strictly for 'Raji: An Ancient Epic' "
            "(developed by Nodding Heads Games).\n"
            "Rules:\n"
            "1. Answer ONLY questions related to 'Raji: An Ancient Epic'—its story, lore, characters "
            "(Raji, Golu, Durga, Vishnu, Shiva, Mahabalasura), divine weapons (Trishul, Sharanga Bow, "
            "Sword & Shield, Chakra), elemental favors, combat, mandala puzzles, and game support.\n"
            "2. If a user asks about a character or thing that does NOT exist in 'Raji: An Ancient Epic' "
            "(for example, a custom name like 'Sanchi'), clearly state that they are not a character in the game "
            "and list the actual main characters (Raji, Golu, Mahabalasura, Durga, Vishnu).\n"
            "3. If a user asks about something completely unrelated to 'Raji: An Ancient Epic', politely decline "
            "and invite them to ask about the game.\n"
            "4. Understand typos or Hinglish queries (like 'raji game kya h' or 'logi game') as questions about "
            "'Raji: An Ancient Epic', and always reply in clear English (the app handles translation).\n"
            "5. Use the Knowledge Base Context first, supplemented by accurate game facts. Keep answers clear and concise."
        )

        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

        if chat_history:
            for msg in chat_history[-6:]:
                role = msg.get("role")
                content = msg.get("content", "").strip()
                if role in {"user", "assistant"} and content:
                    messages.append({"role": role, "content": content})

        messages.append(
            {
                "role": "user",
                "content": f"Knowledge Base Context:\n{context}\n\nPlayer Question: {query}",
            }
        )

        for model in self._get_candidate_models(client):
            try:
                completion = client.chat.completions.create(
                    model=model,
                    temperature=0.35,
                    max_tokens=500,
                    messages=messages,
                )
                self._resolved_model = model
                self.last_api_error = None
                text = (completion.choices[0].message.content or "").strip()
                if text:
                    return text
            except Exception as exc:
                self.last_api_error = f"[{model}] {exc}"
                continue

        return None

    def search(
        self,
        query: str,
        top_k: int = 3,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        cleaned_query = self.clean_text(query)
        if not cleaned_query:
            return {
                "matched": False,
                "confidence": 0.0,
                "answer": "Please enter a question about Raji: An Ancient Epic.",
                "matches": [],
            }

        matches = []
        best_score = 0.0

        if self.tfidf_matrix is not None and self.chunks:
            query_vec = self.vectorizer.transform([cleaned_query])
            scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]

            for idx in top_indices:
                score = float(scores[idx])
                matches.append(
                    {
                        "source": self.chunks[idx]["source"],
                        "text": self.chunks[idx]["text"],
                        "score": round(score, 4),
                        "confidence_pct": round(min(100.0, score * 100.0), 1),
                    }
                )
            best_score = matches[0]["score"] if matches else 0.0

        relevant_chunks = [m["text"] for m in matches if m["score"] > 0.01]
        context_text = (
            "\n\n".join(relevant_chunks)
            if relevant_chunks
            else "No specific local snippet matched; answer using verified Raji: An Ancient Epic knowledge."
        )

        llm_answer = self._generate_llm_reply(
            cleaned_query, context_text, chat_history=chat_history
        )

        if llm_answer:
            confidence = max(matches[0]["confidence_pct"], 85.0) if matches else 88.0
            return {
                "matched": True,
                "confidence": confidence,
                "answer": llm_answer,
                "matches": matches,
            }

        if best_score >= self.threshold and matches:
            return {
                "matched": True,
                "confidence": matches[0]["confidence_pct"],
                "answer": matches[0]["text"],
                "matches": matches,
            }

        err_hint = f"\n\n*(API debug: `{self.last_api_error}`)*" if self.last_api_error else ""
        return {
            "matched": False,
            "confidence": matches[0]["confidence_pct"] if matches else 0.0,
            "answer": (
                "I couldn't find an exact offline match and the AI model is currently unavailable. "
                f"Please check your `GROQ_API_KEY` or reach out via **Contact Support**.{err_hint}"
            ),
            "matches": matches,
        }


@lru_cache(maxsize=1)
def get_retriever() -> RajiRetriever:
    return RajiRetriever()


def _load_index() -> RajiRetriever:
    retriever = get_retriever()
    if retriever.tfidf_matrix is None or not retriever.chunks:
        retriever.rebuild_index()
    return retriever


def rebuild_knowledge_index() -> int:
    get_retriever.cache_clear()
    retriever = get_retriever()
    return retriever.rebuild_index()


def answer_question(
    question: str,
    top_k: int = 3,
    chat_history: Optional[List[Dict[str, str]]] = None,
) -> tuple[str, float, list[dict]]:
    retriever = get_retriever()
    result = retriever.search(question, top_k=top_k, chat_history=chat_history)
    answer = result.get("answer", "")
    matches = result.get("matches", [])
    best_score = (
        float(matches[0]["score"])
        if matches
        else float(result.get("confidence", 0.0)) / 100.0
    )
    return answer, best_score, matches
KB_DIR = Path("data/knowledge_base")
UPLOADS_DIR = Path("data/uploads")
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def rebuild_index() -> int:
    """Compatibility wrapper expected by pages/2_Knowledge_Base.py."""
    return rebuild_knowledge_index()


def search_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Retrieve matching knowledge base chunks for pages/3_Semantic_Search.py."""
    retriever = _load_index()
    cleaned = retriever.clean_text(query)
    if not cleaned or retriever.tfidf_matrix is None or not retriever.chunks:
        return []

    query_vec = retriever.vectorizer.transform([cleaned])
    scores = cosine_similarity(query_vec, retriever.tfidf_matrix).flatten()
    top_indices = np.argsort(scores)[::-1][:top_k]

    results: List[Dict[str, Any]] = []
    for idx in top_indices:
        score = float(scores[idx])
        results.append(
            {
                "source": retriever.chunks[idx]["source"],
                "text": retriever.chunks[idx]["text"],
                "score": round(score, 4),
                "confidence_pct": round(min(100.0, score * 100.0), 1),
            }
        )
    return results
