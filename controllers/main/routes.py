# ===============================
# blueprints/main/routes.py
# ===============================

from flask import render_template, request, redirect, url_for, flash
from controllers.main import main_bp
from models.models import Mapa, Municipio

@main_bp.route('/')
def index():
    """Página principal"""
    mapas = Mapa.obtener_todos()
    return render_template('index.html', mapas=mapas)

@main_bp.route('/crear')
def crear_mapa():
    """Interfaz para crear un nuevo mapa."""
    municipios = Municipio.obtener_todos()
    return render_template('editor_mapa.html', mapa=None, municipios=municipios)

# --- ESTA ES LA FUNCIÓN QUE FALTABA ---
@main_bp.route('/ver/<int:mapa_id>')
def ver_mapa(mapa_id):
    """Interfaz para visualizar mapa"""
    mapa = Mapa.obtener_por_id(mapa_id)
    if not mapa:
        return redirect(url_for('main.index'))
    
    return render_template('visualizar_mapa.html', mapa=mapa, mapa_id=mapa_id)
# --- FIN DE LA FUNCIÓN QUE FALTABA ---

@main_bp.route('/modificar')
def modificar_mapa():
    """Página para seleccionar qué mapa modificar."""
    mapas = Mapa.obtener_todos()
    return render_template('modificar_mapa.html', mapas=mapas)

@main_bp.route('/modificar/<int:mapa_id>')
def modificar_mapa_especifico(mapa_id):
    """Interfaz para modificar un mapa específico."""
    mapa = Mapa.obtener_por_id(mapa_id)
    if not mapa:
        flash('Mapa no encontrado', 'error')
        return redirect(url_for('main.index'))
    
    municipios = Municipio.obtener_todos()
    return render_template('editor_mapa.html', mapa=mapa, municipios=municipios)