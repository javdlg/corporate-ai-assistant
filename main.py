import os
from dotenv import load_dotenv

# Cargar variables de entorno
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from src.graph.workflow import app


def run_console_assistant():
    """
    Script principal de prueba en consola para interactuar de forma directa
    con el Asistente AI corporativo de OmniCorp a través de LangGraph.
    """
    print("================================================================")
    print("🏢   ASISTENTE AI CORPORATIVO OMNICORP - MODO CONSOLA   🏢")
    print("================================================================")
    print("Escribe tu consulta y presiona Enter. Escribe 'salir' para finalizar.\n")
    
    # Validamos que exista la API Key antes de arrancar
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        print("❌ ERROR: No se encontró la API Key de Gemini configurada en tu archivo .env.")
        print("Por favor, crea el archivo .env a partir de .env.example y añade tu GOOGLE_API_KEY.")
        return

    chat_history = []

    while True:
        try:
            question = input("\nColaborador 👤: ").strip()
            if not question:
                continue
            
            if question.lower() in ["salir", "exit", "quit"]:
                print("\n👋 ¡Gracias por usar el Asistente AI de OmniCorp! Hasta luego.")
                break
                
            print("⏳ Pensando...")
            
            # Inicializamos el estado del agente
            inputs = {
                "question": question,
                "chat_history": chat_history,
                "documents": [],
                "generation": ""
            }
            
            # Ejecutamos el grafo completo (Ingesta/Recuperación -> Generación)
            result = app.invoke(inputs)
            
            # Mostramos la respuesta generada
            print(f"\nOmniCorp Assistant 🤖:\n{result['generation']}")
            
            # Mostramos las fuentes recuperadas como evidencia de trazabilidad profesional
            if result.get("documents"):
                print("\n📚 Fuentes consultadas:")
                seen_sources = set()
                for doc in result["documents"]:
                    source = doc.metadata.get("source", "Desconocido")
                    chunk_id = doc.metadata.get("chunk_id", "?")
                    total = doc.metadata.get("total_chunks", "?")
                    source_key = f"{source} (Chunk {chunk_id}/{total})"
                    
                    if source_key not in seen_sources:
                        print(f"   • {source_key}")
                        seen_sources.add(source_key)
            
            # Actualizamos el historial de conversación (opcional para mantener contexto)
            chat_history.append(("human", question))
            chat_history.append(("ai", result["generation"]))
            
        except KeyboardInterrupt:
            print("\n👋 Sesión finalizada por el usuario.")
            break
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    run_console_assistant()
