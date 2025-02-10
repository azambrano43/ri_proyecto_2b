from flask import Flask, request, render_template
from model import handle_query

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = ""
    contexto = ""

    if request.method == 'POST':
        consulta_usuario = request.form.get('consulta')

        try:
            respuesta, contexto = handle_query(consulta_usuario)
        except Exception as e:
            respuesta = "Hubo un error procesando tu consulta. Intenta nuevamente."
            contexto = f"Error técnico: {str(e)}"

    return render_template('index.html', respuesta=respuesta, contexto=contexto)

if __name__ == '__main__':
    app.run(debug=True)
