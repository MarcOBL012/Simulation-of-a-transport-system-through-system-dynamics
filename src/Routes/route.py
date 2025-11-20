from flask import render_template, make_response, request, jsonify
from src.Controllers.controller import controller, simulate_new_run

def modelRoute(app):
    @app.route('/', methods=['GET'])
    def home():
        response = controller()
        
        # Verificación de errores simplificada
        if isinstance(response, list) and 'message' in response[0]:
             return render_template('error.html', error_message=response)
        
        if isinstance(response, dict) and 'niveles' in response:
             respuesta = make_response(render_template('template.html', 
                                                       nivel=response['niveles'], 
                                                       constantes=response['constantes']))
             respuesta.headers['Cache-Control'] = 'public, max-age=180'
             return respuesta
             
        return render_template('error.html', error_message=[{'message': 'Error desconocido en respuesta del controlador'}])

    # Nueva ruta para la simulación dinámica
    @app.route('/simulate', methods=['POST'])
    def simulate():
        data = request.get_json()
        result = simulate_new_run(data)
        return jsonify(result)