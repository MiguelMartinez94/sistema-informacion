# ===============================
# blueprints/api/routes.py
# ===============================

from flask import jsonify, request
from controllers.api import api_bp
from models.models import Mapa, MunicipioConfiguracion, TablaDatos, Municipio

@api_bp.route('/mapas')
def get_mapas():
    """Obtener todos los mapas"""
    try:
        mapas = Mapa.obtener_todos()
        return jsonify({
            'success': True,
            'mapas': mapas
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/mapa/<int:mapa_id>')
def get_mapa(mapa_id):
    """Obtener mapa específico con toda su configuración"""
    try:
        mapa = Mapa.obtener_por_id(mapa_id)
        if not mapa:
            return jsonify({
                'success': False,
                'error': 'Mapa no encontrado'
            }), 404
        
        municipios = MunicipioConfiguracion.obtener_por_mapa(mapa_id)
        tabla = TablaDatos.obtener_por_mapa(mapa_id)
        
        return jsonify({
            'success': True,
            'mapa': mapa,
            'municipios': municipios,
            'tabla': tabla
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/municipios')
def get_municipios():
    """Obtener todos los municipios"""
    try:
        municipios = Municipio.obtener_todos()
        return jsonify({
            'success': True,
            'municipios': municipios
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/municipio/<municipio_id>/configuracion/<int:mapa_id>')
def get_configuracion_municipio(municipio_id, mapa_id):
    """Obtener configuración específica de un municipio en un mapa"""
    try:
        config = MunicipioConfiguracion.obtener_configuracion(mapa_id, municipio_id)
        return jsonify({
            'success': True,
            'configuracion': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500