import time
import streamlit as st
from core.sidebar import render_sidebar
from core.rag import answer_question
from core.translate import to_english, from_english
from core.voice import transcribe_audio, text_to_speech
from core.storage import log_interaction, record_feedback

st.set_page_config(page_title="Chat | Raji Assistant", page_icon="💬", layout="wide")
render_sidebar()

st.title("💬 Raji Game Assistant")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

col_clear, col_voice = st.columns([1, 3])
with col_clear:
    if st.button("🗑️ Clear Chat"):
        st.session_state["messages"] = []
        st.rerun()

with col_voice:
    audio_file = st.audio_input("🎤 Ask via Voice (optional)")

# Display chat history
for idx, msg in enumerate(st.session_state["messages"]):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if msg.get("audio"):
                st.audio(msg["audio"], format="audio/mp3")
            if msg.get("log_id"):
                fb_col1, fb_col2, _ = st.columns([1, 1, 10])
                if fb_col1.button("👍", key=f"up_{idx}"):
                    record_feedback(msg["log_id"], "up")
                    st.toast("Thanks for the positive feedback!")
                if fb_col2.button("👎", key=f"down_{idx}"):
                    record_feedback(msg["log_id"], "down")
                    st.toast("Feedback recorded.")

# Determine prompt source (text or voice)
prompt = st.chat_input("Ask a question about Raji: An Ancient Epic...")
if audio_file is not None and not prompt:
    voice_key = f"processed_{audio_file.name}_{audio_file.size}"
    if not st.session_state.get(voice_key):
        st.session_state[voice_key] = True
        transcribed = transcribe_audio(audio_file.read(), st.session_state["language"])
        if transcribed:
            prompt = transcribed
        else:
            st.warning("Could not transcribe audio. Check your internet connection or try typing.")

if prompt:
    lang = st.session_state["language"]
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    start_time = time.time()
    english_query = to_english(prompt, lang)
    english_answer, score, source = answer_question(english_query)
    final_answer = from_english(english_answer, lang)
    elapsed = time.time() - start_time

    log_id = log_interaction(prompt, final_answer, score, elapsed, lang)

    audio_bytes = None
    if st.session_state.get("tts_enabled"):
        audio_bytes = text_to_speech(final_answer, lang)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": final_answer,
        "log_id": log_id,
        "audio": audio_bytes,
    })
    st.rerun()