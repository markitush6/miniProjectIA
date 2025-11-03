from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from config import get_db_connection
from flask_cors import CORS
import pandas as pd 
import os
import sys
RAIZ = os.path.dirname(os.path.dirname(__file__))  # sube dos niveles desde /api/api.py
sys.path.append(RAIZ)
RUTA_CSV = os.path.join(RAIZ, 'anime_with_images.csv')
from ia.script import procesar_recomendaciones
import ia.recomendacion_anime as ra

app = Flask(__name__)
app.secret_key = 'clave_secreta_animeworld_2024'  # Clave para las sesiones

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/estado', methods=['GET'])
def estado_check():
    return jsonify({
        "status": "active",
        "service": "Anime Recommendation API",
        "user_logged_in": session.get('logged_in', False)
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


@app.route('/api/login', methods=['POST'])
def login():
    """
    Endpoint de login - MODIFICADO para trabajar con formularios HTML
    """
    # Cambiamos a request.form para recibir datos del formulario HTML
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        # Redirigir con error si faltan campos
        return """
        <script>
            alert('Usuario y contraseña requeridos');
            window.history.back();
        </script>
        """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, nombre_usuario FROM usuarios WHERE nombre_usuario = %s AND password = %s"
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if usuario:
            # Login exitoso - guardar en sesión
            session['user_id'] = usuario[0]
            session['username'] = usuario[1]
            session['logged_in'] = True
            
            # Redirigir a la página principal
            return """
            <script>
                alert('✅ ¡Login exitoso! Bienvenido, """ + username + """');
                window.location.href = '/';
            </script>
            """
        else:
            # Credenciales incorrectas
            return """
            <script>
                alert('Credenciales incorrectas');
                window.history.back();
            </script>
            """
            
    except mysql.connector.Error as e:
        return f"Error de base de datos: {str(e)}", 500
    except Exception as e:
        return f"Error interno: {str(e)}", 500

@app.route('/api/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/user')
def get_user():
    """Obtener información del usuario actual (para AJAX)"""
    if session.get('logged_in'):
        return jsonify({
            'user_id': session.get('user_id'),
            'username': session.get('username'),
            'logged_in': True
        })
    else:
        return jsonify({'logged_in': False})

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
    print("🚀 Servidor API AnimeWorld iniciado")
    print("📍 URL: http://localhost:5000")
    print("\n📚 Endpoints disponibles:")
    print("   GET  /              - Página principal")
    print("   GET  /api/estado    - Estado del servicio")
    print("   POST /api/entrenar  - Entrenar modelo")
    print("   POST /api/recomendar - Obtener recomendaciones")
    print("   POST /api/login     - Login de usuario")
    print("   GET  /api/logout    - Logout de usuario")
    print("   GET  /api/user      - Info del usuario")
    
    app.run(debug=True, host='0.0.0.0', port=5000)