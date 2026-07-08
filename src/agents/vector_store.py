import os
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# Imports con compatibilidad hacia atrás y adelante para LangChain / Chroma
try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Ruta persistente para la base vectorial ChromaDB
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")


def get_embedding_function():
    """
    Inicializa y retorna el modelo de embeddings de Google Gemini.
    Requiere que GOOGLE_API_KEY o GEMINI_API_KEY esté configurada en el archivo .env.
    """
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "❌ No se encontró GOOGLE_API_KEY en las variables de entorno. "
            "Por favor, configura tu API Key en el archivo .env."
        )

    # Inicializamos el modelo oficial de embeddings de Gemini (text-embedding-004)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=api_key
    )
    return embeddings


def get_vector_store():
    """
    Obtiene o inicializa la instancia de ChromaDB persistente en el directorio chroma_db.
    """
    embeddings = get_embedding_function()
    
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name="corporate_knowledge_base"
    )
    return vector_store


def build_vector_store(chunks):
    """
    Toma una lista de fragmentos (Document) de LangChain, genera sus embeddings con Gemini
    y los almacena de forma persistente en ChromaDB.
    """
    if not chunks:
        print("⚠️ No hay fragmentos para indexar.")
        return None

    print(f"📦 Indexando {len(chunks)} fragmentos en ChromaDB (directorio: {CHROMA_PATH})...")

    embeddings = get_embedding_function()

    # Creamos/Actualizamos la colección en ChromaDB
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="corporate_knowledge_base"
    )

    print(f"✅ Indexación completada exitosamente en ChromaDB.")
    return vector_store


if __name__ == "__main__":
    print("🧪 Probando inicialización de Gemini Embeddings y ChromaDB...")
    try:
        store = get_vector_store()
        print("✅ Conexión e inicialización de ChromaDB con Gemini Embeddings correcta.")
    except Exception as e:
        print(f"⚠️ Nota de configuración: {e}")
