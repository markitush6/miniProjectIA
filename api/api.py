from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/estado', methods=['GET'])
def estado_check():
    """Verificar estado del servicio"""
    return jsonify({
        "status": "active",
        "service": "Anime Recommendation API"
    })

@app.route('/api/entrenar', methods=['POST'])
def entrenar_modelo():
    """
    Endpoint para entrenar el algoritmo
    """
    return jsonify({
        "message": "Solicitud de entrenamiento recibida",
        "status": "success"
    })

@app.route('/api/recomendar', methods=['POST'])
def obtener_recomendaciones():
    """
    Obtener recomendaciones basadas en ratings
    """
    data = request.get_json()
    
    if not data or 'ratings' not in data:
        return jsonify({"error": "Se requieren ratings"}), 400
    
    user_ratings = data['ratings']
    
    # Validaciones básicas
    if not isinstance(user_ratings, dict):
        return jsonify({"error": "Los ratings deben ser un objeto JSON"}), 400
    
    if len(user_ratings) == 0:
        return jsonify({"error": "Se requiere al menos un rating"}), 400
    
    return jsonify({
        "message": "Solicitud de recomendaciones recibida",
        "ratings_recibidos": user_ratings,
        "status": "success"
    })

@app.route('/api/probar', methods=['GET'])
def probar_algoritmo():
    """
    Probar el algoritmo con caso de prueba
    """
    test_case = {
        # "Hunter x Hunter (2011)": 10,
        # "School Days": 1
    }
    
    return jsonify({
        "test_case": test_case,
        "message": "Prueba recibida - ejecutando caso de prueba",
        "status": "success"
    })

# Manejo de errores
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