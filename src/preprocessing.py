import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# Inicializar herramientas de NLP
stemmer = SnowballStemmer("spanish")
stop_words = set(stopwords.words('spanish'))
puntuaciones = string.punctuation + "¿¡"

def preprocesar_texto(texto):
    """ 
    Preprocesa el texto: minúsculas, sin puntuación, sin stopwords, stemming 
    """
    texto = texto.lower()
    texto = "".join([char for char in texto if char not in puntuaciones and not char.isdigit()])
    tokens = word_tokenize(texto)
    return " ".join(stemmer.stem(t) for t in tokens if t not in stop_words)