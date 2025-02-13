from transformers import T5ForConditionalGeneration, T5Tokenizer
from sentence_transformers import SentenceTransformer
from database import buscar_documentos
from preprocessing import preprocesar_texto

# Cargar modelos de procesamiento de lenguaje natural
# - T5 para generación de texto
# - SentenceTransformer para embeddings semánticos
modelo_t5 = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
tokenizer_t5 = T5Tokenizer.from_pretrained("google/flan-t5-base", legacy=False)
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

def handle_query(user_query):
    """ 
    Procesa una consulta del usuario, busca en ChromaDB y genera una respuesta precisa y concisa con T5.
    
    Pasos:
    1. Preprocesa la consulta del usuario.
    2. Convierte la consulta en un embedding semántico.
    3. Busca documentos relevantes en la base de datos ChromaDB.
    4. Construye un contexto basado en los documentos encontrados.
    5. Genera una respuesta con el modelo T5 utilizando el contexto.
    6. Retorna la respuesta generada y el contexto utilizado.
    
    Parámetros:
    - user_query (str): Consulta ingresada por el usuario.
    
    Retorna:
    - respuesta (str): Respuesta generada por el modelo T5.
    - contexto (str): Fragmentos de documentos utilizados para generar la respuesta.
    """
    # Preprocesamiento de la consulta del usuario (normalización y limpieza del texto)
    processed_query = preprocesar_texto(user_query)
    
    # Generación de embeddings semánticos a partir de la consulta procesada
    embedding_query = modelo_embeddings.encode(processed_query)
    
    # Búsqueda de documentos relevantes en la base de datos ChromaDB
    resultados = buscar_documentos(embedding_query)

    # Si no se encuentran resultados relevantes, devolver un mensaje genérico
    if not resultados:
        return "No encontré información relevante.", "No se encontró contexto relevante."
    
    # Construcción del contexto utilizando los documentos más relevantes
    contexto = "\n\n".join([
        f"Documento {i+1}: {item['documento'][:300]}...\nMetadatos: {', '.join([f'{k}: {v}' for k, v in item['metadatos'].items()])}" 
        for i, item in enumerate(resultados)
    ])
    
    # En caso de que el contexto esté vacío, establecer un mensaje predeterminado
    if not contexto.strip():
        contexto = "No se encontró contexto relevante."

    # Construcción de la entrada para el modelo T5, proporcionando la pregunta y el contexto relevante
    entrada = (
        f"Responde con precisión a la siguiente pregunta basándote en el contexto proporcionado."
        f"\n\nPregunta: {user_query}\n\nContexto: {contexto}\n\n"
        "Proporciona una respuesta clara y directa sin añadir información innecesaria."
    )

    # Tokenización de la entrada para ajustarse a los requerimientos del modelo T5
    inputs = tokenizer_t5(entrada, return_tensors="pt", max_length=1024, truncation=True)
    
    # Generación de la respuesta utilizando T5 con configuración de hiperparámetros optimizados
    output = modelo_t5.generate(
        **inputs, max_length=250, min_length=50, num_beams=5, do_sample=False, length_penalty=1.2, repetition_penalty=1.1
    )
    
    # Decodificación de la respuesta generada eliminando tokens especiales
    respuesta = tokenizer_t5.decode(output[0], skip_special_tokens=True)
    
    return respuesta, contexto
