// ===============================
// static/js/visualizar_mapa.js
// ===============================

// Variables globales para visualización
let datosMapaActual = null;
let configuracionesMunicipiosVisualizacion = {};

// Mostrar información del municipio
function mostrarInfo(municipioId, event) {
    const tooltip = document.getElementById('tooltip-municipio');
    const config = configuracionesMunicipiosVisualizacion[municipioId];
    
    if (config) {
        document.getElementById('tooltip-nombre').textContent = getNombreMunicipio(municipioId);
        document.getElementById('tooltip-info').textContent = config.informacion || 'Sin información disponible';
        
        const imagen = document.getElementById('tooltip-imagen');
        if (config.imagen_url) {
            imagen.src = config.imagen_url;
            imagen.style.display = 'block';
        } else {
            imagen.style.display = 'none';
        }
    } else {
        document.getElementById('tooltip-nombre').textContent = getNombreMunicipio(municipioId);
        document.getElementById('tooltip-info').textContent = 'Sin información configurada';
        document.getElementById('tooltip-imagen').style.display = 'none';
    }
    
    tooltip.style.display = 'block';
    moverTooltip(event);
}

// Ocultar información
function ocultarInfo() {
    document.getElementById('tooltip-municipio').style.display = 'none';
}

// Mover tooltip con el cursor
function moverTooltip(event) {
    const tooltip = document.getElementById('tooltip-municipio');
    tooltip.style.left = (event.pageX + 10) + 'px';
    tooltip.style.top = (event.pageY + 10) + 'px';
}

// Cargar datos del mapa
async function cargarDatosMapa() {
    const mapaId = document.getElementById('mapa-visualizacion').dataset.mapaId;
    
    try {
        const response = await fetch(`/api/mapa/${mapaId}`);
        const data = await response.json();
        
        if (data.success) {
            datosMapaActual = data;
            aplicarConfiguracionesMunicipios(data.municipios);
            cargarTablaEstadisticas(data.tabla);
        } else {
            console.error('Error al cargar datos del mapa:', data.error);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}

// Aplicar configuraciones de municipios
function aplicarConfiguracionesMunicipios(municipios) {
    municipios.forEach(municipio => {
        configuracionesMunicipiosVisualizacion[municipio.municipio_id] = municipio;
        
        // Aplicar color al municipio
        const municipioElement = document.getElementById('view-' + municipio.municipio_id);
        if (municipioElement) {
            municipioElement.style.fill = municipio.color;
        }
    });
}

// Cargar tabla de estadísticas
function cargarTablaEstadisticas(tablaDatos) {
    const container = document.getElementById('tabla-estadisticas');
    
    if (!tablaDatos || !tablaDatos.datos || tablaDatos.datos.length === 0) {
        container.innerHTML = '<p>No hay datos estadísticos disponibles</p>';
        return;
    }
    
    let tablaHTML = '<table class="stats-table"><tbody>';
    
    tablaDatos.datos.forEach(fila => {
        tablaHTML += '<tr>';
        fila.forEach(celda => {
            tablaHTML += `<td>${celda || ''}</td>`;
        });
        tablaHTML += '</tr>';
    });
    
    tablaHTML += '</tbody></table>';
    container.innerHTML = tablaHTML;
}

// Inicialización para visualización
document.addEventListener('DOMContentLoaded', function() {
    cargarDatosMapa();
});