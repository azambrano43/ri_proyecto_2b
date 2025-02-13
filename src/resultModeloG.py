from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

# Respuesta generada por el modelo
respuesta_generada = """Metadatos: candidato: Daniel Noboa, descripción: El conversatorio abordó temas clave como democracia y participación ciudadana, 
destacando la importancia del voto informado y la necesidad de fortalecer la institucionalidad. En seguridad, se discutieron la sobrepoblación carcelaria, 
el uso de cárceles barcazas, la reforma del SNAI y la implementación del plan Fénix con tecnología e inteligencia. En economía y empleo, se planteó la 
creación de empleo de calidad, el impulso a sectores estratégicos como la industria 4.0 y la"""

# Respuesta esperada
respuesta_esperada = """Daniel Noboa ha abordado temas clave como democracia y participación ciudadana, destacando la importancia del voto informado 
y la necesidad de fortalecer la institucionalidad. En seguridad, ha discutido la sobrepoblación carcelaria, el uso de cárceles barcazas, la reforma del 
SNAI y la implementación del plan Fénix con tecnología e inteligencia. En economía y empleo, ha planteado la creación de empleo de calidad, 
el impulso a sectores estratégicos como la industria 4.0 y la infraestructura. También ha tratado la atracción de inversión extranjera, la competitividad, 
la reducción de costos en electricidad y combustibles, y la diferenciación entre gasto e inversión."""

# Tokenizar las respuestas
referencia = [respuesta_esperada.split()]
respuesta_tokens = respuesta_generada.split()

# Calcular BLEU Score
bleu_score = sentence_bleu(referencia, respuesta_tokens)

# Calcular ROUGE-L Score
rouge = Rouge()
scores = rouge.get_scores(respuesta_generada, respuesta_esperada)
rouge_l_score = scores[0]['rouge-l']['f']

# Mostrar los resultados
print("BLEU Score:", bleu_score)
print("ROUGE-L Score:", rouge_l_score)
