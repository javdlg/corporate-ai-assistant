from typing import List, TypedDict
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    Definición del estado que fluye a través del grafo de LangGraph.
    
    Attributes:
        question: La consulta original en lenguaje natural enviada por el usuario.
        documents: Lista de fragmentos (Document) recuperados de ChromaDB.
        generation: La respuesta final generada por el LLM.
        chat_history: Historial de la conversación para dar soporte al contexto multivuelta.
    """
    question: str
    documents: List[Document]
    generation: str
    chat_history: List[BaseMessage]
    is_on_topic: bool
