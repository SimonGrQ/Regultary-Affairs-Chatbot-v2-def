import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


def configure_gemini(api_key=None, system_instruction=None, model_name="gemini-1.5-flash", temperature=0.1):
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction,
        generation_config={"temperature": temperature},
    )


def load_vector_db(persist_directory="mdr_db"):
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )
    return Chroma(persist_directory=persist_directory, embedding_function=embedding)


def retrieve_context(db, query, k=5):
    docs = db.similarity_search(query, k=k)
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_prompt(context, user_question):
    return f"""
Utiliza únicamente la documentación siguiente.
======================
{context}
======================
Pregunta del usuario:
{user_question}

Responde citando siempre el documento y la regla correspondiente.
"""
