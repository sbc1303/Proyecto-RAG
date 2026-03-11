import streamlit as st
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

st.set_page_config(page_title="RAG Local", page_icon="🔍")
st.title("Sistema de preguntas sobre documentos")
st.caption("Respuestas generadas a partir del corpus local usando Ollama + ChromaDB")

@st.cache_resource
def cargar_indice():
    db = chromadb.PersistentClient(path="chroma_db")
    chroma_collection = db.get_or_create_collection("rag_collection")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    llm = Ollama(model="llama3.1")
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model
    )
    return index, llm

index, llm = cargar_indice()

pregunta = st.text_input("¿Qué quieres saber?", placeholder="Escribe tu pregunta aquí...")

if pregunta:
    with st.spinner("Buscando en los documentos..."):
        query_engine = index.as_query_engine(
            llm=llm,
            similarity_top_k=3
        )
        respuesta = query_engine.query(pregunta)

    st.subheader("Respuesta")
    st.write(str(respuesta))

    with st.expander("Ver fragmentos recuperados"):
        for i, nodo in enumerate(respuesta.source_nodes):
            st.markdown(f"**Fragmento {i+1}** — similitud: `{round(nodo.score, 3)}`")
            st.info(nodo.text)
