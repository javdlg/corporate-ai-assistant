from langgraph.graph import StateGraph, START, END

from src.agents.state import AgentState
from src.agents.nodes import retrieve_documents, generate_answer, check_guardrails


def should_continue(state: AgentState) -> str:
    """
    Decide si continuar a la fase de recuperación (RAG) o terminar
    el flujo en base al resultado del guardrail.
    """
    if state.get("is_on_topic", True):
        return "retrieve"
    else:
        return "end"


def create_workflow():
    """
    Crea, conecta los nodos y compila el flujo de trabajo (workflow) 
    del Asistente AI utilizando LangGraph.
    """
    # 1. Inicializamos el grafo basado en nuestro AgentState
    workflow = StateGraph(AgentState)
    
    # 2. Registramos los nodos lógicos del RAG
    workflow.add_node("guardrail", check_guardrails)
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("generate", generate_answer)
    
    # 3. Definimos las conexiones (aristas/edges)
    # Iniciamos validando los guardrails
    workflow.add_edge(START, "guardrail")
    
    # Arista condicional: enrutamos según el resultado del guardrail
    workflow.add_conditional_edges(
        "guardrail",
        should_continue,
        {
            "retrieve": "retrieve",
            "end": END
        }
    )
    
    # Luego de recuperar, pasa al nodo de generación de respuesta
    workflow.add_edge("retrieve", "generate")
    
    # El flujo finaliza tras generar la respuesta
    workflow.add_edge("generate", END)
    
    # 4. Compilamos el grafo
    app = workflow.compile()
    return app


# Instancia compilada del grafo lista para ser importada por el frontend o consola
app = create_workflow()
