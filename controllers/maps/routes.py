# ===============================
# blueprints/maps/routes.py
# ===============================

from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from controllers.maps import maps_bp
from models.models import Mapa, MunicipioConfiguracion, TablaDatos
import os
import uuid

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@maps_bp.route('/guardar', methods=['POST'])
def guardar_mapa():
    """Guardar nuevo mapa"""
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion', '')
        
        if not nombre:
            flash('El nombre del mapa es requerido', 'error')
            return redirect(url_for('main.crear_mapa'))
        
        # Crear mapa
        mapa_id = Mapa.crear(nombre, descripcion)
        
        # Guardar configuraciones de municipios
        municipios_data = request.form.get('municipios_data')
        if municipios_data:
            import json
            municipios = json.loads(municipios_data)
            
            for municipio_id, config in municipios.items():
                municipio_config = MunicipioConfiguracion(
                    mapa_id=mapa_id,
                    municipio_id=municipio_id,
                    color=config.get('color', '#FFFFFF'),
                    informacion=config.get('informacion', ''),
                    imagen_url=config.get('imagen_url', '')
                )
                municipio_config.guardar()
        
        # Guardar tabla de datos
        tabla_data = request.form.get('tabla_data')
        if tabla_data:
            import json
            tabla_info = json.loads(tabla_data)
            
            tabla = TablaDatos(
                mapa_id=mapa_id,
                filas=tabla_info.get('filas', 0),
                columnas=tabla_info.get('columnas', 0),
                datos=tabla_info.get('datos', [])
            )
            tabla.guardar()
        
        flash('Mapa guardado exitosamente', 'success')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        flash(f'Error al guardar el mapa: {str(e)}', 'error')
        return redirect(url_for('main.crear_mapa'))

@maps_bp.route('/actualizar/<int:mapa_id>', methods=['POST'])
def actualizar_mapa(mapa_id):
    """Actualizar mapa existente"""
    try:
        # Similar a guardar_mapa pero actualizando
        municipios_data = request.form.get('municipios_data')
        if municipios_data:
            import json
            municipios = json.loads(municipios_data)
            
            for municipio_id, config in municipios.items():
                municipio_config = MunicipioConfiguracion(
                    mapa_id=mapa_id,
                    municipio_id=municipio_id,
                    color=config.get('color', '#FFFFFF'),
                    informacion=config.get('informacion', ''),
                    imagen_url=config.get('imagen_url', '')
                )
                municipio_config.guardar()
        
        # Actualizar tabla
        tabla_data = request.form.get('tabla_data')
        if tabla_data:
            import json
            tabla_info = json.loads(tabla_data)
            
            tabla = TablaDatos(
                mapa_id=mapa_id,
                filas=tabla_info.get('filas', 0),
                columnas=tabla_info.get('columnas', 0),
                datos=tabla_info.get('datos', [])
            )
            tabla.guardar()
        
        flash('Mapa actualizado exitosamente', 'success')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        flash(f'Error al actualizar el mapa: {str(e)}', 'error')
        return redirect(url_for('main.modificar_mapa_especifico', mapa_id=mapa_id))

@maps_bp.route('/eliminar/<int:mapa_id>', methods=['POST'])
def eliminar_mapa(mapa_id):
    """Eliminar mapa"""
    try:
        if Mapa.eliminar(mapa_id):
            flash('Mapa eliminado exitosamente', 'success')
        else:
            flash('No se pudo eliminar el mapa', 'error')
    except Exception as e:
        flash(f'Error al eliminar el mapa: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))

@maps_bp.route('/subir_imagen', methods=['POST'])
def subir_imagen():
    """Subir imagen para municipio"""
    try:
        if 'imagen' not in request.files:
            return {'error': 'No se encontró archivo'}, 400
        
        file = request.files['imagen']
        if file.filename == '':
            return {'error': 'No se seleccionó archivo'}, 400
        
        if file and allowed_file(file.filename):
            # Generar nombre único
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Guardar archivo
            filepath = os.path.join('static', 'images', 'municipios', unique_filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            
            # Retornar URL relativa
            return {'url': f'/static/images/municipios/{unique_filename}'}, 200
        
        return {'error': 'Tipo de archivo no permitido'}, 400
        
    except Exception as e:
        return {'error': str(e)}, 500
