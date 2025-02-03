import os
import chromadb

# Obtener la ruta absoluta del directorio del proyecto
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ruta absoluta a la base de datos
DB_PATH = os.path.join(ROOT_DIR, "db")

# Conectar a ChromaDB
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection("entrevistas")

def buscar_documentos(embedding_query, top_k=3):
    """ 
    Realiza una consulta en la base de datos vectorial 
    """
    return collection.query(query_embeddings=[embedding_query], n_results=top_k)