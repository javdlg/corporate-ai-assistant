from langgraph.graph import StateGraph, START, END

from src.agents.state import AgentState
from src.agents.nodes import retrieve_documents, generate_answer


def create_workflow():
    """
    Crea, conecta los nodos y compila el flujo de trabajo (workflow) 
    del Asistente AI utilizando LangGraph.
    """
    # 1. Inicializamos el grafo basado en nuestro AgentState
    workflow = StateGraph(AgentState)
    
    # 2. Registramos los nodos lógicos del RAG
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("generate", generate_answer)
    
    # 3. Definimos las conexiones (aristas/edges)
    # El flujo comienza recuperando documentos
    workflow.add_edge(START, "retrieve")
    
    # Luego de recuperar, pasa al nodo de generación de respuesta
    workflow.add_edge("retrieve", "generate")
    
    # El flujo finaliza tras generar la respuesta
    workflow.add_edge("generate", END)
    
    # 4. Compilamos el grafo
    app = workflow.compile()
    return app


# Instancia compilada del grafo lista para ser importada por el frontend o consola
app = create_workflow()
