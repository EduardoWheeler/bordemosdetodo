const API_URL = 'http://127.0.0.1:8000/api/parches';
const API_PEDIDOS_URL = 'http://127.0.0.1:8000/api/pedidos';

let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

document.addEventListener('DOMContentLoaded', () => {
    cargarCatalogo();
    actualizarContadorCarrito();

    const btnCarrito = document.getElementById('btn-carrito');
    const modalCarrito = document.getElementById('modal-carrito');
    const cerrarModal = document.getElementById('cerrar-modal');
    const btnProcesar = document.getElementById('btn-procesar-pedido');

    btnCarrito.addEventListener('click', () => {
        renderizarCarrito();
        modalCarrito.classList.remove('oculto');
    });

    cerrarModal.addEventListener('click', () => {
        modalCarrito.classList.add('oculto');
    });

    window.addEventListener('click', (e) => {
        if (e.target === modalCarrito) {
            modalCarrito.classList.add('oculto');
        }
    });

    btnProcesar.addEventListener('click', enviarPedido);
});

/**
 * Obtiene los parches de la API y dibuja el catálogo de forma segura
 */
async function cargarCatalogo() {
    const contenedor = document.getElementById('catalogo');

    try {
        const respuesta = await fetch(API_URL);
        if (!respuesta.ok) throw new Error('error al conectar con el servidor');

        const parches = await respuesta.json();
        contenedor.innerHTML = '';

        if (parches.length === 0) {
            contenedor.innerHTML = '<p class="mensaje-carga">no hay parches disponibles.</p>';
            return;
        }

        parches.forEach(parche => {
            const card = document.createElement('div');
            card.className = 'card-parche';
            
            card.innerHTML = `
                <h3>${parche.nombre}</h3>
                <p class="descripcion">${parche.descripcion || 'sin descripcion.'}</p>
                <div class="card-info">
                    <span class="precio">$${parche.precio}</span>
                    <span class="stock">stock: ${parche.stock}</span>
                </div>
                <button class="btn-agregar" data-id="${parche.id}">agregar al carrito</button>
            `;

            // Agregar el evento de forma segura sin romper cadenas HTML
            const btnAgregar = card.querySelector('.btn-agregar');
            btnAgregar.addEventListener('click', () => agregarAlCarrito(parche));

            contenedor.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        contenedor.innerHTML = '<p class="mensaje-error">error al conectar con la api backend.</p>';
    }
}

/**
 * Agrega un producto al carrito o incrementa su cantidad
 */
function agregarAlCarrito(parche) {
    const itemExistente = carrito.find(item => item.parche_id === parche.id);

    if (itemExistente) {
        if (itemExistente.cantidad < parche.stock) {
            itemExistente.cantidad++;
        } else {
            alert('no hay mas stock disponible para este parche.');
            return;
        }
    } else {
        if (parche.stock > 0) {
            carrito.push({
                parche_id: parche.id,
                nombre: parche.nombre,
                precio: parche.precio,
                cantidad: 1,
                stock_max: parche.stock
            });
        } else {
            alert('producto sin stock.');
            return;
        }
    }

    guardarCarrito();
    actualizarContadorCarrito();
    alert(`se agrego "${parche.nombre}" al carrito.`);
}

function guardarCarrito() {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

function actualizarContadorCarrito() {
    const contador = document.getElementById('contador-carrito');
    const totalItems = carrito.reduce((acc, item) => acc + item.cantidad, 0);
    contador.textContent = totalItems;
}

function renderizarCarrito() {
    const listaCarrito = document.getElementById('lista-carrito');
    const totalCarrito = document.getElementById('total-carrito');
    
    listaCarrito.innerHTML = '';

    if (carrito.length === 0) {
        listaCarrito.innerHTML = '<p>el carrito esta vacio.</p>';
        totalCarrito.textContent = '$0.00';
        return;
    }

    let subtotalGeneral = 0;

    carrito.forEach(item => {
        const subtotalItem = item.precio * item.cantidad;
        subtotalGeneral += subtotalItem;

        const div = document.createElement('div');
        div.className = 'item-carrito';
        div.innerHTML = `
            <span>${item.nombre} (x${item.cantidad})</span>
            <span>$${subtotalItem.toFixed(2)}</span>
        `;
        listaCarrito.appendChild(div);
    });

    totalCarrito.textContent = `$${subtotalGeneral.toFixed(2)}`;
}

async function enviarPedido() {
    const nombre = document.getElementById('nombre-cliente').value.trim();
    const email = document.getElementById('email-cliente').value.trim();

    if (!nombre || !email) {
        alert('por favor completa tu nombre y email.');
        return;
    }

    if (carrito.length === 0) {
        alert('el carrito esta vacio.');
        return;
    }

    const payload = {
        nombre_cliente: nombre,
        email_cliente: email,
        items: carrito.map(item => ({
            parche_id: item.parche_id,
            cantidad: item.cantidad
        }))
    };

    try {
        const respuesta = await fetch(API_PEDIDOS_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(resultado.detail || 'error al procesar la compra.');
        }

        alert(`¡compra exitosa! total pagado: $${resultado.total_compra}`);
        
        carrito = [];
        guardarCarrito();
        actualizarContadorCarrito();
        document.getElementById('modal-carrito').classList.add('oculto');
        cargarCatalogo();

    } catch (error) {
        console.error(error);
        alert(`hubo un error: ${error.message}`);
    }
}