import streamlit as st
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

st.set_page_config(
    page_title="RAG Local",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; }
        h1 { font-size: 1.4rem !important; font-weight: 600; color: #111; }

        .respuesta-box {
            background: #f7f9fc;
            border-left: 3px solid #2563eb;
            border-radius: 4px;
            padding: 0.9rem 1.1rem;
            margin: 0.5rem 0 1.5rem 0;
            font-size: 0.97rem;
            color: #1a1a1a;
            line-height: 1.6;
        }
        .fragmento-box {
            background: #fafafa;
            border: 1px solid #e5e7eb;
            border-radius: 4px;
            padding: 0.8rem 1rem;
            margin-bottom: 0.6rem;
            font-size: 0.88rem;
            color: #374151;
            line-height: 1.6;
        }
        .score-badge {
            display: inline-block;
            background: #eff6ff;
            color: #2563eb;
            border-radius: 10px;
            padding: 1px 8px;
            font-size: 0.75rem;
            font-weight: 500;
            margin-left: 8px;
        }
        .historial-item {
            border-left: 2px solid #d1d5db;
            padding: 0.4rem 0.75rem;
            margin-bottom: 0.5rem;
            font-size: 0.85rem;
            color: #6b7280;
        }
        .historial-pregunta {
            font-weight: 600;
            color: #111;
            margin-bottom: 0.2rem;
        }
        section[data-testid="stSidebar"] {
            background-color: #111827;
        }
        section[data-testid="stSidebar"] * {
            color: #d1d5db !important;
        }
        section[data-testid="stSidebar"] hr {
            border-color: #374151 !important;
        }
    </style>
""", unsafe_allow_html=True)

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

if "historial" not in st.session_state:
    st.session_state.historial = []

with st.sidebar:
    st.markdown("### RAG Local")
    st.divider()
    st.markdown("**Modelo**")
    st.markdown("llama3.1 via Ollama")
    st.markdown("**Embeddings**")
    st.markdown("nomic-embed-text")
    st.markdown("**Vector store**")
    st.markdown("ChromaDB (persistente)")
    st.divider()
    st.markdown("**Corpus**")
    st.markdown("rag.txt  \nchromadb.txt  \npython.txt")

st.title("Sistema RAG — consulta sobre documentos")

pregunta = st.text_input(
    "",
    placeholder="Escribe una pregunta sobre los documentos...",
    label_visibility="collapsed"
)

if pregunta:
    with st.spinner("Buscando..."):
        query_engine = index.as_query_engine(
            llm=llm,
            similarity_top_k=3
        )
        respuesta = query_engine.query(pregunta)

    st.markdown(f'<div class="respuesta-box">{str(respuesta)}</div>', unsafe_allow_html=True)

    with st.expander("Fragmentos recuperados"):
        for i, nodo in enumerate(respuesta.source_nodes):
            score = round(nodo.score, 3)
            st.markdown(
                f'<div class="fragmento-box"><strong>Fragmento {i+1}</strong>'
                f'<span class="score-badge">{score}</span><br><br>{nodo.text}</div>',
                unsafe_allow_html=True
            )

    st.session_state.historial.insert(0, {
        "pregunta": pregunta,
        "respuesta": str(respuesta)
    })

if len(st.session_state.historial) > 1:
    st.divider()
    st.markdown("**Historial**")
    for item in st.session_state.historial[1:]:
        st.markdown(f"""
        <div class="historial-item">
            <div class="historial-pregunta">{item['pregunta']}</div>
            {item['respuesta']}
        </div>
        """, unsafe_allow_html=True)