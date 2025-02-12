import string
from nltk.tokenize import word_tokenize  # Para dividir el texto en palabras (tokens)
from nltk.corpus import stopwords  # Para eliminar palabras irrelevantes (stopwords)
from nltk.stem.snowball import SnowballStemmer  # Para reducir las palabras a su raíz (stemming)

# Inicialización de herramientas de Procesamiento de Lenguaje Natural (NLP)
stemmer = SnowballStemmer("spanish")  # Algoritmo de stemming para español
stop_words = set(stopwords.words('spanish'))  # Conjunto de stopwords en español
puntuaciones = string.punctuation + "¿¡"  # Caracteres de puntuación a eliminar

def preprocesar_texto(texto):
    """ 
    Función para preprocesar el texto antes de su análisis.

    Pasos realizados:
    1. Convertir el texto a minúsculas.
    2. Eliminar caracteres de puntuación y números.
    3. Tokenizar el texto (dividirlo en palabras).
    4. Eliminar palabras vacías (stopwords).
    5. Aplicar stemming a cada palabra (reducirlas a su raíz).

    Parámetros:
    texto (str): Texto de entrada en español.

    Retorna:
    str: Texto preprocesado con palabras en su raíz, sin stopwords ni puntuación.
    """

    # Convertir el texto a minúsculas para normalizarlo
    texto = texto.lower()

    # Eliminar puntuaciones y números del texto
    texto = "".join([char for char in texto if char not in puntuaciones and not char.isdigit()])

    # Tokenizar el texto, dividiéndolo en palabras
    tokens = word_tokenize(texto)

    # Aplicar stemming y eliminar stopwords
    tokens_procesados = [stemmer.stem(t) for t in tokens if t not in stop_words]

    # Unir los tokens procesados en una cadena de texto
    return " ".join(tokens_procesados)
