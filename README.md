# README.md
# 🤖 AI Research Assistant — RAG Chatbot

An advanced Retrieval-Augmented Generation (RAG) AI chatbot developed using React, FastAPI, LangChain, ChromaDB, Hugging Face embeddings, and LLaMA 3.2 via Ollama.

This chatbot allows users to upload PDF and . txt files and ask intelligent questions from uploaded content with contextual AI-generated responses and source citations.

---

# ✨ Features

- 📄 Upload PDF documents directly from frontend
- 🤖 AI-powered conversational chatbot
- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 Semantic document search using embeddings
- 📚 Source citation with page references
- 💬 Conversational memory support
- ⚡ FastAPI backend
- 🎨 Modern React frontend UI
- 🌌 Futuristic AI dashboard design
- 📎 ChatGPT-style file attachment system
- 🔄 Automatic vector database refresh
- 🧾 Support for large documents

---

#  Technologies Used

## Frontend
- React.js
- Axios
- CSS3

## Backend
- FastAPI
- Python

## AI & RAG Stack
- LangChain
- ChromaDB
- Hugging Face Embeddings
- Ollama
- LLaMA 3.2

#  How the RAG System Works

1. User uploads PDF document
2. PDF text is extracted
3. Text is split into chunks
4. Hugging Face generates embeddings
5. Embeddings are stored in ChromaDB
6. User asks a question
7. Retriever finds relevant chunks
8. LLaMA generates contextual response
9. Source citations are displayed

---

#  Project Structure

 text
rag-chatbot/
├── backend.py
├── documents/
├── chroma_db_main/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── requirements.txt
└── README.md
````

⚙️ Installation

1️⃣ Clone Repository

```bash
git clone https://github.com/Hafsa642/rag-ai-chatbot.git
```
2️⃣ Backend Setup

```bash
cd rag-chatbot

python -m venv venv

source venv/bin/activate

Install dependencies:

```bash
pip install fastapi uvicorn langchain langchain-community chromadb sentence-transformers pypdf python-multipart
```
3️⃣ Install Ollama

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh

Pull LLaMA model:

```bash
ollama pull llama3.2

Start Ollama:

```bash
ollama serve
```
## 4️Frontend Setup

```bash
cd frontend

npm install

Install Axios:

```bash
npm install axios


Run frontend:

```bash
npm start
```
#  Run Backend

  bash
cd rag-chatbot

source venv/bin/activate

uvicorn backend:app --host 0.0.0.0 --port 8000
# Frontend Preview

The frontend includes:

* AI dashboard landing page
* Animated robot interface
* Glassmorphism UI
* ChatGPT-style chat interface
* File upload preview
* Auto-scrolling messages
* Loading animations

#  AI Technologies Explained

## LangChain

LangChain was used to build the RAG pipeline and connect:

* LLM
* vector database
* retriever
* conversational memory

## Hugging Face Embeddings

Used to convert document text into semantic vectors using:

  python
sentence-transformers/all-MiniLM-L6-v2

Benefits:

* semantic understanding
* contextual retrieval
* fast vector search

## ChromaDB

Vector database used to:

* store embeddings
* retrieve relevant document chunks
* perform similarity search

## Ollama + LLaMA 3.2

Used as the Large Language Model for:

* conversational responses
* contextual answer generation
* document understanding

#  API Endpoints

## Chat Endpoint

  http
POST /chat

Request:

 json
{
  "question": "What is machine learning?"
}

## Upload Endpoint

 http
POST /upload

Uploads PDF documents for indexing.

# Future Improvements

* Multi-document chat
* Authentication system
* Cloud deployment
* Streaming responses
* Voice input
* OCR support for scanned PDFs
* Dark/light themes

# Developer

Developed by Hafsa as a full-stack AI RAG chatbot project using modern AI technologies and retrieval systems.

#  Acknowledgements

* LangChain
* Hugging Face
* ChromaDB
* Ollama
* Meta LLaMA
* React
* FastAPI

```
```
