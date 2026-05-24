import os
import shutil
from fastapi import UploadFile, File
from langchain.prompts import PromptTemplate
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document

# SETTINGS

DOCUMENTS_PATH = "documents"
DB_PATH = "chroma_db_main"

# FAST API

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LOAD DOCUMENTS

all_docs = []

print("Loading documents...")

for file in os.listdir(DOCUMENTS_PATH):

    file_path = os.path.join(DOCUMENTS_PATH, file)

    try:

        if file.endswith(".pdf"):

            loader = PyPDFLoader(file_path)
            docs = loader.load()

            all_docs.extend(docs)

        elif file.endswith(".txt"):

            with open(file_path, "r", encoding="utf-8") as f:

                text = f.read()

            docs = [Document(page_content=text)]

            all_docs.extend(docs)

    except Exception as e:

        print(f"Error loading {file}: {e}")

print(f"Loaded pages: {len(all_docs)}")

# TEXT SPLITTING

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=400
)

texts = text_splitter.split_documents(all_docs)

for doc in texts:
    doc.page_content = doc.page_content.lower()

print(f"Chunks created: {len(texts)}")

# EMBEDDINGS

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# VECTOR DATABASE

if os.path.exists(DB_PATH):

    print("Loading existing Chroma DB...")

    vector_db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model
    )

else:

    print("Creating new Chroma DB...")

    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )

    vector_db.persist()

# RETRIEVER

retriever = vector_db.as_retriever(
    search_kwargs={
        "k": 4,
    }
)
# LLM

llm = Ollama(
    model="llama3.2"
)

# MEMORY
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)


template = """
You are a helpful AI research assistant.

Answer ONLY from the provided context.

If the answer exists in the context, explain it clearly and completely.

Do not say 'I don't know' unless the context truly lacks the answer.

Context:
{context}

Question:
{question}

Answer:
"""

QA_PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)
# RAG CHAIN

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    combine_docs_chain_kwargs={
        "prompt": QA_PROMPT
    }
)
# REQUEST MODEL

class ChatRequest(BaseModel):
    question: str
# API ENDPOINT

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        result = qa_chain.invoke({
            "question": request.question.lower()
        })

        answer = result["answer"]

        sources = []

        for doc in result["source_documents"]:

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "?")

            sources.append({
                "source": source,
                "page": page
            })

        if len(sources) == 0:

            return {
                "answer": "I could not find relevant information in the uploaded documents.",
                "sources": []
            }

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:

        return {
            "error": str(e)
        }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    global vector_db
    global retriever
    global qa_chain

    file_path = os.path.join(
        DOCUMENTS_PATH,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # load uploaded pdf

    loader = PyPDFLoader(file_path)

    docs = loader.load()

    # split text

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    texts = text_splitter.split_documents(docs)

    # lowercase for better matching

    for doc in texts:
        doc.page_content = doc.page_content.lower()

    # create NEW database every upload

    upload_db = f"chroma_upload_{file.filename}"

    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embedding_model,
        persist_directory=upload_db
    )

    vector_db.persist()

    retriever = vector_db.as_retriever(
        search_kwargs={"k": 4}
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={
            "prompt": QA_PROMPT
        }
    )

    return {
        "message": "File uploaded successfully"
    }
