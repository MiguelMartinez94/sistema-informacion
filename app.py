# ===============================
# app.py - APLICACIÓN PRINCIPAL
# ===============================

from flask import Flask, send_from_directory
from models.database import init_db
from controllers.main import main_bp
from controllers.maps import maps_bp
from controllers.api import api_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Inicializar base de datos
    init_db(app)
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(maps_bp, url_prefix='/maps')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Crear el directorio de subidas si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # --- AÑADIR ESTA NUEVA RUTA ---
    # Esta ruta servirá los archivos desde la carpeta UPLOAD_FOLDER
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # --- FIN DE LA NUEVA RUTA ---

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)