from transformers import T5ForConditionalGeneration, T5Tokenizer
from sentence_transformers import SentenceTransformer
from database import buscar_documentos
from preprocessing import preprocesar_texto

# Cargar modelos
modelo_t5 = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")
tokenizer_t5 = T5Tokenizer.from_pretrained("google/flan-t5-large")
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

def handle_query(user_query):
    """ 
    Procesa una consulta del usuario, busca en ChromaDB y genera una respuesta con T5.
    Cada documento se asocia con su respectivo metadato.
    """
    processed_query = preprocesar_texto(user_query)
    embedding_query = modelo_embeddings.encode(processed_query)
    resultados = buscar_documentos(embedding_query)

    if not resultados["documents"] or not resultados["documents"][0]:
        return "No encontré información relevante."

    documentos = resultados["documents"][0]
    metadatos = resultados["metadatas"][0]

    # Construir el contexto asociando cada documento con su metadato correspondiente
    contexto = "\n\n".join([f"Documento {i+1}: {doc}\nMetadatos: {meta}" for i, (doc, meta) in enumerate(zip(documentos, metadatos))])
    
    # Instrucción simple que incluye contexto y la pregunta del usuario 
    entrada = f"Pregunta: {user_query} Contexto: {contexto}"

    # Generar respuesta con T5
    inputs = tokenizer_t5(entrada, return_tensors="pt", max_length=512, truncation=True)
    output = modelo_t5.generate(**inputs, max_length=150)
    
    return tokenizer_t5.decode(output[0], skip_special_tokens=True)
