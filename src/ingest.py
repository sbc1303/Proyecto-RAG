from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
import chromadb

def main():

    # Leer documentos
    documents = SimpleDirectoryReader("data").load_data()

    # Conectar con ChromaDB
    db = chromadb.PersistentClient(path="chroma_db")
    chroma_collection = db.get_or_create_collection("rag_collection")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Modelo de embeddings
    embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # Crear índice vectorial
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model
    )

    print("Indexación completada")
    print(f"Documentos procesados: {len(documents)}")

if __name__ == "__main__":
    main()
