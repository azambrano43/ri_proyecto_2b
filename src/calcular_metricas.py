# calcular_metricas.py

# Importar métricas de evaluación desde scikit-learn
from sklearn.metrics import precision_score, recall_score, f1_score
from datos_prueba import DATOS_PRUEBA

def calcular_metricas(y_true, y_pred):
    """
    Calcula las métricas de evaluación de desempeño del modelo: precisión, recall y F-score.
    
    Parámetros:
    - y_true (list): Lista de valores verdaderos esperados (ground truth).
    - y_pred (list): Lista de valores predichos por el modelo.
    
    Retorna:
    - dict: Diccionario con los valores de precisión, recall y F-score redondeados a 3 decimales.
    """
    precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    
    return {
        'Precision': round(precision, 3),
        'Recall': round(recall, 3),
        'F-score': round(f1, 3)
    }

def evaluar_respuesta(respuesta_generada, respuesta_esperada):
    """
    Evalúa la calidad de la respuesta generada comparándola con la respuesta esperada.
    
    Parámetros:
    - respuesta_generada (str): Texto generado por el modelo.
    - respuesta_esperada (str): Respuesta correcta esperada.
    
    Retorna:
    - dict: Métricas de evaluación (precisión, recall, F-score).
    """
    palabras_esperadas = set(respuesta_esperada.lower().split())
    palabras_generadas = set(respuesta_generada.lower().split())

    # Crear listas de etiquetas binarias indicando presencia de palabras esperadas en la respuesta generada
    y_true = [1 if palabra in palabras_esperadas else 0 for palabra in palabras_generadas]
    y_pred = [1] * len(y_true)  # Se asume que todas las palabras generadas son relevantes

    return calcular_metricas(y_true, y_pred)

def calcular_todas_las_metricas():
    """
    Calcula las métricas de evaluación para todas las consultas almacenadas en DATOS_PRUEBA.
    
    Itera sobre las consultas de prueba, evaluando las respuestas generadas en comparación con las respuestas esperadas.
    
    Retorna:
    - dict: Diccionario con las métricas de cada consulta, incluyendo las respuestas esperadas y generadas.
    """
    metricas_calculadas = {}
    for query, data in DATOS_PRUEBA.items():
        metricas = evaluar_respuesta(data["respuesta_generada"], data["respuesta_esperada"])
        metricas_calculadas[query] = {
            "respuesta_generada": data["respuesta_generada"],
            "respuesta_esperada": data["respuesta_esperada"],
            "Precision": metricas["Precision"],
            "Recall": metricas["Recall"],
            "F-score": metricas["F-score"]
        }
    return metricas_calculadas
