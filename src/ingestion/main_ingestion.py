import os
from document_loader import process_unstructured_documents
from structured_loader import process_structured_documents
from chunker import chunk_processed_documents


def run_pipeline():
    print("==================================================")
    print("INICIANDO PIPELINE DE INGESTA CORPORATIVA")
    print("==================================================")

    # 1. Procesar PDFs, Word, HTML y MD
    process_unstructured_documents()

    print("-" * 50)

    # 2. Procesar CSVs y planillas
    process_structured_documents()

    print("-" * 50)

    # 3. Aplicar estrategia de chunking sobre los textos limpios
    chunks = chunk_processed_documents(chunk_size=1000, chunk_overlap=200)

    print("==================================================")
    print(f"✅ PIPELINE FINALIZADO CON ÉXITO - {len(chunks)} CHUNKS LISTOS PARA VECTORIZAR")
    print("==================================================")


if __name__ == "__main__":
    run_pipeline()

