// ===============================
// static/js/editor_mapa.js
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
        const id = path.id.replace('municipio-', '');
        path.setAttribute('onclick', `seleccionarMunicipio('${id}')`);
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
                const el = document.getElementById(`municipio-${municipio.municipio_id}`);
                if (el) el.style.fill = municipio.color;
            });
            
            // Cargar tabla
            if (data.tabla) {
                datosTabla = data.tabla;
                datosTabla.datos = JSON.parse(datosTabla.datos_json); // Asegurarse de que 'datos' es un array
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
    
    const municipioElement = document.getElementById(`municipio-${municipioId}`);
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

    document.getElementById(`municipio-${municipioActual}`).style.fill = color;

    configuracionesMunicipios[municipioActual] = {
        ...configuracionesMunicipios[municipioActual],
        color: color,
        informacion: info,
    };

    if (imagenFile) {
        const response = await subirImagen(imagenFile);
        if (response.success) {
            configuracionesMunicipios[municipioActual].imagen_url = response.url;
            mostrarPreviewImagen(response.url);
        } else {
            alert('Error al subir imagen: ' + response.error);
        }
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
        `<img src="${url}" alt="Preview" style="max-width: 100px; max-height: 100px; margin-top: 10px;">`;
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
    datosParaEnviar.append('descripcion', ''); // Puedes agregar un campo para esto si quieres
    datosParaEnviar.append('municipios_data', JSON.stringify(configuracionesMunicipios));
    datosParaEnviar.append('tabla_data', JSON.stringify(datosTabla));

    const url = mapaId ? `/maps/actualizar/${mapaId}` : '/maps/guardar';

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: datosParaEnviar
        });
        
        if (response.ok) {
            window.location.href = '/'; // Redirigir al inicio
        } else {
            alert('Error al guardar el mapa');
        }
    } catch (error) {
        alert('Error de conexión: ' + error.message);
    }
}

// ... (El resto de las funciones para la tabla, si las necesitas)