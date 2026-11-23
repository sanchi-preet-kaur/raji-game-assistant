import streamlit as st


def apply_theme():
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = True

    if st.session_state["dark_mode"]:
        css = """
        <style>
        .stApp { background-color: #0e1117; color: #f0f2f6; }
        section[data-testid="stSidebar"] { background-color: #161b22; }
        .raji-card {
            background: #1c2128; border: 1px solid #30363d;
            border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;
        }
        </style>
        """
    else:
        css = """
        <style>
        .stApp { background-color: #faf7f2; color: #1f2328; }
        section[data-testid="stSidebar"] { background-color: #f0ebe1; }
        .raji-card {
            background: #ffffff; border: 1px solid #dfd7c8;
            border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)