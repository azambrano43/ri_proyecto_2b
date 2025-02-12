import os
import chromadb
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from preprocessing import preprocesar_texto

# Cargar el modelo de embeddings para convertir textos en representaciones numéricas
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

# Obtener la ruta absoluta del directorio del proyecto
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Definir la ruta absoluta a la base de datos de ChromaDB
DB_PATH = os.path.join(ROOT_DIR, "db")

# Conectar a ChromaDB para almacenar y recuperar documentos
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection("entrevistas")

def buscar_documentos(embedding_query, consulta_original=None, top_k=3):
    """ 
    Realiza una consulta en la base de datos vectorial y devuelve los fragmentos más relevantes.
    
    Parámetros:
    - embedding_query (array): Embedding de la consulta generada.
    - consulta_original (str, opcional): Texto original de la consulta del usuario.
    - top_k (int): Número de documentos relevantes a recuperar.
    
    Retorna:
    - contexto (list): Lista de diccionarios con los fragmentos más relevantes y sus metadatos.
    """
    resultados = collection.query(query_embeddings=[embedding_query], n_results=top_k)
    
    if not resultados.get("documents") or not resultados["documents"][0]:
        return []
    
    documentos_filtrados = (
        [extraer_fragmento_mas_relevante(doc, embedding_query, consulta_original)
        for doc in resultados["documents"][0]]
        if consulta_original else resultados["documents"][0]
    )
    
    documentos_filtrados = [doc if doc.strip() else "Información no disponible." for doc in documentos_filtrados]
    metadatos = resultados.get("metadatas", [{}])[0]
    
    # Construcción del contexto estructurado con los documentos recuperados
    contexto = [
        {
            "documento": doc,
            "metadatos": meta if isinstance(meta, dict) else {"info": str(meta)}
        }
        for doc, meta in zip(documentos_filtrados, metadatos)
    ]
    
    return contexto

def extraer_fragmento_mas_relevante(texto, embedding_query, consulta_original, umbral_similitud=0.2):
    """
    Extrae los fragmentos más relevantes de un documento en función de la similitud semántica y palabras clave.
    
    Parámetros:
    - texto (str): Documento de origen.
    - embedding_query (array): Embedding de la consulta.
    - consulta_original (str): Consulta original del usuario.
    - umbral_similitud (float): Valor mínimo de relevancia para incluir fragmentos.
    
    Retorna:
    - fragmento_final (str): Texto más relevante extraído del documento.
    """
    if not texto.strip():
        return "No hay información relevante."
    
    # Dividir el texto en fragmentos de oraciones
    oraciones = re.split(r'(?<=[.!?]) +', texto)
    fragmentos = [" ".join(oraciones[i:i+3]) for i in range(0, len(oraciones), 3)]
    
    fragmentos_relevantes = []
    for frag in fragmentos:
        sim = similitud_semantica(frag, embedding_query)
        keyword_score = calcular_relevancia_por_palabras_clave(frag, consulta_original)
        relevancia_total = (sim * 0.7) + (keyword_score * 0.3)
        
        if relevancia_total > umbral_similitud:
            fragmentos_relevantes.append((frag, relevancia_total))
    
    # Ordenar fragmentos según la relevancia descendente
    fragmentos_relevantes.sort(key=lambda x: x[1], reverse=True)
    
    # Retornar fragmentos más relevantes o una sección inicial si no hay coincidencias
    if not fragmentos_relevantes:
        return texto[:300] + "..."
    
    fragmento_final = " ".join([f[0] for f in fragmentos_relevantes[:2]])
    
    return fragmento_final if fragmento_final.strip() else "Información no disponible."

def similitud_semantica(texto, embedding_query):
    """
    Calcula la similitud semántica entre un fragmento de texto y la consulta.
    
    Parámetros:
    - texto (str): Texto del documento.
    - embedding_query (array): Embedding generado para la consulta.
    
    Retorna:
    - float: Valor de similitud entre el texto y la consulta.
    """
    embedding_texto = modelo_embeddings.encode([texto])
    return np.dot(embedding_texto, np.array(embedding_query).T).flatten()[0]

def calcular_relevancia_por_palabras_clave(texto, consulta_original):
    """
    Evalúa la relevancia del fragmento analizando la coincidencia de palabras clave.
    
    Parámetros:
    - texto (str): Fragmento a evaluar.
    - consulta_original (str): Consulta original del usuario.
    
    Retorna:
    - float: Proporción de palabras clave encontradas en el fragmento.
    """
    palabras_clave = set(preprocesar_texto(consulta_original).split())
    palabras_texto = set(preprocesar_texto(texto).split())
    return sum(1 for palabra in palabras_texto if palabra in palabras_clave) / max(len(palabras_clave), 1)
