import streamlit as st

ADMIN_CREDENTIALS = {
    "admin": "admin123"
}


def init_auth():
    if "role" not in st.session_state:
        st.session_state["role"] = "Customer"
    if "username" not in st.session_state:
        st.session_state["username"] = "Guest"


def login(username: str, password: str) -> bool:
    if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
        st.session_state["role"] = "Admin"
        st.session_state["username"] = username
        return True
    return False


def logout():
    st.session_state["role"] = "Customer"
    st.session_state["username"] = "Guest"


def is_admin() -> bool:
    init_auth()
    return st.session_state.get("role") == "Admin"