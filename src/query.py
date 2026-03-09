from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import chromadb

def main():

    # Conectar con ChromaDB
    db = chromadb.PersistentClient(path="chroma_db")
    chroma_collection = db.get_or_create_collection("rag_collection")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Embeddings
    embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # LLM
    llm = Ollama(model="llama3.1")

    # Cargar índice
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model
    )

    query_engine = index.as_query_engine(llm=llm)

    pregunta = input("Haz una pregunta: ")

    respuesta = query_engine.query(pregunta)

    print("\nRespuesta:")
    print(respuesta)


if __name__ == "__main__":
    main()
