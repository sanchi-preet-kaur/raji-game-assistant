# 🗡️ Raji — AI Game & Support Assistant

<p align="center">
  An intelligent, multilingual game knowledge and player support assistant for
  <b>Raji: An Ancient Epic</b>.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit" />
  <img src="https://img.shields.io/badge/NLP-TF--IDF-orange" />
  <img src="https://img.shields.io/badge/LLM-Groq-purple" />
  <img src="https://img.shields.io/badge/Architecture-RAG-success" />
</p>

---

## 📌 Overview

**Raji — AI Game & Support Assistant** is an interactive, multi-page chatbot and player support application developed for the action-adventure video game *Raji: An Ancient Epic* by Nodding Heads Games.

The application helps players explore game lore, characters, weapons, powers, puzzles, and gameplay-related information through a conversational interface.

Built using Python and Streamlit, the system combines local Natural Language Processing (NLP) and information retrieval techniques with Groq-powered Large Language Model (LLM) generation.

It uses **TF-IDF vectorization and cosine similarity** to retrieve relevant information from a curated knowledge base. The retrieved context is then used to generate domain-focused responses through the Groq API.

An offline-friendly retrieval fallback helps maintain basic question-answering functionality when the external LLM service is unavailable.

## ✨ Key Features

| Feature | Description |
|---|---|
| 💬 AI Chat Assistant | Conversational answers to game-related questions |
| 🧠 RAG Pipeline | Combines knowledge retrieval with Groq LLM generation |
| 🔎 Semantic Knowledge Search | TF-IDF and cosine similarity-based retrieval |
| 📚 Knowledge Management | Upload TXT, PDF, and DOCX documents |
| 🔐 Role-Based Access | Guest/customer and administrator access |
| 🌐 Multilingual Support | Translation and multilingual reply functionality |
| 🎨 Theme Customization | Dark and light themes |
| 📊 Admin Analytics | Monitor queries, response performance, and usage |
| 🎤 Voice Features | Optional speech input and text-to-speech functionality |
| 🎫 Support System | Submit and manage player support tickets |
| 📴 Local Fallback | Retrieval-based responses when Groq generation is unavailable |

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application and navigation |
| Scikit-learn | NLP and information retrieval |
| TF-IDF | Text vectorization |
| Cosine Similarity | Knowledge relevance scoring |
| Groq API | LLM-powered response generation |
| Deep Translator | Multilingual text translation |
| PyPDF | PDF text extraction |
| Python-docx | DOCX document processing |
| JSON | Local data storage |
| Pickle | Retrieval index serialization |
| HTML & CSS | Interface customization |
| SpeechRecognition | Optional voice input |
| gTTS | Optional text-to-speech generation |

## 🧠 System Architecture

The application follows a retrieval-augmented question-answering workflow.

1. The user submits a game-related question.
2. The system preprocesses the query.
3. TF-IDF converts the query into a numerical representation.
4. Cosine similarity compares the query with indexed knowledge chunks.
5. The most relevant chunks are retrieved from the knowledge base.
6. A similarity threshold helps determine whether relevant context is available.
7. Retrieved context is passed to the Groq LLM with game-specific instructions.
8. The generated response is displayed to the user.
9. If Groq is unavailable or no suitable result is found, the application uses its configured fallback response.

### Architecture Diagram

```text
                 USER
                   |
                   v
          STREAMLIT INTERFACE
                   |
                   v
            QUERY PROCESSING
                   |
                   v
            TF-IDF VECTORIZER
                   |
                   v
           COSINE SIMILARITY
                   |
                   v
          KNOWLEDGE RETRIEVAL
                   |
                   v
          RELEVANCE EVALUATION
                   |
             +-----+-----+
             |           |
          Relevant    No Match
             |           |
             v           v
       RETRIEVED       FALLBACK
        CONTEXT       RESPONSE
             |
             v
         GROQ LLM API
             |
             v
      GENERATED RESPONSE
             |
             v
          USER OUTPUT
```

## 📂 Project Structure

```text
raji-game-assistant/
│
├── Home.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── assets/
│
├── core/
│   ├── auth.py
│   ├── rag.py
│   ├── sidebar.py
│   ├── storage.py
│   ├── theme.py
│   ├── translate.py
│   └── voice.py
│
├── data/
│   ├── knowledge_base/
│   ├── uploads/
│   └── store/
│
└── pages/
    ├── 1_Chat.py
    ├── 2_Knowledge_Base.py
    ├── 3_Semantic_Search.py
    ├── 4_Analytics.py
    └── 5_Contact_Support.py
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- VS Code (recommended)
- Groq API key for LLM-powered responses

### 1. Clone the repository

```bash
git clone https://github.com/sanchi-preet-kaur/raji-game-assistant.git
```

### 2. Navigate to the project directory

```bash
cd raji-game-assistant
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Groq API key

Create a `.streamlit` folder in the project directory if it does not already exist.

Inside it, create a file named `secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Replace the placeholder with your own Groq API key.

**Security note:** Never upload your API key or `secrets.toml` file to GitHub. Keep it excluded through `.gitignore`.

If your application uses a different configuration method, follow the corresponding setup in your source code.

### 7. Run the application

```bash
streamlit run Home.py
```

### 8. Open in your browser

```text
http://localhost:8501
```

## 📸 Application Screenshots

Add screenshots of your actual running application to showcase its interface and functionality.

| Home Page | Chat Interface |
|---|---|
| Add home page screenshot | Add chat screenshot |

| Semantic Search | Analytics Dashboard |
|---|---|
| Add semantic search screenshot | Add analytics screenshot |

| Knowledge Base | Support Page |
|---|---|
| Add knowledge base screenshot | Add support screenshot |

## 🔍 Core Application Modules

| Module | Responsibility |
|---|---|
| `Home.py` | Main entry point and application navigation |
| `core/rag.py` | TF-IDF indexing, retrieval, Groq integration, and fallback handling |
| `core/auth.py` | User authentication and role management |
| `core/sidebar.py` | Shared navigation and application settings |
| `core/storage.py` | Local data persistence |
| `core/theme.py` | Dark and light theme customization |
| `core/translate.py` | Translation and multilingual functionality |
| `core/voice.py` | Optional speech and audio functionality |

## 🎯 Project Objectives

- Develop an intelligent game-specific knowledge assistant.
- Apply NLP and information retrieval techniques to gaming-related questions.
- Integrate a Large Language Model for contextual response generation.
- Ground generated responses in a curated knowledge base.
- Support administrator-managed knowledge documents.
- Provide multilingual and voice accessibility features.
- Build an interactive dashboard for monitoring application usage.
- Implement an offline-friendly fallback mechanism.

## ⚠️ Limitations

- Response quality depends on the quality and coverage of the knowledge base.
- TF-IDF is based on lexical similarity and may not understand every semantic relationship.
- Groq-powered generation requires an internet connection and a valid API key.
- Local fallback responses may be less conversational than LLM-generated responses.
- Translation and some voice features may require internet access.
- Retrieval performance depends on document quality, preprocessing, and similarity thresholds.
- Analytics are based on the application's locally stored usage data.

## 🚀 Future Enhancements

- Integration with local LLMs using Ollama.
- Dense vector embeddings for improved semantic retrieval.
- Hybrid sparse and dense retrieval.
- Improved Hinglish query normalization.
- Expanded multilingual knowledge base.
- Advanced retrieval evaluation and benchmarking.
- Improved conversational memory.
- Deployment and scalability improvements.

## 👩‍💻 Developer

**Sanchi Preet Kaur**

- Degree: B.Tech
- Department: Computer Science and Engineering (Data Science)
- Institution: Haldia Institute of Technology
- Academic Year: 2025–2026

## 📄 License

Developed for educational, academic, and portfolio purposes.

---

<p align="center">
  <b>Built with ❤️ using Python, Streamlit, and Groq</b>
</p>

<p align="center">
  If you find this project interesting, consider giving it a ⭐ on GitHub!
</p>
