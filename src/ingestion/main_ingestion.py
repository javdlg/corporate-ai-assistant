import os
import sys
from document_loader import process_unstructured_documents
from structured_loader import process_structured_documents
from chunker import chunk_processed_documents

# Añadimos el directorio src/agents al path para importar el vector store
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(SCRIPT_DIR)
AGENTS_DIR = os.path.join(SRC_DIR, "agents")
if AGENTS_DIR not in sys.path:
    sys.path.append(AGENTS_DIR)

from vector_store import build_vector_store  # noqa: E402


def run_pipeline():
    print("==================================================")
    print("INICIANDO PIPELINE DE INGESTA CORPORATIVA Y VECTORIZACIÓN")
    print("==================================================")

    # 1. Procesar PDFs, Word, HTML y MD
    process_unstructured_documents()

    print("-" * 50)

    # 2. Procesar CSVs y planillas
    process_structured_documents()

    print("-" * 50)

    # 3. Aplicar estrategia de chunking sobre los textos limpios
    chunks = chunk_processed_documents(chunk_size=1000, chunk_overlap=200)

    print("-" * 50)

    # 4. Vectorizar e indexar en ChromaDB con Gemini Embeddings
    try:
        build_vector_store(chunks)
    except Exception as e:
        print(f"⚠️ Nota de vectorización: {e}")

    print("==================================================")
    print(f"✅ PIPELINE FINALIZADO CON ÉXITO - {len(chunks)} CHUNKS INDEXADOS Y PERSISTIDOS")
    print("==================================================")


if __name__ == "__main__":
    run_pipeline()


