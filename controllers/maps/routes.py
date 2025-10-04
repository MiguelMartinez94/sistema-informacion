# ===============================
# blueprints/maps/routes.py (AJUSTADO A NUEVO ESQUEMA)
# ===============================

from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from controllers.maps import maps_bp
from models.models import Mapa, Contenido, Municipio, TablaDatos
import os
import uuid
import json

# ... (La función allowed_file permanece igual) ...

@maps_bp.route('/guardar', methods=['POST'])
@maps_bp.route('/actualizar/<int:mapa_id>', methods=['POST'])
def guardar_modificar_mapa(mapa_id=None):
    """Guardar un nuevo mapa o actualizar uno existente."""
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion', '')

        if not nombre:
            flash('El nombre del mapa es requerido', 'error')
            return redirect(url_for('main.crear_mapa'))

        if mapa_id is None:
            # 1. Crear nuevo mapa
            mapa_id = Mapa.crear(nombre, descripcion)
            flash_message = 'Mapa guardado exitosamente'
        else:
            # Al actualizar, podrías querer actualizar el nombre/descripción aquí
            # Por ahora, solo preparamos para actualizar los contenidos
            flash_message = 'Mapa actualizado exitosamente'

        # 2. Procesar los datos de los municipios
        municipios_data = request.form.get('municipios_data')
        if municipios_data:
            municipios = json.loads(municipios_data)
            
            # Si es una actualización, borramos los vínculos viejos para empezar de cero
            if mapa_id:
                Municipio.eliminar_configuraciones_por_mapa(mapa_id)

            for municipio_id, config in municipios.items():
                # 3. Para cada municipio, crear una nueva entrada de Contenido
                contenido_id = Contenido.crear(
                    color=config.get('color', '#FFFFFF'),
                    detalle=config.get('informacion', ''),
                    imagen=config.get('imagen_url', '')
                )
                
                # 4. Vincular el Mapa, el Municipio y el nuevo Contenido
                Municipio.vincular_contenido(mapa_id, municipio_id, contenido_id)
        
        # ... (La lógica de TablaDatos puede permanecer igual) ...

        flash(flash_message, 'success')
        return redirect(url_for('main.index'))

    except Exception as e:
        flash(f'Error al guardar el mapa: {str(e)}', 'error')
        if mapa_id:
            return redirect(url_for('main.modificar_mapa_especifico', mapa_id=mapa_id))
        else:
            return redirect(url_for('main.crear_mapa'))


# ... (El resto de las funciones: eliminar_mapa y subir_imagen permanecen igual) ...