
# 🗡️ Raji — Game Assistant

An offline-first, zero-API-key Retrieval-Augmented Generation (RAG)-style game assistant built using **Python**, **Streamlit**, and **Scikit-learn** for the action-adventure video game *Raji: An Ancient Epic*, developed by Nodding Heads Games.

---

## 1. Project Overview

Raji — Game Assistant is an interactive web-based chatbot designed to help players access information about the game *Raji: An Ancient Epic*.

The application uses Natural Language Processing (NLP) and information retrieval techniques to find relevant answers from a predefined knowledge base. It uses TF-IDF vectorization and cosine similarity to identify the most relevant information.

Unlike conventional AI assistants that depend on external Large Language Model (LLM) APIs, this application uses a lightweight, locally executable retrieval system without requiring paid API keys.

---

## 2. Problem Statement

Many AI-powered gaming assistants depend on cloud-based LLM APIs and external translation services. These dependencies can introduce:

- API usage costs.
- Internet connectivity requirements.
- Response delays.
- API rate-limit errors.
- Privacy and data-sharing concerns.

Raji — Game Assistant addresses these challenges through a lightweight retrieval-based approach that can run locally.

---

## 3. Project Objectives

The main objectives are:

1. Develop an interactive chatbot dedicated to Raji: An Ancient Epic.
2. Implement a locally executable information retrieval system.
3. Use TF-IDF and cosine similarity to retrieve relevant answers.
4. Provide role-based access for guests and administrators.
5. Allow administrators to upload and manage knowledge documents.
6. Provide multilingual support with offline fallback mechanisms.
7. Develop an accessible interface with dark and light themes.
8. Maintain local chat records, analytics, and support tickets.

---

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application framework |
| Scikit-learn | TF-IDF vectorization and similarity calculation |
| TF-IDF | Text representation |
| Cosine Similarity | Ranking relevant knowledge chunks |
| PyPDF | PDF text extraction |
| Python-docx | DOCX text extraction |
| JSON | Local data persistence |
| Pickle | Serialization of retrieval index |
| HTML and CSS | Interface customization |

Optional voice features may use SpeechRecognition and gTTS.

---

## 5. Key Features

### 5.1 Interactive Chatbot

- Answers questions related to Raji: An Ancient Epic.
- Provides information about characters, weapons, powers, and gameplay.
- Retrieves relevant information from the knowledge base.
- Uses a fallback response when no suitable match is found.

### 5.2 Retrieval-Based Question Answering

- Divides knowledge documents into smaller text chunks.
- Converts text into TF-IDF vectors.
- Compares user queries with stored knowledge.
- Uses cosine similarity to rank matching chunks.
- Applies a similarity threshold to avoid irrelevant answers.

### 5.3 Knowledge Base Management

- Admin-only document upload functionality.
- Supports TXT, PDF, and DOCX documents.
- Extracts text from uploaded documents.
- Updates the retrieval index when new documents are added.

### 5.4 Role-Based Authentication

- Guest or customer access for regular players.
- Administrator access for managing documents and viewing analytics.
- Session-based authentication.

### 5.5 Semantic Search

- Displays the most relevant knowledge chunks.
- Shows cosine similarity scores.
- Helps inspect and understand retrieval results.

### 5.6 Multilingual Support

- English and Hindi offline fallback mechanisms.
- Language-related functionality for supported languages.
- Local translation mappings for selected responses.

### 5.7 Dark and Light Themes

- Single-click theme switching.
- Customized interface elements.
- Improved readability and accessibility.

### 5.8 Analytics and Support

- Tracks user queries.
- Records unanswered questions.
- Displays usage information.
- Allows players to submit support tickets.

---

## 6. System Architecture

The application is divided into five main layers:

1. **Presentation Layer:** Streamlit pages and user interface.
2. **Authentication Layer:** Guest and administrator access management.
3. **Retrieval Layer:** Document processing, TF-IDF indexing, and cosine similarity.
4. **Persistence Layer:** Local JSON records and serialized retrieval index.
5. **Knowledge Layer:** Seed game knowledge and administrator-uploaded documents.

### Question Answering Workflow

1. The user enters a question.
2. The application processes the query.
3. The retrieval engine searches the knowledge base.
4. TF-IDF represents the query and knowledge chunks numerically.
5. Cosine similarity calculates the matching scores.
6. The system identifies the best matching chunk.
7. The similarity threshold determines whether the result is suitable.
8. The application displays the retrieved answer or a fallback message.

---

## 7. Project Structure

```text
raji-game-assistant/
│
├── Home.py
├── requirements.txt
├── README.md
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
│   │   └── raji_game_lore.txt
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

---

## 8. Installation and Setup

### Prerequisites

- Python installed on your computer.
- Visual Studio Code or another Python editor.
- Required project files.

### Step 1: Download the Project

Download or clone the project repository and open its folder in VS Code.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
streamlit run Home.py
```

### Step 6: Open the Application

Open the local address displayed in your terminal. The default address is:

```text
http://localhost:8501
```

---

## 9. Core Modules

| Module | Description |
|---|---|
| `auth.py` | Handles authentication and user roles |
| `rag.py` | Handles document processing, indexing, and retrieval |
| `storage.py` | Manages local JSON data |
| `translate.py` | Handles language routing and translation fallbacks |
| `theme.py` | Provides dark and light themes |
| `sidebar.py` | Manages navigation and sidebar controls |
| `voice.py` | Handles optional voice functionality |

---

## 10. Functional Pages

| Page | Functionality |
|---|---|
| Home | Project introduction and navigation |
| Chat | Interactive game assistant |
| Knowledge Base | Document upload and index management |
| Semantic Search | Displays matching knowledge chunks |
| Analytics | Displays usage and query information |
| Contact Support | Accepts player support requests |

---

## 11. Advantages

- No paid LLM API key required.
- Lightweight retrieval architecture.
- Locally executable core functionality.
- Game-specific knowledge retrieval.
- Easy knowledge base expansion.
- Role-based access control.
- Modular and maintainable project structure.
- Reduced dependence on external cloud services.

---

## 12. Limitations

- Answer quality depends on the knowledge base.
- TF-IDF may not understand complex paraphrased questions.
- The system does not currently demonstrate LLM-based answer generation.
- Translation and optional voice features may have limitations depending on their implementation and network availability.
- Retrieval accuracy depends on the selected similarity threshold.

---

## 13. Future Enhancements

1. Integrate local LLMs using Ollama.
2. Implement dense vector embeddings.
3. Develop hybrid sparse and dense retrieval.
4. Add Hinglish query normalization.
5. Expand the Hindi knowledge base.
6. Improve multilingual question answering.
7. Enhance analytics and retrieval evaluation.

---

## 14. Conclusion

Raji — Game Assistant demonstrates how Natural Language Processing and information retrieval techniques can be used to develop a dedicated gaming assistant.

By combining Python, Streamlit, TF-IDF, and cosine similarity, the application provides a lightweight and locally executable approach to game-related question answering.

The modular architecture also provides opportunities for future improvements, including embedding-based retrieval and local Large Language Model integration.

---

## 15. Developer Information

**Developed by:** Sanchi Preet Kaur  
**Degree:** B.Tech  
**Department:** Computer Science and Engineering (Data Science)  
**Institution:** Haldia Institute of Technology  
**Academic Year:** 2025–2026

---

## 16. License

This project is developed for educational and portfolio purposes.
#   r a j i - g a m e - a s s i s t a n t  
 