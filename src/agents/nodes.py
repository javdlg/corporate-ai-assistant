import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agents.state import AgentState
from src.agents.retriever import retrieve_relevant_documents

# Cargar variables de entorno (.env)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
ENV_PATH = os.path.join(PROJECT_DIR, ".env")
load_dotenv(ENV_PATH)


def retrieve_documents(state: AgentState) -> dict:
    """
    Nodo de LangGraph: Recupera documentos relevantes de la base vectorial
    basándose en la pregunta formulada por el usuario.

    Args:
        state: El estado actual del agente.

    Returns:
        dict: Un diccionario con la lista de documentos recuperados.
    """
    print(
        f"🕵️ Nodo retrieve_documents: Buscando información para '{state['question']}'..."
    )

    # Recuperamos los 4 fragmentos más relevantes (k=4)
    docs = retrieve_relevant_documents(state["question"], k=4)
    return {"documents": docs}


def generate_answer(state: AgentState) -> dict:
    """
    Nodo de LangGraph: Genera la respuesta final al usuario utilizando
    el modelo Gemini e inyectando el contexto de los documentos recuperados.

    Args:
        state: El estado actual del agente.

    Returns:
        dict: Un diccionario con la respuesta final generada.
    """
    print("🤖 Nodo generate_answer: Formulando respuesta final con Gemini...")

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "❌ No se encontró la API Key de Gemini en las variables de entorno (.env)."
        )

    # Inicializamos el modelo oficial de chat de Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.2,  # Temperatura baja para garantizar respuestas precisas basadas en el contexto
    )

    # Formateamos el contexto a partir de los documentos recuperados
    docs = state.get("documents", [])
    context_parts = []
    for doc in docs:
        source = doc.metadata.get("source", "Documento corporativo")
        context_parts.append(f"--- Fragmento de {source} ---\n{doc.page_content}")

    context = "\n\n".join(context_parts)

    # Construimos el System Prompt profesional
    system_prompt = (
        "Eres un asistente de Inteligencia Artificial corporativo experto de la empresa OmniCorp.\n"
        "Tu tarea consiste en responder a las consultas de los colaboradores de manera clara, "
        "concisa y profesional, basándote ÚNICAMENTE en el contexto de documentos provisto a continuación.\n\n"
        "Instrucciones críticas de seguridad y veracidad:\n"
        "1. Responde basándote estrictamente en el contexto corporativo provisto. No especules ni inventes datos.\n"
        "2. Si la información solicitada no está presente en el contexto, indica de forma amable "
        "que no dispones de esa información en la base de conocimientos oficial de OmniCorp. No uses conocimiento externo.\n"
        "3. Menciona la fuente u origen del documento de manera profesional (ej. 'Según las Políticas de RRHH...', "
        "'En el Manual de Operaciones se detalla...') en tu respuesta para otorgar trazabilidad.\n\n"
        f"CONTEXTO CORPORATIVO DISPONIBLE:\n{context}\n"
    )

    # Construimos los mensajes para el modelo
    messages = [("system", system_prompt), ("human", state["question"])]

    try:
        response = llm.invoke(messages)
        return {"generation": response.content}
    except Exception as e:
        print(f"❌ Error al invocar a Gemini API: {e}")
        return {
            "generation": f"Lo siento, ocurrió un error interno al intentar procesar tu consulta con el modelo de IA. Detalle técnico: {e}"
        }
