#import os
from model import handle_query

if __name__ == "__main__":
    
    consulta_usuario = "¿Qué candidato presidencial habla más sobre reducir la delincuencia?"

    # Obtener respuesta
    respuesta = handle_query(consulta_usuario)

    print("Respuesta generada:\n", respuesta)
