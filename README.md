# Proyecto RAG

Este proyecto implementa un sistema básico de **Retrieval Augmented Generation (RAG)** utilizando Python.

El objetivo es permitir hacer preguntas sobre documentos almacenados en el proyecto y generar respuestas basadas en ese contenido.

## Tecnologías utilizadas

- Python
- LlamaIndex
- ChromaDB
- Ollama

## Estructura del proyecto

```
Proyecto-RAG
│
├── data
│   └── documentos de ejemplo
│
├── src
│   ├── ingest.py
│   └── query.py
│
├── requirements.txt
└── .gitignore
```

## Instalación

Clonar el repositorio:

```
git clone https://github.com/sbc1303/Proyecto-RAG.git
cd Proyecto-RAG
```

Crear entorno virtual:

```
python -m venv venv
source venv/bin/activate
```

Instalar dependencias:

```
pip install -r requirements.txt
```

## Uso

Indexar los documentos:

```
python src/ingest.py
```

Ejecutar el sistema de preguntas:

```
python src/query.py
```

Ejemplo de pregunta:

```
¿Qué es un sistema RAG?
```
