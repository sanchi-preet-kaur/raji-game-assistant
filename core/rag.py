import os
import pickle
import re
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
from docx import Document

KB_DIR = os.path.join("data", "knowledge_base")
UPLOADS_DIR = os.path.join("data", "uploads")
STORE_DIR = os.path.join("data", "store")
INDEX_FILE = os.path.join(STORE_DIR, "tfidf_index.pkl")


def extract_text_from_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif ext == ".pdf":
        reader = PdfReader(filepath)
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == ".docx":
        doc = Document(filepath)
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return ""


def chunk_text(text: str, source: str, chunk_size: int = 450, overlap: int = 60) -> List[dict]:
    # Split cleanly on blank lines first (preserves Q&A blocks)
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    chunks = []
    for block in blocks:
        if len(block) <= chunk_size:
            chunks.append({"text": block, "source": source})
        else:
            start = 0
            while start < len(block):
                end = start + chunk_size
                chunks.append({"text": block[start:end].strip(), "source": source})
                start += chunk_size - overlap
    return chunks


def rebuild_index() -> int:
    os.makedirs(KB_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    os.makedirs(STORE_DIR, exist_ok=True)

    all_chunks = []
    for folder in (KB_DIR, UPLOADS_DIR):
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            if os.path.isfile(fpath):
                raw_text = extract_text_from_file(fpath)
                all_chunks.extend(chunk_text(raw_text, source=fname))

    if not all_chunks:
        all_chunks = [{"text": "Raji: An Ancient Epic is an action-adventure game set in ancient India.", "source": "default"}]

    corpus = [c["text"] for c in all_chunks]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(corpus)

    with open(INDEX_FILE, "wb") as f:
        pickle.dump({"vectorizer": vectorizer, "matrix": matrix, "chunks": all_chunks}, f)

    return len(all_chunks)


def _load_index():
    if not os.path.exists(INDEX_FILE):
        rebuild_index()
    with open(INDEX_FILE, "rb") as f:
        return pickle.load(f)


def search_chunks(query: str, top_k: int = 3) -> List[Tuple[dict, float]]:
    if not query.strip():
        return []
    data = _load_index()
    q_vec = data["vectorizer"].transform([query])
    sims = cosine_similarity(q_vec, data["matrix"]).flatten()
    ranked_indices = sims.argsort()[::-1][:top_k]
    return [(data["chunks"][i], float(sims[i])) for i in ranked_indices if sims[i] > 0]


def answer_question(query: str, threshold: float = 0.14) -> Tuple[str, float, str]:
    results = search_chunks(query, top_k=1)
    if not results or results[0][1] < threshold:
        fallback = (
            "I couldn't find reliable information about that in the **Raji: An Ancient Epic** "
            "knowledge base. Please check your phrasing or reach out via **Contact Support** in the sidebar!"
        )
        return fallback, (results[0][1] if results else 0.0), "None"

    best_chunk, score = results[0]
    text = best_chunk["text"]
    # Format Q:/A: blocks cleanly if present
    if "\nA:" in text:
        text = text.split("\nA:", 1)[1].strip()
    return text, score, best_chunk["source"]