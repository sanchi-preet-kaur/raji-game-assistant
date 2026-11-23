import os
import streamlit as st
from core.sidebar import render_sidebar
from core.auth import is_admin
from core.rag import UPLOADS_DIR, KB_DIR, rebuild_index

st.set_page_config(page_title="Knowledge Base | Raji Assistant", page_icon="📁", layout="wide")
render_sidebar()

st.title("📁 Knowledge Base Management")

if not is_admin():
    st.warning("🔒 Admin access required. Please log in via the sidebar (`admin` / `admin123`).")
    st.stop()

st.markdown("Upload **Raji: An Ancient Epic** guides, lore sheets, or walkthroughs (`.pdf`, `.docx`, `.txt`).")

uploaded_files = st.file_uploader(
    "Upload Game Documents", type=["pdf", "docx", "txt"], accept_multiple_files=True
)

if uploaded_files and st.button("📥 Save & Re-Index Knowledge Base", type="primary"):
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    for uf in uploaded_files:
        save_path = os.path.join(UPLOADS_DIR, uf.name)
        with open(save_path, "wb") as f:
            f.write(uf.getbuffer())
    total_chunks = rebuild_index()
    st.success(f"Uploaded {len(uploaded_files)} file(s) and indexed **{total_chunks}** total chunks!")

st.divider()
st.subheader("📚 Currently Indexed Documents")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Seed Knowledge Base (`data/knowledge_base/`)**")
    for f in os.listdir(KB_DIR):
        st.write(f"• `{f}`")

with col2:
    st.markdown("**Admin Uploads (`data/uploads/`)**")
    uploads = os.listdir(UPLOADS_DIR) if os.path.exists(UPLOADS_DIR) else []
    if uploads:
        for f in uploads:
            c_name, c_del = st.columns([4, 1])
            c_name.write(f"• `{f}`")
            if c_del.button("🗑️", key=f"del_{f}"):
                os.remove(os.path.join(UPLOADS_DIR, f))
                rebuild_index()
                st.rerun()
    else:
        st.caption("No custom documents uploaded yet.")