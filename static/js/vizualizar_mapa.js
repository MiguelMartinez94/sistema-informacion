// ===============================
// static/js/visualizar_mapa.js (CORREGIDO)
// ===============================

document.addEventListener('DOMContentLoaded', function() {
    const mapaContainer = document.getElementById('mapa-visualizacion');
    if (mapaContainer) {
        const mapaId = mapaContainer.dataset.mapaId;
        if (mapaId) {
            cargarDatosMapa(mapaId);
        }
    }
});

let configuracionesMunicipios = {};

async function cargarDatosMapa(mapaId) {
    try {
        const response = await fetch(`/api/mapa/${mapaId}`);
        const data = await response.json();

        if (data.success) {
            // Guardar configuraciones y aplicar colores
            data.municipios.forEach(municipio => {
                configuracionesMunicipios[municipio.municipio_id] = municipio;
                // CORRECCIÓN: Se busca el ID directamente, sin el prefijo 'view-'
                const municipioElement = document.getElementById(municipio.municipio_id);
                if (municipioElement) {
                    municipioElement.style.fill = municipio.color;
                }
            });

            // Asignar eventos de tooltip a todos los municipios
            document.querySelectorAll('.municipio-path').forEach(path => {
                path.addEventListener('mouseover', (event) => mostrarInfo(path.id, event));
                path.addEventListener('mouseout', ocultarInfo);
                path.addEventListener('mousemove', moverTooltip);
            });

            // Cargar tabla de estadísticas
            cargarTablaEstadisticas(data.tabla);
        } else {
            console.error('Error al cargar datos del mapa:', data.error);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}

function mostrarInfo(municipioId, event) {
    const tooltip = document.getElementById('tooltip-municipio');
    const config = configuracionesMunicipios[municipioId];
    
    // Obtener el nombre legible del municipio desde el mismo objeto de configuración
    const nombreMunicipio = config ? config.municipio_nombre : municipioId.replace(/([A-Z])/g, ' $1').trim();

    document.getElementById('tooltip-nombre').textContent = nombreMunicipio;

    if (config) {
        document.getElementById('tooltip-info').textContent = config.informacion || 'Sin información disponible.';
        const imagen = document.getElementById('tooltip-imagen');
        if (config.imagen_url) {
            imagen.src = config.imagen_url;
            imagen.style.display = 'block';
        } else {
            imagen.style.display = 'none';
        }
    } else {
        document.getElementById('tooltip-info').textContent = 'Sin información configurada.';
        document.getElementById('tooltip-imagen').style.display = 'none';
    }
    
    tooltip.style.display = 'block';
    moverTooltip(event);
}

function ocultarInfo() {
    document.getElementById('tooltip-municipio').style.display = 'none';
}

function moverTooltip(event) {
    const tooltip = document.getElementById('tooltip-municipio');
    tooltip.style.left = (event.pageX + 15) + 'px';
    tooltip.style.top = (event.pageY + 15) + 'px';
}

function cargarTablaEstadisticas(tablaDatos) {
    const container = document.getElementById('tabla-estadisticas');
    
    if (!tablaDatos || !tablaDatos.datos || tablaDatos.datos.length === 0) {
        container.innerHTML = '<p>No hay datos estadísticos disponibles.</p>';
        return;
    }
    
    let tablaHTML = '<table class="stats-table"><tbody>';
    
    // El JSON ya viene parseado desde la API
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