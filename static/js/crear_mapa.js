// ===============================
// static/js/crear_mapa.js
// ===============================

// Variables globales
let municipioActual = null;
let configuracionesMunicipios = {};
let datosTabla = {
    filas: 0,
    columnas: 0,
    datos: []
};

// Función para seleccionar municipio
function seleccionarMunicipio(municipioId) {
    // Limpiar selección anterior
    document.querySelectorAll('.municipio-editable').forEach(path => {
        path.classList.remove('municipio-seleccionado');
    });
    
    // Seleccionar nuevo municipio
    municipioActual = municipioId;
    const municipioElement = document.getElementById('edit-' + municipioId);
    municipioElement.classList.add('municipio-seleccionado');
    
    // Actualizar interfaz
    document.getElementById('municipio-actual').value = municipioId;
    document.getElementById('municipio-status').innerHTML = 
        `<p>Municipio seleccionado: <strong>${getNombreMunicipio(municipioId)}</strong></p>`;
    
    // Cargar configuración existente si existe
    if (configuracionesMunicipios[municipioId]) {
        const config = configuracionesMunicipios[municipioId];
        document.getElementById('color-municipio').value = config.color;
        document.getElementById('info-municipio').value = config.informacion || '';
        
        if (config.imagen_url) {
            mostrarPreviewImagen(config.imagen_url);
        }
    } else {
        // Limpiar formulario
        document.getElementById('color-municipio').value = '#ffffff';
        document.getElementById('info-municipio').value = '';
        document.getElementById('preview-imagen').innerHTML = '';
    }
}

// Aplicar configuración a municipio
function aplicarConfiguracion() {
    if (!municipioActual) {
        alert('Selecciona un municipio primero');
        return;
    }

    const color = document.getElementById('color-municipio').value;
    const info = document.getElementById('info-municipio').value;
    const imagenFile = document.getElementById('imagen-municipio').files[0];

    // Aplicar color visualmente
    const municipioElement = document.getElementById('edit-' + municipioActual);
    municipioElement.style.fill = color;

    // Guardar configuración en memoria
    if (!configuracionesMunicipios[municipioActual]) {
        configuracionesMunicipios[municipioActual] = {};
    }
    
    configuracionesMunicipios[municipioActual].color = color;
    configuracionesMunicipios[municipioActual].informacion = info;

    // Subir imagen si existe
    if (imagenFile) {
        subirImagen(imagenFile).then(response => {
            if (response.success) {
                configuracionesMunicipios[municipioActual].imagen_url = response.url;
                mostrarPreviewImagen(response.url);
            } else {
                alert('Error al subir imagen: ' + response.error);
            }
        });
    }

    console.log('Configuración aplicada para:', municipioActual, configuracionesMunicipios[municipioActual]);
}

// Subir imagen
async function subirImagen(file) {
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

// Mostrar preview de imagen
function mostrarPreviewImagen(url) {
    document.getElementById('preview-imagen').innerHTML = 
        `<img src="${url}" alt="Preview" style="max-width: 100px; max-height: 100px; margin-top: 10px;">`;
}

// Generar tabla
function generarTabla() {
    const filas = parseInt(document.getElementById('num-filas').value);
    const columnas = parseInt(document.getElementById('num-columnas').value);
    
    if (filas < 1 || columnas < 1) {
        alert('El número de filas y columnas debe ser mayor a 0');
        return;
    }
    
    datosTabla.filas = filas;
    datosTabla.columnas = columnas;
    datosTabla.datos = [];
    
    let tablaHTML = '<table class="data-table"><tbody>';
    
    for (let i = 0; i < filas; i++) {
        tablaHTML += '<tr>';
        for (let j = 0; j < columnas; j++) {
            const cellId = `cell-${i}-${j}`;
            tablaHTML += `<td><input type="text" id="${cellId}" placeholder="Celda ${i+1},${j+1}" onchange="actualizarDatosTabla()"></td>`;
        }
        tablaHTML += '</tr>';
    }
    
    tablaHTML += '</tbody></table>';
    tablaHTML += '<button onclick="limpiarTabla()" class="btn btn-clear">Limpiar Tabla</button>';
    
    document.getElementById('tabla-container').innerHTML = tablaHTML;
}

// Actualizar datos de tabla
function actualizarDatosTabla() {
    datosTabla.datos = [];
    
    for (let i = 0; i < datosTabla.filas; i++) {
        const fila = [];
        for (let j = 0; j < datosTabla.columnas; j++) {
            const cellValue = document.getElementById(`cell-${i}-${j}`).value;
            fila.push(cellValue);
        }
        datosTabla.datos.push(fila);
    }
}

// Limpiar tabla
function limpiarTabla() {
    for (let i = 0; i < datosTabla.filas; i++) {
        for (let j = 0; j < datosTabla.columnas; j++) {
            document.getElementById(`cell-${i}-${j}`).value = '';
        }
    }
    datosTabla.datos = [];
}

// Guardar mapa completo
async function guardarMapa() {
    const nombreMapa = document.getElementById('nombre-mapa').value.trim();
    
    if (!nombreMapa) {
        alert('Ingresa un nombre para el mapa');
        return;
    }
    
    if (Object.keys(configuracionesMunicipios).length === 0) {
        alert('Configura al menos un municipio antes de guardar');
        return;
    }
    
    // Actualizar datos de tabla antes de guardar
    if (datosTabla.filas > 0) {
        actualizarDatosTabla();
    }
    
    const datosParaEnviar = {
        nombre: nombreMapa,
        descripcion: '',
        municipios_data: JSON.stringify(configuracionesMunicipios),
        tabla_data: JSON.stringify(datosTabla)
    };
    
    try {
        const response = await fetch('/maps/guardar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(datosParaEnviar)
        });
        
        if (response.ok) {
            alert('Mapa guardado exitosamente');
            window.location.href = '/';
        } else {
            alert('Error al guardar el mapa');
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

// Función auxiliar para obtener nombre del municipio
function getNombreMunicipio(municipioId) {
    const nombres = {
        'landaDematamoros': 'Landa de Matamoros',
        'arroyoSeco': 'Arroyo Seco',
        'sanJoaquin': 'San Joaquín',
        'cadereytaDemontes': 'Cadereyta de Montes',
        'ezequielMontes': 'Ezequiel Montes',
        'colon': 'Colón',
        'tequisquiapan': 'Tequisquiapan',
        'huimilpan': 'Huimilpan',
        'amealcoDeBonfil': 'Amealco de Bonfil',
        'sanJuanDelRio': 'San Juan del Río',
        'pedroEscobedo': 'Pedro Escobedo',
        'corregidora': 'Corregidora',
        'queretaro': 'Querétaro',
        'elMarques': 'El Marqués',
        'toliman': 'Tolimán',
        'penamiller': 'Peñamiller',
        'pinalDeAmoles': 'Pinal de Amoles',
        'jalpanDeSerra': 'Jalpan de Serra'
    };
    return nombres[municipioId] || municipioId;
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Listeners para cambios en inputs de tabla
    document.getElementById('imagen-municipio').addEventListener('change', function(e) {
        if (e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                mostrarPreviewImagen(e.target.result);
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    });
});
