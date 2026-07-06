import os
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


def chunk_processed_documents(chunk_size=1000, chunk_overlap=200):
    """
    Lee los archivos planos en data/processed/, aplica RecursiveCharacterTextSplitter
    y devuelve una lista de objetos Document con metadatos contextuales.
    """
    print("✂️ Iniciando módulo de fragmentación de texto (Chunking)...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    all_chunks = []

    if not os.path.exists(PROCESSED_DIR):
        print(f"⚠️ El directorio de datos procesados '{PROCESSED_DIR}' no existe.")
        return all_chunks

    for filename in os.listdir(PROCESSED_DIR):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(PROCESSED_DIR, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                continue

            # Generamos los fragmentos asociando el nombre de origen como metadato
            chunks = splitter.create_documents(
                texts=[content],
                metadatas=[{"source": filename}]
            )

            # Enriquecemos cada chunk con índice de fragmento y total del archivo
            for idx, chunk in enumerate(chunks):
                chunk.metadata["chunk_id"] = idx
                chunk.metadata["total_chunks"] = len(chunks)
                all_chunks.append(chunk)

            print(f"🧩 '{filename}': {len(chunks)} fragmento(s) generado(s).")

        except Exception as e:
            print(f"❌ Error al procesar chunking para '{filename}': {e}")

    print(f"✅ Fragmentación completada: {len(all_chunks)} chunks totales creados.")
    return all_chunks


if __name__ == "__main__":
    chunk_processed_documents()
