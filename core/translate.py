LANG_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
}

HINDI_FALLBACKS = {
    "Hello! Ask me anything about **Raji: An Ancient Epic**—such as Raji and Golu's story, weapons, elemental powers, puzzles, or gameplay.": (
        "नमस्ते! **Raji: An Ancient Epic** के बारे में कुछ भी पूछें—जैसे राजी और गोलू की कहानी, "
        "हथियार, तत्वों की शक्तियाँ, पहेलियाँ या गेमप्ले।"
    ),
    "I couldn't find reliable information about that in the **Raji: An Ancient Epic** knowledge base. Please check your phrasing or reach out via **Contact Support** in the sidebar!": (
        "**Raji: An Ancient Epic** के नॉलेज बेस में मुझे इसकी विश्वसनीय जानकारी नहीं मिली। "
        "कृपया अपना प्रश्न बदलकर देखें या साइडबार में **Contact Support** से संपर्क करें!"
    ),
}


def to_english(text: str, source_lang: str) -> str:
    if not text or not isinstance(text, str) or not text.strip():
        return text or ""
    return text.strip()


def from_english(text: str, target_lang: str) -> str:
    if not text or not isinstance(text, str) or not text.strip():
        return text or ""
    cleaned = text.strip()
    if target_lang == "Hindi":
        return HINDI_FALLBACKS.get(cleaned, cleaned)
    return cleaned
