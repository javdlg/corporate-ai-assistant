import os
import pandas as pd
from pydantic import BaseModel, ValidationError

# Configuración de rutas
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


# 1. Definimos el esquema esperado usando Pydantic
class TransaccionFinanciera(BaseModel):
    id_transaccion: str
    departamento: str
    categoria: str
    monto_usd: float
    fecha: str


def process_financial_csv(file_path):
    """Lee un CSV, valida con Pydantic y lo convierte a texto semántico."""
    text_chunks = []
    try:
        df = pd.read_csv(file_path)

        for index, row in df.iterrows():
            try:
                # 2. Validación: Pydantic verifica que la fila cumpla con el esquema
                transaccion = TransaccionFinanciera(**row.to_dict())

                # 3. Transformación Semántica: Convertimos la fila en un texto natural
                oracion = (
                    f"El departamento de {transaccion.departamento} registró un gasto de "
                    f"${transaccion.monto_usd} USD en la categoría '{transaccion.categoria}' "
                    f"el día {transaccion.fecha}. (ID de transacción: {transaccion.id_transaccion})."
                )
                text_chunks.append(oracion)

            except ValidationError as e:
                print(f"⚠️ Fila {index} ignorada por error de validación: {e}")

        return "\n".join(text_chunks)

    except Exception as e:
        print(f"❌ Error leyendo CSV {file_path}: {e}")
        return ""


def process_structured_documents():
    print("📊 Iniciando pipeline de ingesta de datos estructurados (CSV/Excel)...")
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".csv"):
            file_path = os.path.join(RAW_DIR, filename)
            print(f"📄 Procesando tabla: {filename}...")

            # Extraemos y transformamos
            semantic_text = process_financial_csv(file_path)

            if semantic_text:
                out_name = f"{os.path.splitext(filename)[0]}_semantico.txt"
                out_path = os.path.join(PROCESSED_DIR, out_name)

                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(semantic_text)
                print(f"✅ Guardado en processed como texto semántico: {out_name}")


if __name__ == "__main__":
    process_structured_documents()
