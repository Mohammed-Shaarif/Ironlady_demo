# Ironlady Course Management & RAG Chat Project

This repository contains two main components:

1. **Course Management System** (Flask-based web app)
2. **RAG Chatbot** (Streamlit-based UI for Retrieval-Augmented Generation)

---

## 1. Course Management System

A Flask web application for managing courses and students, with CRUD operations and a simple summarizer.

### Features
- Add, view, update, and delete courses
- Add, view, update, and delete students
- Course and student detail pages
- Summarize course information

### Directory Structure
```
Ironlady_demo/
  ironlady_task2/
    app.py                # Main Flask app
    models.py             # SQLAlchemy models
    summarizer.py         # Summarization logic
    init_db.py            # DB initialization
    requirements.txt      # Python dependencies
    templates/            # HTML templates
    course_management.db  # SQLite database
```

---

## 2. RAG Chatbot

A Streamlit UI for interacting with a Retrieval-Augmented Generation chatbot, using a custom knowledge base.

### Features
- Upload and query PDF knowledge base
- Chat interface powered by RAG
- Modular code for building and chatting with RAG

### Directory Structure
```
Ironlady_demo/
  ironlady_task1/
    src/
      rag_build.py        # RAG builder logic
      rag_chat.py         # RAG chat logic
      streamlit_ui.py     # Streamlit UI
      docs/               # Knowledgebase PDFs
      index/              # Index files
    env.sample            # Sample environment variables
```

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the Repository
```powershell
git clone <repo-url>
cd Ironlady_demo
```

### 2. Create & Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Requirements
```powershell
pip install -r ironlady_task2/requirements.txt
pip install -r ironlady_task1/src/requirements.txt  # If exists, else see below
```

#### If `requirements.txt` is missing for `ironlady_task1`, install manually:
```powershell
pip install streamlit PyPDF2 openai
```

### 4. Initialize Database (Course Management)
```powershell
python ironlady_task2/init_db.py
```

### 5. Run Flask App
```powershell
python ironlady_task2/app.py
```

### 6. Run Streamlit RAG Chat UI
```powershell
streamlit run ironlady_task1/src/streamlit_ui.py
```

---

## Common Issues & Troubleshooting

- **Missing Packages**: If you get `ModuleNotFoundError`, install missing packages with `pip install <package>`.
- **Database Errors**: Ensure you run `init_db.py` before starting the Flask app.
- **Streamlit Not Found**: Install with `pip install streamlit`.
- **PDF Parsing Issues**: Ensure your PDFs are not encrypted and are readable by PyPDF2.
- **OpenAI API Key**: For RAG chat, set your OpenAI API key in environment variables or `.env` file.
- **Port Conflicts**: Flask defaults to port 5000, Streamlit to 8501. Change ports if needed.

---

## License
MIT License
