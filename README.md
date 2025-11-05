# Sistema de Recomendación de Anime

## 📋 Descripción
Sistema web de recomendación de anime que utiliza filtrado colaborativo para sugerir series y películas basadas en las preferencias del usuario.

## 🚀 Prerrequisitos
- Python 3.8+
- MySQL 8.0+
- Navegador web moderno

## 📦 Instalación

### 1. Instalar dependencias
```bash
pip install flask mysql-connector-python pandas numpy scikit-learn flask-cors tqdm
```
# Configurar base de datos
CREATE DATABASE usuarios_login;
USE usuarios_login;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

INSERT INTO usuarios VALUES 
(1, 'Leo', '123456.ABC'),
(2, 'Victor', '123456.ABC'),
(3, 'marc', '123456.ABC');

# Configurar conexión MySql

### Modificar archivo config.py
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña', 
    'database': 'usuarios_login'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
# Uso del programa

### Inicar aplicación
```bash
python api/api.py
```
y visitar
http://localhost:5000

### Funcionalidades
<ul>
  <li>Login/Logout - Sistema de autenticación</li>
  <li>Registro - Sistema de creación de usuarios</li>
  <li>Explorar catálogo - Visualizar animes</li>
  <li>Recomendaciones - Sistema ML personalizado</li>
  <li>Gestión de perfil - Opciones de usuario</li>
</ul>

### Endpoints

<ul>
  <li>POST /api/registro - Creación de Usuario</li>
  <li>POST /api/login - Autenticación</li>
  <li>GET /api/logout - Cerrar sesión</li>
  <li>POST /api/recomendar - Recomendaciones</li>
  <li>GET /api/estado - Estado del servicio</li>
</ul>

# Estructura de Proyecto
<ul>
    <li>api/api.py - Servidor Flask principal</li>
    <li>api/config.py - Configuración de base de datos</li>
    <li>api/templates/index.html - Interfaz web</li>
    <li>ia/script.py - Procesamiento de recomendaciones</li>
    <li>ia/recomendacion_anime.py - Algoritmo de machine learning</li>
    <li>datos/ - Datasets de anime (anime.csv, rating.csv)</li>
</ul>

# Configuración para desarrollo

<ul>
    <li>Asegurar que MySQL esté ejecutándose </li>
    <li>Verificar credenciales en config.py</li>
    <li>Los datos de anime deben estar en /datos/</li>
    <li>El servidor se inicia en puerto 5000</li>
</ul>

# 📊 Características Técnicas

<ul>
    <li>Backend: Flask + MySQL</li>
    <li>Frontend: HTML5 + Bootstrap + JavaScript</li>
    <li>ML: Filtrado colaborativo (Pearson correlation)</li>
    <li>Autenticación: Sesiones Flask</li>
</ul>













