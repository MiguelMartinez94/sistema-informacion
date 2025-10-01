# ===============================
# app.py - APLICACIÓN PRINCIPAL
# ===============================

from flask import Flask, render_template
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
    
    # Crear directorios necesarios
    os.makedirs('static/images/municipios', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)