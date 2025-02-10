from transformers import T5ForConditionalGeneration, T5Tokenizer
from sentence_transformers import SentenceTransformer
from database import buscar_documentos
from preprocessing import preprocesar_texto

# Cargar modelos
modelo_t5 = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")
tokenizer_t5 = T5Tokenizer.from_pretrained("google/flan-t5-large", legacy=False)
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

def handle_query(user_query):
    """ 
    Procesa una consulta del usuario, busca en ChromaDB y genera una respuesta precisa y concisa con T5.
    Devuelve la respuesta generada junto con el contexto utilizado.
    """
    processed_query = preprocesar_texto(user_query)
    embedding_query = modelo_embeddings.encode(processed_query)
    resultados = buscar_documentos(embedding_query)

    if not resultados:
        return "No encontré información relevante.", "No se encontró contexto relevante."
    
    # Construcción del contexto utilizando solo la información más relevante
    contexto = "\n\n".join([
        f"Documento {i+1}: {item['documento'][:300]}...\nMetadatos: {', '.join([f'{k}: {v}' for k, v in item['metadatos'].items()])}" 
        for i, item in enumerate(resultados)
    ])
    
    if not contexto.strip():
        contexto = "No se encontró contexto relevante."

    
    # Instrucción optimizada para respuestas más precisas
    entrada = (
        f"Responde con precisión a la siguiente pregunta basándote en el contexto proporcionado."
        f"\n\nPregunta: {user_query}\n\nContexto: {contexto}\n\n"
        "Proporciona una respuesta clara y directa sin añadir información innecesaria."
    )

    # Generar respuesta con mayor precisión
    inputs = tokenizer_t5(entrada, return_tensors="pt", max_length=1024, truncation=True)
    output = modelo_t5.generate(
        **inputs, max_length=250, min_length=50, num_beams=5, do_sample=False, length_penalty=1.2, repetition_penalty=1.1
    )
    respuesta = tokenizer_t5.decode(output[0], skip_special_tokens=True)
    
    return respuesta, contexto
