import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def load_and_embed_text(file_path: str):
    loader = TextLoader(file_path)
    documents = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    vectorstore.save_local("faiss_index")
    print(f"✅ Embedded and saved: {len(chunks)} chunks")

def get_context_from_rag(vectorstore, question: str, k: int = 3):
    docs = vectorstore.similarity_search(question, k=k)
    return "\n\n".join([doc.page_content for doc in docs])
