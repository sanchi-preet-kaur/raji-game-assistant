import html
import streamlit as st
from core.sidebar import render_sidebar
from core.rag import search_chunks

st.set_page_config(
    page_title="Semantic Search | Raji Assistant",
    page_icon="🔍",
    layout="wide",
)
render_sidebar()

st.title("🔍 Semantic Knowledge Search")
st.markdown(
    "Search directly across all **Raji: An Ancient Epic** knowledge chunks using TF-IDF cosine similarity."
)

query = st.text_input(
    "Search keywords or concepts (e.g., 'Trishul', 'Mandala puzzle', 'Mahabalasura')"
)
top_k = st.slider("Number of results", min_value=1, max_value=10, value=3)

if query:
    results = search_chunks(query, top_k=top_k)
    if not results:
        st.info("No matching chunks found.")
    else:
        for rank, item in enumerate(results, start=1):
            if isinstance(item, (tuple, list)):
                chunk = item[0] if len(item) > 0 and isinstance(item[0], dict) else {}
                score = float(item[1]) if len(item) > 1 and item[1] is not None else float(chunk.get("score", 0.0))
            elif isinstance(item, dict):
                chunk = item
                score = float(chunk.get("score", 0.0))
            else:
                chunk = {"source": "knowledge_base", "text": str(item)}
                score = 0.0

            source = html.escape(str(chunk.get("source") or "knowledge_base"))
            raw_text = chunk.get("text") or chunk.get("content") or ""
            safe_text = html.escape(str(raw_text)).replace("\n", "<br>")

            st.markdown(
                f"""
                <div class="raji-card">
                    <strong>#{rank} — Source:</strong> <code>{source}</code>
                    &nbsp;|&nbsp; <strong>Similarity Score:</strong> <code>{score:.4f}</code>
                    <p style="margin-top:0.5rem;">{safe_text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )