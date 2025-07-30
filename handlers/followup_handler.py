import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from .rag_handler import get_context_from_rag

load_dotenv()

def generate_followup_answer(question: str):
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

        context = get_context_from_rag(vectorstore, question)

        rag_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Use the context below to answer the question clearly.

Context:
{context}

Question: {question}

Answer:""")

        llm = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")
        chain = LLMChain(llm=llm, prompt=rag_prompt)

        return chain.run(context=context, question=question).strip()

    except Exception as e:
        return f"⚠️ Could not answer using RAG: {str(e)}"
