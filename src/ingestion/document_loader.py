import os
from pypdf import PdfReader
from docx import Document
from bs4 import BeautifulSoup
import markdown

# Configuración de rutas dinámicas basadas en la ubicación del script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR)) # Sube a la raíz del proyecto
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def extract_text_from_pdf(file_path):
    """Extrae texto de un archivo PDF."""
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        print(f"❌ Error leyendo PDF {file_path}: {e}")
    return text

def extract_text_from_docx(file_path):
    """Extrae texto de un archivo de Word (.docx)."""
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"❌ Error leyendo Word {file_path}: {e}")
    return text

def extract_text_from_html(file_path):
    """Extrae texto plano de un archivo HTML."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            # get_text() limpia las etiquetas y deja solo el contenido
            return soup.get_text(separator='\n', strip=True)
    except Exception as e:
        print(f"❌ Error leyendo HTML {file_path}: {e}")
        return ""

def process_unstructured_documents():
    """Itera sobre la carpeta raw, procesa los formatos soportados y guarda el texto limpio."""
    print("🚀 Iniciando pipeline de ingesta de texto no estructurado...")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Extensiones que maneja este script (Hito 1.1)
    supported_extensions = ('.pdf', '.docx', '.html', '.md')
    
    for filename in os.listdir(RAW_DIR):
        if not filename.lower().endswith(supported_extensions):
            continue # Ignora CSV, JSON, Excel por ahora (van al Hito 1.2)
            
        file_path = os.path.join(RAW_DIR, filename)
        text = ""
        
        print(f"📄 Procesando: {filename}...")
        
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(file_path)
        elif filename.endswith(".html"):
            text = extract_text_from_html(file_path)
        elif filename.endswith(".md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_text = f.read()
                    # Convertimos MD a HTML y luego usamos BeautifulSoup para extraer texto limpio
                    html_content = markdown.markdown(md_text)
                    text = BeautifulSoup(html_content, 'html.parser').get_text(separator='\n', strip=True)
            except Exception as e:
                print(f"❌ Error leyendo Markdown {file_path}: {e}")
        
        if text.strip():
            # Guardamos el resultado en la carpeta processed como un .txt limpio
            out_name = f"{os.path.splitext(filename)[0]}.txt"
            out_path = os.path.join(PROCESSED_DIR, out_name)
            
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(text.strip())
            print(f"✅ Guardado en processed: {out_name}")

if __name__ == "__main__":
    process_unstructured_documents()