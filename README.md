# 🗡️ Raji — Game Assistant

<p align="center">
  A lightweight, offline-first game knowledge assistant for
  <b>Raji: An Ancient Epic</b>.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit" />
  <img src="https://img.shields.io/badge/NLP-TF--IDF-orange" />
  <img src="https://img.shields.io/badge/Approach-Retrieval--Based-success" />
  <img src="https://img.shields.io/badge/API%20Key-Not%20Required-brightgreen" />
</p>

---

## 📌 Overview

**Raji — Game Assistant** is an interactive chatbot designed to help players explore the world, characters, weapons, powers, puzzles, and gameplay of *Raji: An Ancient Epic*.

Built using Python and Streamlit, the application uses Natural Language Processing (NLP) and information retrieval techniques to find relevant answers from a predefined knowledge base.

Instead of relying on paid Large Language Model (LLM) APIs, it uses **TF-IDF vectorization and cosine similarity** to retrieve relevant information locally.

## ✨ Features

| Feature | Description |
|---|---|
| 💬 Interactive Chatbot | Ask questions about Raji: An Ancient Epic |
| 🔎 Smart Retrieval | TF-IDF and cosine similarity-based search |
| 📚 Knowledge Management | Upload TXT, PDF, and DOCX documents |
| 🔐 Role-Based Access | Guest and administrator access |
| 🌐 Multilingual Support | English and Hindi fallback functionality |
| 🎨 Theme Customization | Dark and light themes |
| 📊 Analytics | Track queries and usage information |
| 🎤 Voice Features | Optional speech functionality |
| 🎫 Support System | Submit player support tickets |

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Scikit-learn | Machine learning and retrieval |
| TF-IDF | Text vectorization |
| Cosine Similarity | Document relevance scoring |
| PyPDF | PDF text extraction |
| Python-docx | DOCX processing |
| JSON | Local data storage |
| Pickle | Retrieval index serialization |
| HTML & CSS | UI customization |

## 🧠 How It Works

The application follows a retrieval-based question-answering workflow.

1. User enters a question.
2. The system preprocesses the query.
3. TF-IDF converts the query into a numerical representation.
4. Cosine similarity compares it with stored knowledge chunks.
5. The most relevant chunk is selected.
6. A similarity threshold determines whether the result is reliable.
7. The application displays the answer or a fallback response.

### System Architecture

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
          +----+----+
          |         |
       Relevant   No Match
          |         |
          v         v
       ANSWER    FALLBACK
          |         |
          +----+----+
               |
               v
          USER RESPONSE
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

### 4. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run Home.py
```

### 7. Open in browser

```text
http://localhost:8501
```

## 📸 Application Screenshots

Add screenshots of your actual application here.

| Home Page | Chat Interface |
|---|---|
| Add home screenshot | Add chat screenshot |

| Semantic Search | Analytics |
|---|---|
| Add search screenshot | Add analytics screenshot |

## 🎯 Project Objectives

- Build a dedicated gaming knowledge assistant.
- Implement locally executable information retrieval.
- Apply NLP techniques to game-related questions.
- Support administrator-managed knowledge documents.
- Provide multilingual fallback functionality.
- Develop a modular and accessible web interface.

## ⚠️ Limitations

- Answer quality depends on the available knowledge base.
- TF-IDF may not understand complex semantic relationships.
- The system does not currently generate answers using an LLM.
- Some optional voice and translation features may require internet access.
- Retrieval accuracy depends on the similarity threshold.

## 🚀 Future Enhancements

- Integration with local LLMs using Ollama.
- Dense vector embeddings.
- Hybrid sparse and dense retrieval.
- Hinglish query normalization.
- Expanded Hindi knowledge base.
- Improved multilingual question answering.
- Advanced retrieval evaluation and analytics.

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
  <b>Built with ❤️ using Python and Streamlit</b>
</p>

<p align="center">
  If you find this project interesting, consider giving it a ⭐ on GitHub!
</p>