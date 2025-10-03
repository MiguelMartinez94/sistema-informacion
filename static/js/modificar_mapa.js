// ===============================
// static/js/modificar_mapa.js
// ===============================

// Variables globales para modificación
let mapaParaModificar = null;
let configuracionesOriginales = {};

// Cargar mapa para modificar
function cargarMapaParaModificar() {
    const mapaId = document.getElementById('mapas-existentes').value;
    
    if (!mapaId) {
        alert('Selecciona un mapa para modificar');
        return;
    }
    
    window.location.href = `/modificar/${mapaId}`;
}

// Cargar datos del mapa para modificación
async function cargarDatosMapaModificacion() {
    const mapaId = document.getElementById('mapa-modificacion').dataset.mapaId;
    
    try {
        const response = await fetch(`/api/mapa/${mapaId}`);
        const data = await response.json();
        
        if (data.success) {
            mapaParaModificar = data;
            configuracionesOriginales = {};
            
            // Cargar configuraciones existentes
            data.municipios.forEach(municipio => {
                configuracionesOriginales[municipio.municipio_id] = municipio;
                
                // Aplicar color al municipio
                const el = document.getElementById(municipio.municipio_id);
                if (municipioElement) {
                    municipioElement.style.fill = municipio.color;
                }
            });
            
            // Cargar tabla existente
            if (data.tabla) {
                cargarTablaModificacion(data.tabla);
            }
            
            // Configurar nombre del mapa
            document.getElementById('nombre-mapa-modificar').value = data.mapa.nombre;
        } else {
            console.error('Error al cargar datos del mapa:', data.error);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}

// Seleccionar municipio para modificar (reutiliza lógica de crear_mapa.js)
function seleccionarMunicipioModificar(municipioId) {
    // Limpiar selección anterior
    document.querySelectorAll('.municipio-editable').forEach(path => {
        path.classList.remove('municipio-seleccionado');
    });
    
    // Seleccionar nuevo municipio
    municipioActual = municipioId;
    const municipioElement = document.getElementById(municipioId);
    municipioElement.classList.add('municipio-seleccionado');
    
    // Actualizar interfaz
    document.getElementById('municipio-actual-modificar').value = municipioId;
    
    // Cargar configuración existente
    const config = configuracionesOriginales[municipioId] || {};
    document.getElementById('color-municipio-modificar').value = config.color || '#ffffff';
    document.getElementById('info-municipio-modificar').value = config.informacion || '';
    
    if (config.imagen_url) {
        document.getElementById('preview-imagen-modificar').innerHTML = 
            `<img src="${config.imagen_url}" alt="Preview" style="max-width: 100px; max-height: 100px; margin-top: 10px;">`;
    } else {
        document.getElementById('preview-imagen-modificar').innerHTML = '';
    }
}

// Aplicar modificación a municipio
function aplicarModificacion() {
    if (!municipioActual) {
        alert('Selecciona un municipio primero');
        return;
    }

    const color = document.getElementById('color-municipio-modificar').value;
    const info = document.getElementById('info-municipio-modificar').value;
    const imagenFile = document.getElementById('imagen-municipio-modificar').files[0];

    // Aplicar color visualmente
    const municipioElement = document.getElementById(municipioActual);
    municipioElement.style.fill = color;

    // Actualizar configuración
    if (!configuracionesOriginales[municipioActual]) {
        configuracionesOriginales[municipioActual] = {};
    }
    
    configuracionesOriginales[municipioActual].color = color;
    configuracionesOriginales[municipioActual].informacion = info;

    // Subir nueva imagen si existe
    if (imagenFile) {
        subirImagenModificacion(imagenFile).then(response => {
            if (response.success) {
                configuracionesOriginales[municipioActual].imagen_url = response.url;
                document.getElementById('preview-imagen-modificar').innerHTML = 
                    `<img src="${response.url}" alt="Preview" style="max-width: 100px; max-height: 100px; margin-top: 10px;">`;
            } else {
                alert('Error al subir imagen: ' + response.error);
            }
        });
    }

    console.log('Modificación aplicada para:', municipioActual, configuracionesOriginales[municipioActual]);
}

// Subir imagen para modificación
async function subirImagenModificacion(file) {
    const formData = new FormData();
    formData.append('imagen', file);
    
    try {
        const response = await fetch('/maps/subir_imagen', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        return { success: response.ok, ...result };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Cargar tabla para modificación
function cargarTablaModificacion(tablaDatos) {
    if (!tablaDatos || !tablaDatos.datos) {
        document.getElementById('tabla-modificacion').innerHTML = 
            '<p>No hay tabla configurada. <button onclick="crearNuevaTabla()">Crear Nueva Tabla</button></p>';
        return;
    }
    
    const filas = tablaDatos.filas;
    const columnas = tablaDatos.columnas;
    const datos = tablaDatos.datos;
    
    let tablaHTML = '<h4>Tabla Existente</h4>';
    tablaHTML += '<table class="data-table"><tbody>';
    
    for (let i = 0; i < filas; i++) {
        tablaHTML += '<tr>';
        for (let j = 0; j < columnas; j++) {
            const cellId = `modify-cell-${i}-${j}`;
            const valor = (datos[i] && datos[i][j]) ? datos[i][j] : '';
            tablaHTML += `<td><input type="text" id="${cellId}" value="${valor}" onchange="actualizarTablaModificacion()"></td>`;
        }
        tablaHTML += '</tr>';
    }
    
    tablaHTML += '</tbody></table>';
    tablaHTML += '<button onclick="limpiarTablaModificacion()" class="btn btn-clear">Limpiar Tabla</button>';
    tablaHTML += '<button onclick="crearNuevaTabla()" class="btn btn-new">Nueva Tabla</button>';
    
    document.getElementById('tabla-modificacion').innerHTML = tablaHTML;
    
    // Actualizar datos globales
    datosTabla = {
        filas: filas,
        columnas: columnas,
        datos: datos
    };
}

// Crear nueva tabla desde modificación
function crearNuevaTabla() {
    const filas = prompt('Número de filas:', '3');
    const columnas = prompt('Número de columnas:', '3');
    
    if (filas && columnas) {
        datosTabla = {
            filas: parseInt(filas),
            columnas: parseInt(columnas),
            datos: []
        };
        
        let tablaHTML = '<h4>Nueva Tabla</h4>';
        tablaHTML += '<table class="data-table"><tbody>';
        
        for (let i = 0; i < datosTabla.filas; i++) {
            tablaHTML += '<tr>';
            for (let j = 0; j < datosTabla.columnas; j++) {
                const cellId = `modify-cell-${i}-${j}`;
                tablaHTML += `<td><input type="text" id="${cellId}" placeholder="Celda ${i+1},${j+1}" onchange="actualizarTablaModificacion()"></td>`;
            }
            tablaHTML += '</tr>';
        }
        
        tablaHTML += '</tbody></table>';
        tablaHTML += '<button onclick="limpiarTablaModificacion()" class="btn btn-clear">Limpiar Tabla</button>';
        
        document.getElementById('tabla-modificacion').innerHTML = tablaHTML;
    }
}

// Actualizar datos de tabla modificación
function actualizarTablaModificacion() {
    datosTabla.datos = [];
    
    for (let i = 0; i < datosTabla.filas; i++) {
        const fila = [];
        for (let j = 0; j < datosTabla.columnas; j++) {
            const cellValue = document.getElementById(`modify-cell-${i}-${j}`).value;
            fila.push(cellValue);
        }
        datosTabla.datos.push(fila);
    }
}

// Limpiar tabla modificación
function limpiarTablaModificacion() {
    for (let i = 0; i < datosTabla.filas; i++) {
        for (let j = 0; j < datosTabla.columnas; j++) {
            document.getElementById(`modify-cell-${i}-${j}`).value = '';
        }
    }
    datosTabla.datos = [];
}

// Guardar modificaciones
async function guardarModificaciones() {
    const nombreMapa = document.getElementById('nombre-mapa-modificar').value.trim();
    const mapaId = document.getElementById('mapa-modificacion').dataset.mapaId;
    
    if (!nombreMapa) {
        alert('Ingresa un nombre para el mapa');
        return;
    }
    
    // Actualizar datos de tabla antes de guardar
    if (datosTabla.filas > 0) {
        actualizarTablaModificacion();
    }
    
    const datosParaEnviar = {
        municipios_data: JSON.stringify(configuracionesOriginales),
        tabla_data: JSON.stringify(datosTabla)
    };
    
    try {
        const response = await fetch(`/maps/actualizar/${mapaId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(datosParaEnviar)
        });
        
        if (response.ok) {
            alert('Mapa modificado exitosamente');
            window.location.href = '/';
        } else {
            alert('Error al modificar el mapa');
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

// Inicialización para modificación
document.addEventListener('DOMContentLoaded', function() {
    // Si estamos en la página de modificación específica
    if (document.getElementById('mapa-modificacion')) {
        cargarDatosMapaModificacion();
        
        // Agregar event listeners
        document.getElementById('imagen-municipio-modificar').addEventListener('change', function(e) {
            if (e.target.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('preview-imagen-modificar').innerHTML = 
                        `<img src="${e.target.result}" alt="Preview" style="max-width: 100px; max-height: 100px; margin-top: 10px;">`;
                };
                reader.readAsDataURL(e.target.files[0]);
            }
        });
    }
});