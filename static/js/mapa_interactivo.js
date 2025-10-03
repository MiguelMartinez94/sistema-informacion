// ===============================
// static/js/mapa_interactivo.js
// ===============================

document.addEventListener('DOMContentLoaded', function() {
    const mapaContainer = document.getElementById('mapa-container');
    if (mapaContainer) {
        const mapaId = mapaContainer.dataset.mapaId;
        if (mapaId) {
            cargarDatosMapa(mapaId);
        }
    }

    const municipios = document.querySelectorAll('.municipio-path');
    municipios.forEach(municipio => {
        municipio.addEventListener('click', () => {
            const municipioId = municipio.id.replace('municipio-', '');
            seleccionarMunicipio(municipioId);
        });
    });
});

let mapaActual = null;
let municipioSeleccionado = null;
let configuracionesMunicipios = {};

async function cargarDatosMapa(mapaId) {
    try {
        const response = await fetch(`/api/mapa/${mapaId}`);
        const data = await response.json();

        if (data.success) {
            mapaActual = data;
            document.getElementById('mapa-nombre').textContent = data.mapa.nombre;
            document.getElementById('mapa-descripcion').textContent = data.mapa.descripcion;

            // Limpiar colores
            document.querySelectorAll('.municipio-path').forEach(path => {
                path.style.fill = ''; // Volver al color por defecto
            });

            // Aplicar configuraciones
            configuracionesMunicipios = {};
            data.municipios.forEach(config => {
                configuracionesMunicipios[config.municipio_id] = config;
                const el = document.getElementById(`municipio-${config.municipio_id}`);
                if (el) {
                    el.style.fill = config.color;
                }
            });

            // Cargar tabla
            cargarTabla(data.tabla);
        } else {
            console.error('Error al cargar el mapa:', data.error);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}

function seleccionarMunicipio(municipioId) {
    municipioSeleccionado = municipioId;

    // Resaltar selección
    document.querySelectorAll('.municipio-path').forEach(path => {
        path.classList.remove('seleccionado');
    });
    document.getElementById(`municipio-${municipioId}`).classList.add('seleccionado');

    mostrarInformacionMunicipio(municipioId);
}

function mostrarInformacionMunicipio(municipioId) {
    const infoPanel = document.getElementById('info-panel');
    const config = configuracionesMunicipios[municipioId];

    if (config) {
        infoPanel.innerHTML = `
            <h3>${config.municipio_nombre}</h3>
            <p>${config.informacion || 'No hay información disponible.'}</p>
            ${config.imagen_url ? `<img src="${config.imagen_url}" alt="${config.municipio_nombre}" style="max-width: 100%;">` : ''}
        `;
    } else {
        infoPanel.innerHTML = `
            <h3>${municipioId.replace(/([A-Z])/g, ' $1').trim()}</h3>
            <p>No hay configuración para este municipio en el mapa actual.</p>
        `;
    }
}

function cargarTabla(tablaData) {
    const tablaContainer = document.getElementById('tabla-container');
    if (tablaData && tablaData.datos) {
        let tablaHTML = '<table border="1"><tbody>';
        tablaData.datos.forEach(fila => {
            tablaHTML += '<tr>';
            fila.forEach(celda => {
                tablaHTML += `<td>${celda}</td>`;
            });
            tablaHTML += '</tr>';
        });
        tablaHTML += '</tbody></table>';
        tablaContainer.innerHTML = tablaHTML;
    } else {
        tablaContainer.innerHTML = '<p>No hay tabla de datos para este mapa.</p>';
    }
}