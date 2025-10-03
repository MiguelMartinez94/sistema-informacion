# ===============================
# blueprints/maps/routes.py
# ===============================

from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from controllers.maps import maps_bp
from models.models import Mapa, MunicipioConfiguracion, TablaDatos
import os
import uuid
import json

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@maps_bp.route('/guardar', methods=['POST'])
@maps_bp.route('/actualizar/<int:mapa_id>', methods=['POST'])
@maps_bp.route('/guardar', methods=['POST'])
@maps_bp.route('/actualizar/<int:mapa_id>', methods=['POST'])
def guardar_modificar_mapa(mapa_id=None):
    """Guardar un nuevo mapa o actualizar uno existente."""
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion', '')

        if not nombre:
            flash('El nombre del mapa es requerido', 'error')
            # Ajustar a la ruta correcta para renderizar la plantilla de edición
            return redirect(url_for('main.crear_mapa'))

        if mapa_id is None:
            # Crear nuevo mapa
            mapa_id = Mapa.crear(nombre, descripcion)
            flash_message = 'Mapa guardado exitosamente'
        else:
            # --- INICIO DE LA CORRECCIÓN ---
            # Al actualizar, primero borramos las configuraciones antiguas.
            MunicipioConfiguracion.eliminar_por_mapa(mapa_id)
            # También podrías actualizar el nombre del mapa aquí si lo necesitas.
            # Mapa.actualizar_nombre(mapa_id, nombre) # (Función hipotética)
            flash_message = 'Mapa actualizado exitosamente'
            # --- FIN DE LA CORRECCIÓN ---

        # Guardar (o re-guardar) configuraciones de municipios
        municipios_data = request.form.get('municipios_data')
        if municipios_data:
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
            tabla_info = json.loads(tabla_data)
            
            tabla = TablaDatos(
                mapa_id=mapa_id,
                filas=tabla_info.get('filas', 0),
                columnas=tabla_info.get('columnas', 0),
                # CORRECCIÓN: Evitar doble codificación JSON
                datos=tabla_info.get('datos', [])
            )
            tabla.guardar()

        flash(flash_message, 'success')
        return redirect(url_for('main.index'))

    except Exception as e:
        flash(f'Error al guardar el mapa: {str(e)}', 'error')
        if mapa_id:
            return redirect(url_for('main.modificar_mapa_especifico', mapa_id=mapa_id))
        else:
            return redirect(url_for('main.crear_mapa'))

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
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Guardar archivo en la carpeta UPLOAD_FOLDER configurada
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            
            # Retornar la URL correcta usando url_for para la nueva ruta
            return {'url': url_for('uploaded_file', filename=unique_filename)}, 200
        
        return {'error': 'Tipo de archivo no permitido'}, 400
        
    except Exception as e:
        return {'error': str(e)}, 500