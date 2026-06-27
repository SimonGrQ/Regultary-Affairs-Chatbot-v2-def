import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# IMPORTANTE: Cambiado al nuevo paquete para evitar fallos de persistencia en disco
from langchain_chroma import Chroma 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
# Cargar variables de entorno (GEMINI_API_KEY)
load_dotenv()

# Sincronizado con el modelo de embeddings actual de Google
#embedding = GoogleGenerativeAIEmbeddings(
#    model="models/gemini-embedding-001", 
#    google_api_key=os.getenv("GEMINI_API_KEY")
#)

# Este modelo es gratuito, libre, se descarga a tu pc y es excelente para español
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# Crear la carpeta automáticamente si no existe para evitar errores
if not os.path.exists("documents"):
    os.makedirs("documents")
    print("Se creó la carpeta 'documents'. Coloca tus archivos PDF allí.")

documents = []

# Leer todos los PDFs de la carpeta de forma segura
for file in os.listdir("documents"):
    if file.endswith(".pdf"):
        file_path = os.path.join("documents", file) 
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # Guardamos el origen y número de página en los metadatos de cada fragmento
        for i, d in enumerate(docs):
            d.metadata["source"] = file
            d.metadata["page"] = i + 1 
        documents.extend(docs)

# Validación por si olvidas meter PDFs
if not documents:
    print("Error: No se encontraron archivos PDF en la carpeta 'documents'.")
else:
    # Segmentación del texto
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    # Creación y guardado físico de la base de datos vectorial
    db = Chroma.from_documents(chunks, embedding, persist_directory="mdr_db")
    print(f"Base documental creada con éxito: {len(chunks)} chunks guardados en mdr_db/")