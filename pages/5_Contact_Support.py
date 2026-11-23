import streamlit as st
from core.sidebar import render_sidebar
from core.storage import save_ticket

st.set_page_config(page_title="Contact Support | Raji Assistant", page_icon="📧", layout="wide")
render_sidebar()

st.title("📧 Contact Game Support")
st.markdown("Didn't find the answer you needed about **Raji: An Ancient Epic**? Submit a ticket below.")

with st.form("support_form", clear_on_submit=True):
    name = st.text_input("Your Name")
    email = st.text_input("Email Address")
    category = st.selectbox(
        "Topic",
        ["Gameplay / Puzzle Help", "Lore / Story Question", "Missing Knowledge Base Info", "Bug Report"],
    )
    message = st.text_area("Describe your question or issue")
    submitted = st.form_submit_button("Submit Ticket", type="primary")

    if submitted:
        if not name.strip() or not email.strip() or not message.strip():
            st.error("Please fill in your name, email, and message.")
        else:
            save_ticket(name.strip(), email.strip(), category, message.strip())
            st.success("✅ Your ticket has been submitted! Our team will review and update the knowledge base.")