import streamlit as st
from core.sidebar import render_sidebar
from core.rag import search_chunks

st.set_page_config(page_title="Semantic Search | Raji Assistant", page_icon="🔍", layout="wide")
render_sidebar()

st.title("🔍 Semantic Knowledge Search")
st.markdown("Search directly across all **Raji: An Ancient Epic** knowledge chunks using TF-IDF cosine similarity.")

query = st.text_input("Search keywords or concepts (e.g., 'Trishul', 'Mandala puzzle', 'Mahabalasura')")
top_k = st.slider("Number of results", min_value=1, max_value=10, value=3)

if query:
    results = search_chunks(query, top_k=top_k)
    if not results:
        st.info("No matching chunks found.")
    else:
        for rank, (chunk, score) in enumerate(results, start=1):
            st.markdown(
                f"""
                <div class="raji-card">
                    <strong>#{rank} — Source:</strong> <code>{chunk['source']}</code>
                    &nbsp;|&nbsp; <strong>Similarity Score:</strong> <code>{score:.3f}</code>
                    <p style="margin-top:0.5rem;">{chunk['text']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )