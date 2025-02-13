from model import handle_query

if __name__ == "__main__":
    
    consulta_usuario = "¿Qué candidato presidencial habla mucho más sobre reducir la delincuencia?"

    # Obtener respuesta y contexto
    respuesta, contexto = handle_query(consulta_usuario)

    print("Contexto utilizado:\n", contexto)
    print("\nRespuesta generada:\n", respuesta)
