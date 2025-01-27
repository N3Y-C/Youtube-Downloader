let checkProgressInterval;

function toggleTheme() {
    document.body.dataset.theme = 
        document.body.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', document.body.dataset.theme);
}

async function obtenerMetadatos() {
    const url = document.getElementById('url').value;
    try {
        const response = await axios.post('/metadatos', 
            { url: url },
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );
        
        if (response.data.error) {
            throw new Error(response.data.error);
        }
        mostrarInfoVideo(response.data);
    } catch (error) {
        alert(error.message || 'Error al obtener metadatos');
    }
}

function mostrarInfoVideo(metadata) {
    const infoDiv = document.getElementById('info-video');
    infoDiv.classList.remove('hidden');
    
    document.getElementById('titulo').textContent = metadata.titulo;
    document.getElementById('duracion').textContent = metadata.duracion;
    document.getElementById('resolucion').textContent = metadata.resolucion;
    document.getElementById('thumbnail').src = metadata.thumbnail;
}

async function iniciarDescarga() {
    const url = document.getElementById('url').value;
    document.getElementById('progreso').classList.remove('hidden');
    
    try {
        await axios.post('/descargar', 
            { url: url },
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );
        checkProgressInterval = setInterval(verificarDescargaCompleta, 1000);
    } catch (error) {
        alert(error.response?.data?.error || 'Error en la descarga');
    }
}

async function verificarDescargaCompleta() {
    try {
        const response = await axios.get('/progreso');
        const progreso = response.data;
        
        // Actualizar UI
        actualizarProgresoUI(progreso);
        
        // Verificar si la descarga está completa
        if (progreso.estado === 'completado') {
            clearInterval(checkProgressInterval);
            // Esperar 2 segundos adicionales para asegurar el merge
            setTimeout(() => {
                window.location.href = '/descargar-archivo';
            }, 2000);
        }
    } catch (error) {
        console.error('Error al obtener progreso:', error);
    }
}

function actualizarProgresoUI(progreso) {
    // Limpiar y formatear valores
    const porcentajeLimpio = progreso.porcentaje.replace(/\s+/g, ' ');
    const velocidadLimpia = formatearVelocidad(progreso.velocidad);
    const tiempoLimpio = progreso.tiempo ? `ETA: ${progreso.tiempo}` : 'ETA: --:--';

    document.getElementById('porcentaje').textContent = porcentajeLimpio;
    document.getElementById('velocidad').textContent = velocidadLimpia;
    document.getElementById('tiempo').textContent = tiempoLimpio;
    
    // Actualizar barra de progreso
    const porcentajeMatch = porcentajeLimpio.match(/\d+\.?\d*/);
    const porcentajeNumero = porcentajeMatch ? parseFloat(porcentajeMatch[0]) : 0;
    const progressFill = document.querySelector('.progress-fill');
    progressFill.style.width = `${porcentajeNumero}%`;
}

function formatearVelocidad(velocidad) {
    if (!velocidad) return '0.00 B/s';
    
    const matches = velocidad.match(/(\d+\.?\d*)\s*([KM]?iB)\/s/);
    if (matches) {
        return `${parseFloat(matches[1]).toFixed(2)} ${matches[2]}/s`;
    }
    return velocidad;
}

// Inicialización
document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
const savedTheme = localStorage.getItem('theme') || 'dark';
document.body.dataset.theme = savedTheme;