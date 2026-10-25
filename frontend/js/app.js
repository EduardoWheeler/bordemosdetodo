const API_URL = 'http://127.0.0.1:8000/api/parches';

async function cargarCatalogo() {
    const contenedor = document.getElementById('catalogo');

    try {
        const respuesta = await fetch(API_URL);

        if (!respuesta.ok) {
            throw new Error(`Error en la respuesta del servidor: ${respuesta.status}`);
        }

        const parches = await respuesta.json();
        contenedor.innerHTML = '';

        if (parches.length === 0) {
            contenedor.innerHTML = '<p class="mensaje-carga">No hay parches disponibles en el catálogo.</p>';
            return;
        }

        parches.forEach(parche => {
            const tarjeta = crearTarjetaParche(parche);
            contenedor.appendChild(tarjeta);
        });

    } catch (error) {
        console.error('Error al conectar con la API:', error);
        contenedor.innerHTML = `
            <p class="mensaje-error">
                No se pudo conectar con el servidor backend.<br>
                Asegúrate de que la API esté corriendo en ${API_URL}
            </p>
        `;
    }
}


/**
 * Crea un elemento DOM representando una tarjeta de parche.
 * @param {Object} parche - Objeto con la información del parche retornado por la API.
 * @returns {HTMLElement} Elemento div estructurado de la tarjeta.
 */
function crearTarjetaParche(parche) {
    const card = document.createElement('div');
    card.className = 'card-parche';

    card.innerHTML = `
        <h3>${parche.nombre}</h3>
        <p class="descripcion">${parche.descripcion || 'Sin descripción disponible.'}</p>
        <div class="detalles">
            <span class="precio">$${parche.precio}</span>
            <span class="stock">Stock: ${parche.stock}</span>
        </div>
    `;

    return card;
}


document.addEventListener('DOMContentLoaded', cargarCatalogo);