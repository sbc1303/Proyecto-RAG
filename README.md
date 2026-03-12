🇪🇸 [Español](#proyecto-rag) | 🇬🇧 [English](#rag-project)

---

# Proyecto RAG

Proyecto que tiene como fin crear un sistema de preguntas sobre documentos propio basado en **Retrieval Augmented Generation (RAG)**. Este proyecto está construido completamente en un entorno local sin depender de ninguna API externa.

Este sistema permite cargar documentos de texto, que se encuentran indexados mediante embeddings semánticos para generar respuestas combinando los fragmentos que más coinciden con las preguntas que se realizan.

## Tecnologías

| Herramienta | Versión | Función |
|-------------|---------|---------|
| [Ollama](https://ollama.com) | latest | Ejecución local de LLMs y embeddings |
| [LlamaIndex](https://www.llamaindex.ai) | 0.14.15 | Gestión de flujo entre los documentos y el modelo |
| [ChromaDB](https://www.trychroma.com) | 1.5.2 | Base de datos vectorial |
| [Streamlit](https://streamlit.io) | 1.54.0 | Interfaz web |

## Requisitos del sistema

- Python 3.11 o superior (se recomienda Python 3.11 para más estabilidad)
- Mínimo 8 GB de RAM (los modelos pequeños ocupan entre 2 y 5 GB)
- Espacio en disco: ~5 GB para los modelos

## Requisitos previos — Ollama

Este proyecto necesita Ollama instalado y dos modelos descargados antes de poder ejecutarse.

### Instalación de Ollama

**Mac:**
Descarga el instalador desde [ollama.com](https://ollama.com) y sigue el asistente de instalación. Una vez instalado, Ollama corre en segundo plano como un servicio.

**Windows:**
Descarga el instalador `.exe` desde [ollama.com](https://ollama.com). Requiere Windows 10 o superior. Tras la instalación, Ollama estará disponible desde la terminal.

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Descarga de modelos

Con Ollama instalado, descarga los dos modelos necesarios. El proceso puede tardar varios minutos dependiendo de la conexión:
```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

Puedes verificar que están disponibles con:
```bash
ollama list
```

## Instalación del proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/sbc1303/Proyecto-RAG.git
cd Proyecto-RAG
```

### 2. Crear el entorno virtual

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Una vez activado, el prompt del terminal mostrará `(venv)` al inicio.

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Estructura del proyecto
```
Proyecto-RAG
│
├── data
│   ├── rag.txt           # Qué es RAG y cómo funciona
│   ├── chromadb.txt      # Qué es ChromaDB y búsqueda vectorial
│   └── python.txt        # Python en el ecosistema de IA
│
├── src
│   ├── ingest.py         # Indexa los documentos en ChromaDB
│   ├── query.py          # Consultas por terminal
│   └── app.py            # Interfaz web con Streamlit
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Uso

> **Importante:** Se deben ejecutar siempre los comandos desde la raíz del proyecto (`Proyecto-RAG/`). Si no se realiza de esta forma, no se podrán encontrar las demás rutas relativas (`data/` y `chroma_db/`).

### Paso 1 — Indexar los documentos

En este paso se leen los archivos de `data/`, se generan los embeddings y estos embeddings se guardan en ChromaDB. Solo es necesario ejecutarlo en la primera ejecución o cuando se modifiquen los documentos.
```bash
python src/ingest.py
```

Si todo va bien, se verá:
```
Indexación completada
Documentos procesados: 3
```

### Paso 2 — Lanzar la interfaz web
```bash
streamlit run src/app.py
```

Se abrirá automáticamente en el navegador en `http://localhost:8501`. La primera carga puede tardar unos segundos mientras el modelo se inicializa.

### Alternativa — Modo terminal

Para realizar una consulta de manera directa a través de terminal:
```bash
python src/query.py
```

## Reindexar documentos

Si se modifica algún archivo de `data/`, es necesario borrar la base de datos vectorial existente y volver a indexar. Si no se realiza este paso, ChromaDB seguirá usando los embeddings antiguos y las respuestas no reflejarán los cambios.

**Mac/Linux:**
```bash
rm -rf chroma_db
python src/ingest.py
```

**Windows:**
```bash
rmdir /s /q chroma_db
python src/ingest.py
```

## Añadir documentos propios

Para usar el sistema con documentos propios, copiar los archivos con extensión `.txt` en la carpeta `data/` y reindexar siguiendo los pasos anteriores. Este sistema admite múltiples archivos y los procesa todos de manera automática.

## Solución de problemas frecuentes

**`ingest.py` falla al arrancar**
Asegurar que Ollama está corriendo y se ha descargado el modelo `nomic-embed-text` con `ollama pull nomic-embed-text`.

**Las respuestas mezclan información incorrecta**
Probablemente sea debido a que ChromaDB tiene embeddings de una versión anterior de los documentos. Se debe borrar la carpeta `chroma_db/` y reindexar.

**Streamlit no abre el navegador automáticamente**
Abrir de manera manual `http://localhost:8501` en el navegador.

---

# RAG Project

A local question-answering system built on **Retrieval Augmented Generation (RAG)**. This project runs entirely in a local environment with no dependency on external APIs.

The system loads text documents, indexes them using semantic embeddings, and generates answers by combining the most relevant fragments for each question.

## Technologies

| Tool | Version | Purpose |
|------|---------|---------|
| [Ollama](https://ollama.com) | latest | Local LLM and embedding execution |
| [LlamaIndex](https://www.llamaindex.ai) | 0.14.15 | Document-to-model pipeline management |
| [ChromaDB](https://www.trychroma.com) | 1.5.2 | Vector database |
| [Streamlit](https://streamlit.io) | 1.54.0 | Web interface |

## System Requirements

- Python 3.11 or higher (Python 3.11 recommended for stability)
- At least 8 GB RAM (small models use between 2 and 5 GB)
- Disk space: ~5 GB for models

## Prerequisites — Ollama

This project requires Ollama to be installed and two models downloaded before running.

### Installing Ollama

**Mac:**
Download the installer from [ollama.com](https://ollama.com) and follow the setup wizard. Once installed, Ollama runs as a background service.

**Windows:**
Download the `.exe` installer from [ollama.com](https://ollama.com). Requires Windows 10 or higher. After installation, Ollama will be available from the terminal.

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Downloading Models

With Ollama installed, download the two required models. This may take several minutes depending on your connection:
```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

You can verify they are available with:
```bash
ollama list
```

## Project Setup

### 1. Clone the repository
```bash
git clone https://github.com/sbc1303/Proyecto-RAG.git
cd Proyecto-RAG
```

### 2. Create a virtual environment

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Once activated, the terminal prompt will show `(venv)` at the beginning.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Project Structure
```
Proyecto-RAG
│
├── data
│   ├── rag.txt           # What RAG is and how it works
│   ├── chromadb.txt      # What ChromaDB is and vector search
│   └── python.txt        # Python in the AI ecosystem
│
├── src
│   ├── ingest.py         # Indexes documents into ChromaDB
│   ├── query.py          # Terminal-based queries
│   └── app.py            # Streamlit web interface
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Usage

> **Important:** All commands must be run from the project root (`Proyecto-RAG/`). Otherwise, relative paths (`data/` and `chroma_db/`) will not be found.

### Step 1 — Index the documents

This step reads the files in `data/`, generates embeddings, and stores them in ChromaDB. Only needs to be run on the first execution or when documents are modified.
```bash
python src/ingest.py
```

If successful, you will see:
```
Indexación completada
Documentos procesados: 3
```

### Step 2 — Launch the web interface
```bash
streamlit run src/app.py
```

The browser will open automatically at `http://localhost:8501`. The first load may take a few seconds while the model initialises.

### Alternative — Terminal mode

To query the system directly from the terminal:
```bash
python src/query.py
```

## Re-indexing Documents

If any file in `data/` is modified, the existing vector database must be deleted and re-indexed. Otherwise, ChromaDB will keep using the old embeddings and responses will not reflect the changes.

**Mac/Linux:**
```bash
rm -rf chroma_db
python src/ingest.py
```

**Windows:**
```bash
rmdir /s /q chroma_db
python src/ingest.py
```

## Using Your Own Documents

To use the system with your own documents, copy `.txt` files into the `data/` folder and re-index following the steps above. The system supports multiple files and processes them all automatically.

## Troubleshooting

**`ingest.py` fails on startup**
Make sure Ollama is running and the `nomic-embed-text` model has been downloaded with `ollama pull nomic-embed-text`.

**Responses mix incorrect information**
ChromaDB likely has embeddings from an older version of the documents. Delete the `chroma_db/` folder and re-index.

**Streamlit does not open the browser automatically**
Open `http://localhost:8501` manually in your browser.
