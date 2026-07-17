# 🏢 Corporate AI Assistant

## 📝 Descripción del Proyecto
Agente de Inteligencia Artificial corporativo desarrollado para centralizar la base de conocimiento de una organización. Este sistema permite a los colaboradores consultar políticas de RRHH, reportes financieros, manuales operativos y estructuras de datos internos interactuando en lenguaje natural.

El proyecto es la solución oficial al desafío **"ONE AI for TECH" de Oracle y Alura Latam**, destacando la capacidad de procesar datos multimodales y orquestar flujos de trabajo inteligentes mediante grafos.

## 🎯 Características Principales (Requisitos del Desafío)
- **Ingesta Multimodal:** Capacidad de lectura y procesamiento de múltiples formatos de archivo corporativos, incluyendo: `PDF`, `Word`, `Excel`, `Markdown`, `CSV`, `JSON` y `HTML`.
- **RAG Avanzado:** Arquitectura de *Retrieval-Augmented Generation* para garantizar respuestas precisas basadas estrictamente en la documentación interna.
- **Orquestación Multi-Agente:** Implementación de enrutadores inteligentes utilizando **LangGraph** para dirigir las consultas al procesador de documentos adecuado.
- **Despliegue en la Nube:** Alojado en **Streamlit Community Cloud**.

## 🛠️ Arquitectura y Tecnologías (Stack)
* **LLM Core:** Gemini API (Google).
* **Framework de IA:** LangChain & LangGraph.
* **Procesamiento de Datos:** Pandas, PyPDF, Python-docx, BeautifulSoup.
* **Vector Store:** ChromaDB.
* **Frontend:** Streamlit (Interfaz conversacional ágil).
* **Infraestructura:** Streamlit Community Cloud.

## 📂 Estructura del Directorio
```text
├── data/
│   ├── raw/                 # Documentos crudos (PDFs, Excels, Word)
│   └── processed/           # Textos limpios y vectorizados
├── src/
│   ├── ingestion/           # Scripts de carga multimodal (Loaders)
│   ├── agents/              # Nodos de LangGraph y lógica de RAG
│   └── graph/               # Definición del flujo del grafo (Workflow)
├── app.py                   # Frontend en Streamlit y punto de entrada
├── requirements.txt
└── README.md
```

## 🚀 Despliegue en la Nube (Demostración)
La aplicación se encuentra desplegada y completamente operativa en Streamlit Community Cloud. Puedes acceder a ella e interactuar con el agente a través del siguiente enlace público:

🔗 **[Acceder al Asistente AI Corporativo](https://corporate-ai-assistant.streamlit.app/)**

*(Nota: Una vez generado el GIF de demostración con ScreenToGif, se puede colocar en esta sección reemplazando el placeholder inferior).*

![Demo Placeholder](https://via.placeholder.com/800x400.png?text=Agente+Ejecutándose+en+Streamlit+Cloud)

## ⚙️ Instrucciones de Uso Local
1. Clonar este repositorio.
2. Crear un entorno virtual e instalar dependencias: `pip install -r requirements.txt`
3. Colocar los documentos de prueba en `data/raw/`.
4. Configurar el archivo `.env` con las credenciales de Gemini API.
5. Ejecutar la interfaz: `streamlit run app.py`
