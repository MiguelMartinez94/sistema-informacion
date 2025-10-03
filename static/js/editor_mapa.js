// ===============================
// static/js/editor_mapa.js (CORREGIDO)
// ===============================

// Variables globales
let municipioActual = null;
let configuracionesMunicipios = {};
let datosTabla = {
    filas: 0,
    columnas: 0,
    datos: []
};
let mapaId = null;

document.addEventListener('DOMContentLoaded', function() {
    mapaId = document.getElementById('mapa-edicion').dataset.mapaId;
    
    if (mapaId) {
        // Modo Modificar: Cargar datos existentes
        cargarDatosParaModificar(mapaId);
    }

    // Configurar listeners para los municipios
    document.querySelectorAll('.municipio-path').forEach(path => {
        // CORRECCIÓN: El ID del path ya es el correcto, no necesita prefijos.
        path.setAttribute('onclick', `seleccionarMunicipio('${path.id}')`);
    });

    // Listener para la subida de imagen
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

async function cargarDatosParaModificar(id) {
    try {
        const response = await fetch(`/api/mapa/${id}`);
        const data = await response.json();
        
        if (data.success) {
            // Cargar configuraciones de municipios
            data.municipios.forEach(municipio => {
                configuracionesMunicipios[municipio.municipio_id] = municipio;
                // CORRECCIÓN: Se busca el ID directamente, sin el prefijo 'edit-'
                const el = document.getElementById(municipio.municipio_id);
                if (el) el.style.fill = municipio.color;
            });
            
            // Cargar tabla
            if (data.tabla) {
                datosTabla = data.tabla;
                // La API ya devuelve 'datos' como un array, no es necesario parsear de nuevo.
                generarTabla(true);
            }
        } else {
            console.error('Error al cargar datos del mapa:', data.error);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}


function seleccionarMunicipio(municipioId) {
    document.querySelectorAll('.municipio-path').forEach(path => {
        path.classList.remove('seleccionado');
    });
    
    // CORRECCIÓN: Se busca el ID directamente
    const municipioElement = document.getElementById(municipioId);
    if(municipioElement) {
      municipioElement.classList.add('seleccionado');
    }
    
    municipioActual = municipioId;
    document.getElementById('municipio-actual').value = municipioId;
    document.getElementById('municipio-status').innerHTML = `<p>Editando: <strong>${municipioId.replace(/([A-Z])/g, ' $1').trim()}</strong></p>`;
    
    // Cargar configuración existente o limpiar
    const config = configuracionesMunicipios[municipioId] || {};
    document.getElementById('color-municipio').value = config.color || '#ffffff';
    document.getElementById('info-municipio').value = config.informacion || '';
    
    if (config.imagen_url) {
        mostrarPreviewImagen(config.imagen_url);
    } else {
        document.getElementById('preview-imagen').innerHTML = '';
        document.getElementById('imagen-municipio').value = ''; // Limpiar input de archivo
    }
}

async function aplicarConfiguracion() {
    if (!municipioActual) {
        alert('Selecciona un municipio primero');
        return;
    }

    const color = document.getElementById('color-municipio').value;
    const info = document.getElementById('info-municipio').value;
    const imagenFile = document.getElementById('imagen-municipio').files[0];

    // CORRECCIÓN: Se busca el ID directamente
    document.getElementById(municipioActual).style.fill = color;

    // Crear o actualizar la configuración en memoria
    configuracionesMunicipios[municipioActual] = {
        ...configuracionesMunicipios[municipioActual], // Mantener datos existentes como el nombre
        municipio_id: municipioActual,
        color: color,
        informacion: info,
    };

    // Si se subió una nueva imagen
    if (imagenFile) {
        const response = await subirImagen(imagenFile);
        if (response.success) {
            configuracionesMunicipios[municipioActual].imagen_url = response.url;
            mostrarPreviewImagen(response.url);
        } else {
            alert('Error al subir imagen: ' + response.error);
        }
    }
    // Si no hay imagen nueva, pero ya existía una, la mantenemos
    else if (!configuracionesMunicipios[municipioActual].imagen_url) {
        configuracionesMunicipios[municipioActual].imagen_url = null;
    }
}

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

function mostrarPreviewImagen(url) {
    document.getElementById('preview-imagen').innerHTML = 
        `<img src="${url}" alt="Vista previa" style="max-width: 100px; max-height: 100px; margin-top: 10px;">`;
}

async function guardarMapa() {
    const nombreMapa = document.getElementById('nombre-mapa').value.trim();
    if (!nombreMapa) {
        alert('Ingresa un nombre para el mapa');
        return;
    }

    if (datosTabla.filas > 0) {
        actualizarDatosTabla();
    }

    const datosParaEnviar = new URLSearchParams();
    datosParaEnviar.append('nombre', nombreMapa);
    datosParaEnviar.append('descripcion', '');
    datosParaEnviar.append('municipios_data', JSON.stringify(configuracionesMunicipios));
    datosParaEnviar.append('tabla_data', JSON.stringify(datosTabla));

    const url = mapaId ? `/maps/actualizar/${mapaId}` : '/maps/guardar';

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: datosParaEnviar
        });
        
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            alert('Error al guardar el mapa');
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}