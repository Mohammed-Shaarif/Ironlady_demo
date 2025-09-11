# Ironlady Task 1: RAG Chatbot with Streamlit

This project implements a Retrieval-Augmented Generation (RAG) chatbot using Streamlit for the user interface. It allows users to interact with a chatbot that leverages a custom knowledge base (PDFs) for context-aware responses.

---

## Features
- **PDF Knowledgebase Upload:** Users can upload PDF documents to build a searchable knowledge base.
- **RAG Chatbot:** Chat interface powered by RAG, combining retrieval and generative AI (OpenAI API).
- **Streamlit UI:** Simple, interactive web interface for chatting and managing knowledge sources.
- **Modular Codebase:** Separate modules for building the RAG index, chat logic, and UI.

---

## Directory Structure
```
ironlady_task1/
  src/
    rag_build.py        # Logic for building the RAG index from PDFs
    rag_chat.py         # Chatbot logic using retrieval and OpenAI
    streamlit_ui.py     # Streamlit web interface
    docs/               # Folder for PDF knowledgebase
    index/              # Folder for index files
  env.sample            # Sample environment variables (API keys, etc.)
```

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- pip
- OpenAI API key (for generative responses)

### 1. Clone the Repository
```powershell
git clone <repo-url>
cd ironlady_task1
```

### 2. Create & Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Requirements
If you have a `requirements.txt` file:
```powershell
pip install -r src/requirements.txt
```
If not, install manually:
```powershell
pip install streamlit PyPDF2 openai
```

### 4. Set Environment Variables
Copy `env.sample` to `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your-key-here
```

### 5. Prepare Knowledgebase
- Place your PDF files in the `src/docs/` directory.

### 6. Run the Streamlit App
```powershell
streamlit run src/streamlit_ui.py
```

---

## Usage
1. Open the Streamlit app in your browser (usually at http://localhost:8501).
2. Upload PDF files to build the knowledgebase.
3. Start chatting with the RAG-powered bot.

---

## Common Issues & Troubleshooting
- **Missing Packages:** If you get `ModuleNotFoundError`, install missing packages with `pip install <package>`.
- **OpenAI API Key Error:** Ensure your API key is set in `.env` or as an environment variable.
- **PDF Parsing Issues:** Use readable, non-encrypted PDFs.
- **Streamlit Not Found:** Install with `pip install streamlit`.
- **Index Not Building:** Check for errors in `rag_build.py` and ensure PDFs are present in `docs/`.

---

## License
MIT License
