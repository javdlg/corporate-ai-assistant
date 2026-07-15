import os
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO
# ==========================================
st.set_page_config(
    page_title="OmniCorp AI Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para mejorar la estética visual
st.markdown("""
    <style>
        /* Estilo general y tipografía */
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
        /* Ajuste de márgenes del sidebar */
        .css-1d391kg {
            padding-top: 2rem;
        }
        /* Contenedores de documentos */
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

# Ruta del directorio de documentos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

# ==========================================
# 2. BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/company.png", width=70)
    st.title("OmniCorp Control")
    st.markdown("---")
    
    st.subheader("📂 Base de Conocimiento")
    st.caption("Documentos crudos detectados en `data/raw/`:")
    
    # Escaneamos y listamos los archivos en data/raw/
    if os.path.exists(RAW_DIR):
        files = [f for f in os.listdir(RAW_DIR) if os.path.isfile(os.path.join(RAW_DIR, f)) and f != ".gitkeep"]
        
        if files:
            for file in files:
                st.markdown(f'<div class="doc-item">📄 {file}</div>', unsafe_allow_html=True)
            st.success(f"Se detectaron {len(files)} archivos corporativos.")
        else:
            st.info("La carpeta `data/raw/` está vacía. Añade archivos en formato PDF, Word, Excel, CSV, etc.")
    else:
        st.error("No se encontró el directorio de datos `data/raw/`.")

# ==========================================
# 3. ÁREA PRINCIPAL (CHAT INTERACTIVE)
# ==========================================
st.markdown('<div class="main-title">🏢 Asistente AI de OmniCorp</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interactúa con la base de conocimiento oficial de la empresa para resolver dudas operativas, políticas o financieras.</div>', unsafe_allow_html=True)

# Contenedor del chat de prueba (vacío temporalmente para el Paso 1)
welcome_placeholder = st.empty()
with welcome_placeholder.container():
    st.info("👋 **¡Bienvenido al canal oficial de consultas!** Escribe una pregunta sobre vacaciones, gastos, manuales técnicos o SLAs abajo para comenzar la conversación.")

# Entrada del chat (visual por ahora)
st.chat_input("Escribe tu consulta aquí...")
