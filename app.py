import os
import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno y configurar rutas antes de importar el workflow
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Importamos el grafo de LangGraph
from src.graph.workflow import app as workflow_app

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO
# ==========================================
st.set_page_config(
    page_title="OmniCorp AI Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1E3A8A;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            font-size: 1.1rem;
            color: #4B5563;
            margin-bottom: 2rem;
        }
        .doc-item {
            padding: 8px 12px;
            background-color: #F3F4F6;
            border-left: 4px solid #3B82F6;
            border-radius: 4px;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

# ==========================================
# 2. BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/company.png", width=70)
    st.title("OmniCorp Control")
    st.markdown("---")
    
    # Validación y configuración interactiva de API Key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.warning("⚠️ API Key de Gemini no configurada.")
        user_key = st.text_input("Ingresa tu GOOGLE_API_KEY:", type="password")
        if user_key:
            os.environ["GOOGLE_API_KEY"] = user_key
            st.success("API Key configurada temporalmente.")
            st.rerun()
    else:
        st.success("🔑 Gemini API Key activa.")
        
    st.markdown("---")
    st.subheader("📂 Base de Conocimiento")
    st.caption("Documentos crudos detectados en `data/raw/`:")
    
    if os.path.exists(RAW_DIR):
        files = [f for f in os.listdir(RAW_DIR) if os.path.isfile(os.path.join(RAW_DIR, f)) and f != ".gitkeep"]
        if files:
            for file in files:
                st.markdown(f'<div class="doc-item">📄 {file}</div>', unsafe_allow_html=True)
            st.success(f"Se detectaron {len(files)} archivos corporativos.")
        else:
            st.info("La carpeta `data/raw/` está vacía.")
    else:
        st.error("No se encontró el directorio `data/raw/`.")

    st.markdown("---")
    st.subheader("⚙️ Acciones")
    
    # Botón para correr el pipeline de ingesta (Paso 3)
    if st.button("🔄 Actualizar Base Vectorial", use_container_width=True, disabled=not api_key):
        with st.spinner("Ejecutando pipeline de ingesta, fragmentación e indexación en ChromaDB..."):
            try:
                from src.ingestion.main_ingestion import run_pipeline
                run_pipeline()
                st.success("¡Base vectorial actualizada exitosamente!")
                st.rerun()
            except Exception as e:
                st.error(f"Error al actualizar la base: {e}")

# ==========================================
# 3. GESTIÓN DE HISTORIAL (STATE)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# 4. ÁREA PRINCIPAL (CHAT INTERACTIVE)
# ==========================================
st.markdown('<div class="main-title">🏢 Asistente AI de OmniCorp</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interactúa con la base de conocimiento oficial de la empresa para resolver dudas operativas, políticas o financieras.</div>', unsafe_allow_html=True)

# Mensaje de bienvenida si no hay historial
if not st.session_state.messages:
    st.info("👋 **¡Bienvenido al canal oficial de consultas!** Escribe una pregunta sobre vacaciones, gastos, manuales técnicos o SLAs abajo para comenzar la conversación.")

# Renderizado de historial de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        st.write(msg["content"])

# Captura de la entrada del usuario
if question := st.chat_input("Escribe tu consulta aquí...", disabled=not api_key):
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.write(question)
        
    # Invocación de LangGraph
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        with st.spinner("Buscando en base de conocimientos y generando respuesta..."):
            try:
                inputs = {
                    "question": question,
                    "chat_history": st.session_state.chat_history,
                    "documents": [],
                    "generation": ""
                }
                result = workflow_app.invoke(inputs)
                answer = result["generation"]
                documents = result.get("documents", [])
                
                # Renderizar respuesta
                message_placeholder.write(answer)
                
                # Actualizar historial en sesión
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "documents": documents
                })
                st.session_state.chat_history.append(("human", question))
                st.session_state.chat_history.append(("ai", answer))
                
                # Pedir rerun para actualizar la vista limpia
                st.rerun()
            except Exception as e:
                st.error(f"Ocurrió un error al procesar tu consulta: {e}")
