import os
from document_loader import process_unstructured_documents
from structured_loader import process_structured_documents


def run_pipeline():
    print("==================================================")
    print("INICIANDO PIPELINE DE INGESTA CORPORATIVA")
    print("==================================================")

    # 1. Procesar PDFs, Word, HTML y MD
    process_unstructured_documents()

    print("-" * 50)

    # 2. Procesar CSVs y planillas
    process_structured_documents()

    print("==================================================")
    print("✅ PIPELINE FINALIZADO CON ÉXITO")
    print("==================================================")


if __name__ == "__main__":
    run_pipeline()
