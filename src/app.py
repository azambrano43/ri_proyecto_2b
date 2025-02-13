# Importar las librerías necesarias para el servidor Flask
from flask import Flask, request, render_template
from model import handle_query  # Importar la función que maneja las consultas del usuario
from calcular_metricas import calcular_todas_las_metricas  # Importar la función que calcula las métricas

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Ruta principal de la aplicación web.
    
    Funcionalidad:
    - Muestra un formulario donde el usuario puede ingresar una consulta.
    - Si la consulta es enviada mediante POST, se procesa con `handle_query`.
    - Calcula métricas de evaluación utilizando datos predefinidos de prueba.
    - Renderiza la página HTML con la respuesta generada, el contexto y las métricas.
    
    Métodos soportados:
    - GET: Carga la página con los valores iniciales.
    - POST: Procesa la consulta ingresada y muestra la respuesta.
    
    Retorna:
    - render_template: Renderiza `index.html` con los datos procesados.
    """
    respuesta = ""
    contexto = ""
    metricas = calcular_todas_las_metricas()  # Calcular métricas al cargar la web

    if request.method == 'POST':
        consulta_usuario = request.form.get('consulta')  # Obtener la consulta ingresada por el usuario

        try:
            respuesta, contexto = handle_query(consulta_usuario)  # Procesar la consulta con el modelo
        except Exception as e:
            respuesta = "Hubo un error procesando tu consulta. Intenta nuevamente."
            contexto = f"Error técnico: {str(e)}"

    return render_template('index.html', respuesta=respuesta, contexto=contexto, metricas=metricas)

if __name__ == '__main__':
    # Ejecutar la aplicación en modo de depuración
    app.run(debug=True)
