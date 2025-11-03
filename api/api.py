from flask import Flask, request, jsonify
from flask_cors import CORS
import ia.recomendacion_anime as ra
from ia.script import procesar_recomendaciones
import pandas as pd 
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


RAIZ = os.path.dirname(os.path.dirname(__file__))  # sube dos niveles desde /api/api.py
RUTA_CSV = os.path.join(RAIZ, 'anime_with_images.csv')

@app.route('/api/estado', methods=['GET'])
def estado_check():
    return jsonify({
        "status": "active",
        "service": "Anime Recommendation API"
    })

@app.route('/api/entrenar', methods=['POST'])
def entrenar_modelo():
    data = request.get_json()
    print(data)

    if not data or 'ratings' not in data:
        return jsonify({"error": "Se requieren ratings"}), 400

    user_ratings = data['ratings']

    try:
        recomendaciones = ra.trainingRecommendation(user_ratings, True)
        return jsonify({"recomendaciones": recomendaciones})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recomendar', methods=['POST'])
def obtener_recomendaciones():
    data = request.get_json()
    print(data)

    if not data or 'ratings' not in data:
        return jsonify({"error": "Se requieren ratings"}), 400

    user_ratings = data['ratings']

    try:
        recomendaciones = ra.trainingRecommendation(user_ratings)

        # Ejecutar el script con las recomendaciones
        recomendaciones = list(recomendaciones)[:10]
        procesar_recomendaciones(recomendaciones)
        anime_img = pd.read_csv(RUTA_CSV, encoding='utf-8', usecols=range(2))


        return jsonify({"recomendaciones": anime_img.to_dict(orient='records')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/probar', methods=['GET'])
def probar_algoritmo():
    test_case = {}
    return jsonify({
        "test_case": test_case,
        "message": "Prueba recibida - ejecutando caso de prueba",
        "status": "success"
    })

@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(405)
def metodo_no_permitido(error):
    return jsonify({"error": "Método no permitido"}), 405

@app.errorhandler(500)
def error_interno(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    print(" Servidor API iniciado")
    print("  Endpoints disponibles:")
    print("   GET  /api/estado")
    print("   POST /api/entrenar") 
    print("   POST /api/recomendar")
    print("   GET  /api/probar")
    print("\n🌐 Servidor corriendo en: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)