import streamlit as st
from core.auth import init_auth, login, logout, is_admin
from core.theme import apply_theme


def render_sidebar():
    init_auth()
    apply_theme()

    with st.sidebar:
        st.markdown("## 🗡️ Raji Assistant")
        st.caption(f"Role: **{st.session_state['role']}** ({st.session_state['username']})")

        # Language Selector
        if "language" not in st.session_state:
            st.session_state["language"] = "English"
        st.session_state["language"] = st.selectbox(
            "🌐 Reply Language",
            ["English", "Hindi", "Bengali"],
            index=["English", "Hindi", "Bengali"].index(st.session_state["language"]),
        )

        # Voice Toggle
        if "tts_enabled" not in st.session_state:
            st.session_state["tts_enabled"] = False
        st.session_state["tts_enabled"] = st.toggle(
            "🔊 Voice Reply (TTS)", value=st.session_state["tts_enabled"]
        )

        # Theme Toggle
        st.session_state["dark_mode"] = st.toggle(
            "🌙 Dark Mode", value=st.session_state.get("dark_mode", True)
        )

        st.divider()

        # Login / Logout Section
        if is_admin():
            st.success("Logged in as Admin")
            if st.button("Logout", use_container_width=True):
                logout()
                st.rerun()
        else:
            with st.expander("🔒 Admin Login"):
                user = st.text_input("Username", key="login_user")
                pwd = st.text_input("Password", type="password", key="login_pwd")
                if st.button("Login", use_container_width=True):
                    if login(user, pwd):
                        st.rerun()
                    else:
                        st.error("Invalid credentials")