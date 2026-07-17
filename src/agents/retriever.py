import os
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
ENV_PATH = os.path.join(PROJECT_DIR, ".env")
load_dotenv(ENV_PATH)

from src.agents.vector_store import get_vector_store


def retrieve_relevant_documents(query: str, k: int = 4):
    """
    Recibe una pregunta en lenguaje natural y busca los K fragmentos 
    más relevantes en la base vectorial ChromaDB.
    """
    try:
        vector_store = get_vector_store()
        
        # Realizamos la búsqueda por similitud
        docs = vector_store.similarity_search(query, k=k)
        return docs
    except Exception as e:
        print(f"❌ Error al recuperar documentos de ChromaDB: {e}")
        return []


def test_retriever():
    """
    Función de prueba en consola para verificar la exactitud de la recuperación de información.
    """
    print("\n🔍 --- PROBADOR DE RECUPERACIÓN SEMÁNTICA (RETRIEVER) ---")
    
    # Preguntas de prueba alineadas con los 4 documentos corporativos reales
    test_queries = [
        "¿Cuáles son las políticas de vacaciones en la empresa y los días especiales?",
        "¿Cuál es el stack tecnológico oficial para ingeniería de datos?",
        "¿Cuáles son los acuerdos de nivel de servicio (SLA) para incidentes críticos?",
        "¿Cuánto gastó el departamento de IT en infraestructura Cloud en enero?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print("\n──────────────────────────────────────────────────")
        print(f"Pregunta {i}: '{query}'")
        print("──────────────────────────────────────────────────")
        
        results = retrieve_relevant_documents(query, k=2)
        
        if not results:
            print("⚠️ No se encontraron resultados. ¿Inicializaste la base de datos corriendo el pipeline de ingesta?")
            continue
            
        for idx, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'Desconocido')
            chunk_id = doc.metadata.get('chunk_id', '?')
            total = doc.metadata.get('total_chunks', '?')
            
            print(f"\n[Resultado {idx}] (Origen: {source} | Chunk: {chunk_id}/{total})")
            print(f"📝 Contenido:\n{doc.page_content.strip()}")


if __name__ == "__main__":
    test_retriever()
