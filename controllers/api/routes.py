# ===============================
# blueprints/api/routes.py (CORREGIDO)
# ===============================

from flask import jsonify, request
from controllers.api import api_bp
# CORRECCIÓN: Se elimina 'MunicipioConfiguracion' que ya no existe
from models.models import Mapa, Municipio, TablaDatos, Contenido
import json

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
            return jsonify({'success': False, 'error': 'Mapa no encontrado'}), 404
        
        # Usar el nuevo método para obtener las configuraciones uniendo las tablas
        municipios_config = Municipio.obtener_configuraciones_por_mapa(mapa_id)
        tabla = TablaDatos.obtener_por_mapa(mapa_id)
        
        # Decodificar el JSON de la tabla si existe
        if tabla and 'datos_json' in tabla and tabla['datos_json']:
            tabla['datos'] = json.loads(tabla['datos_json'])
        
        return jsonify({
            'success': True,
            'mapa': mapa,
            'municipios': municipios_config,
            'tabla': tabla
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# El resto de las rutas de la API pueden permanecer igual si no las has modificado
# (get_municipios, etc.)