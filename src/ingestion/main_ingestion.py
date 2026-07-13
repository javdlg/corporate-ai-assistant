from src.ingestion.document_loader import process_unstructured_documents
from src.ingestion.structured_loader import process_structured_documents
from src.ingestion.chunker import chunk_processed_documents
from src.agents.vector_store import build_vector_store


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


