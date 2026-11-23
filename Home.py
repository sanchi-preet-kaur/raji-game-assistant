import os
import streamlit as st
from core.sidebar import render_sidebar
from core.rag import _load_index

st.set_page_config(page_title="Raji — Game Assistant", page_icon="🗡️", layout="wide")
render_sidebar()
_load_index()  # Ensure seed knowledge base is indexed on first boot

col1, col2 = st.columns([1, 3])
with col1:
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)
    else:
        st.markdown("# 🗡️🪷")

with col2:
    st.title("Raji: An Ancient Epic — Game Assistant")
    st.markdown(
        "Welcome, traveler! Ask anything about **Raji's divine weapons, Hindu mythology lore, "
        "boss battles, mandala puzzles, and gameplay mechanics**—powered by a fast local RAG engine."
    )
    if st.button("💬 Start Chat", type="primary"):
        st.switch_page("pages/1_Chat.py")

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="raji-card"><h4>⚔️ Lore & Combat</h4><p>Explore the Trishul, Sharanga Bow, Chakra, and elemental favor trees.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="raji-card"><h4>🌐 Multilingual & Voice</h4><p>Chat in English, Hindi, or Bengali with optional speech input and audio replies.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="raji-card"><h4>📚 Zero-API RAG Engine</h4><p>Instant TF-IDF semantic retrieval with Admin document ingestion.</p></div>', unsafe_allow_html=True)