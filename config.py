# ===============================
# config.py - CONFIGURACIÓN
# ===============================

import os

# Obtiene la ruta absoluta del directorio donde se encuentra este archivo
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Kesadilla94'
    
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Kesadilla94'
    MYSQL_DB = 'queretaro_mapas'
    MYSQL_PORT = 3310
    
    # Para ejecutable con SQLite
    SQLITE_PATH = 'queretaro_mapas.db'
    
    # Configuración de archivos
    # Usamos BASE_DIR para asegurarnos de que la ruta sea siempre correcta
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}