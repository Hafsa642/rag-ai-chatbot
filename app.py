import os
import time

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


DOCUMENTS_PATH = "documents"
DB_PATH = "chroma_db"



all_docs = []

print("\nLoading documents...\n")

for file in os.listdir(DOCUMENTS_PATH):

    if file.endswith(".pdf"):

        file_path = os.path.join(DOCUMENTS_PATH, file)

        print(f"Reading: {file}")

        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            all_docs.extend(docs)

        except Exception as e:
            print(f"Error loading {file}: {e}")

print(f"\nTotal pages loaded: {len(all_docs)}")




text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200
)

texts = text_splitter.split_documents(all_docs)

print(f"Total chunks created: {len(texts)}")




print("\nLoading embedding model...\n")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)





if os.path.exists(DB_PATH):

    print("\nLoading existing Chroma database...\n")

    vector_db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model
    )

else:

    print("\nCreating new Chroma database...\n")

    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )

    vector_db.persist()

print("Vector database ready!")




retriever = vector_db.as_retriever(
    search_kwargs={"k": 5}
)



print("\nLoading LLaMA model...\n")

llm = Ollama(
    model="llama3.2"
)



memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)





qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True
)




print("\n===================================")
print("      RAG CHATBOT READY")
print("===================================\n")

print("Type 'exit' to quit.\n")

while True:

    query = input("You: ")

    if query.lower() == "exit":
        print("\nGoodbye!\n")
        break

    try:

        start = time.time()

        result = qa_chain.invoke({
            "question": query
        })

        end = time.time()

        answer = result["answer"]

        sources = result["source_documents"]

        if len(sources) == 0:

            print("\nBot:")
            print("I could not find relevant information in the uploaded documents.\n")

            continue

        print("\nBot:")
        print(answer)

        print("\nSources:")

        unique_sources = set()

        for doc in sources:

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "?")

            source_text = f"{source} | Page {page}"

            if source_text not in unique_sources:
                print(f"- {source_text}")
                unique_sources.add(source_text)

    except Exception as e:

        print("\nError:", e)
