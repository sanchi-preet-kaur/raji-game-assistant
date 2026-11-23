import io
import speech_recognition as sr
from gtts import gTTS

TTS_LANG = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
}


def transcribe_audio(audio_bytes: bytes, language: str = "English") -> str:
    recognizer = sr.Recognizer()
    lang_map = {"English": "en-IN", "Hindi": "hi-IN", "Bengali": "bn-IN"}
    try:
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data, language=lang_map.get(language, "en-IN"))
    except Exception:
        return ""


def text_to_speech(text: str, language: str = "English") -> bytes | None:
    try:
        clean_text = text.replace("**", "").replace("#", "")
        tts = gTTS(text=clean_text, lang=TTS_LANG.get(language, "en"))
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None