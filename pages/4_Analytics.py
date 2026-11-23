from collections import Counter
import streamlit as st
from core.sidebar import render_sidebar
from core.auth import is_admin
from core.storage import get_logs, get_tickets

st.set_page_config(page_title="Analytics | Raji Assistant", page_icon="📈", layout="wide")
render_sidebar()

st.title("📈 Chat & Support Analytics")

if not is_admin():
    st.warning("🔒 Admin access required. Please log in via the sidebar (`admin` / `admin123`).")
    st.stop()

logs = get_logs()
tickets = get_tickets()

total_chats = len(logs)
avg_time = sum(l["response_time"] for l in logs) / total_chats if total_chats else 0.0
rated = [l for l in logs if l["feedback"] in ("up", "down")]
positive = sum(1 for l in rated if l["feedback"] == "up")
satisfaction = (positive / len(rated) * 100) if rated else 100.0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Chats", total_chats)
m2.metric("Avg Response Time", f"{avg_time:.3f}s")
m3.metric("Satisfaction Rate", f"{satisfaction:.1f}%", f"{len(rated)} ratings")
m4.metric("Support Tickets", len(tickets))

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("🔥 Top Asked Questions")
    if logs:
        counts = Counter(l["question"].strip() for l in logs).most_common(5)
        for q, count in counts:
            st.write(f"• **{q}** ({count}x)")
    else:
        st.caption("No chat interactions logged yet.")

with col2:
    st.subheader("📧 Recent Support Tickets")
    if tickets:
        for t in reversed(tickets[-5:]):
            st.markdown(f"**{t['id']}** ({t['category']}) — *{t['name']}*: {t['message']}")
    else:
        st.caption("No support tickets submitted yet.")