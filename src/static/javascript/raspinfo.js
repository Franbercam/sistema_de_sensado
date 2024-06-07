document.addEventListener("DOMContentLoaded", function() {
    // Se ejecuta al cargar el .html
    obtenerDatosSQlite();

});

function recargarPagina() {
    location.reload();
  }
  
  setInterval(recargarPagina, 10000);

function obtenerDatosSQlite() {
    fetch('/raspinfo/obtener_alertas')
        .then(response => {
            if (!response.ok) {
                console.log(response);
                throw new Error('Error al obtener alertas de SQlite');
            }
            return response.json();
        })
        .then(data => {
            console.log('Alertas obtenidas de SQlite:', data);
            mostrarAlertasEnPantalla(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function mostrarAlertasEnPantalla(data) {
    const listaAlertas = document.getElementById('lista-alertas');
    listaAlertas.innerHTML = '';

    if (!data || data.length === 0) {
        listaAlertas.innerHTML = '<p>No se ha emitido ninguna alerta</p>';
        return;
    }

    data.forEach(alerta => {
        console.log('Procesando alerta:', alerta); // Depuración adicional
        const alertaDiv = document.createElement('div');
        alertaDiv.classList.add('alerta');
        
        const alertaNombre = document.createElement('span');
        
        if (alerta.length > 1) {
            const nombre = alerta[1];
            const tem_max = alerta[4];
            const tem_min = alerta[5];
            const hum_max = alerta[6];
            const hum_min = alerta[7];
            alertaNombre.textContent = nombre;

            // Crear botón para mostrar detalles
            const botonDetalles = document.createElement('button');
            botonDetalles.textContent = 'Ver';
            botonDetalles.classList.add('boton-detalles');
            botonDetalles.onclick = () => {
                mostrarDetalles(nombre, tem_max, tem_min, hum_max, hum_min);
            };

            // Crear botón para borrar alerta
            const botonBorrar = document.createElement('button');
            botonBorrar.textContent = 'Borrar';
            botonBorrar.classList.add('boton-borrar');
            botonBorrar.onclick = () => borrarAlerta(alerta[1]);

            // Crear contenedor para los botones
            const botonesDiv = document.createElement('div');
            botonesDiv.classList.add('botones');
            botonesDiv.appendChild(botonDetalles);
            botonesDiv.appendChild(botonBorrar);

            // Añadir elementos al contenedor de la alerta
            alertaDiv.appendChild(alertaNombre);
            alertaDiv.appendChild(botonesDiv);
        } else {
            console.warn('El objeto alerta no tiene los elementos esperados:', alerta);
            alertaNombre.textContent = 'Nombre desconocido';
            alertaDiv.appendChild(alertaNombre);
        }
        
        listaAlertas.appendChild(alertaDiv);
    });
}

function mostrarDetalles(nombre, tem_max, tem_min, hum_max, hum_min) {
    const modal = document.getElementById('detalle-modal');
    const modalContent = document.getElementById('detalle-modal-content');
    const modalNombre = document.getElementById('modal-nombre');
    const modalTemMax = document.getElementById('modal-tem-max');
    const modalTemMin = document.getElementById('modal-tem-min');
    const modalHumMax = document.getElementById('modal-hum-max');
    const modalHumMin = document.getElementById('modal-hum-min');
    
    modalNombre.textContent = nombre;
    modalTemMax.textContent = `Tem Máx: ${tem_max}`;
    modalTemMin.textContent = `Tem Mín: ${tem_min}`;
    modalHumMax.textContent = `Hum Máx: ${hum_max}`;
    modalHumMin.textContent = `Hum Mín: ${hum_min}`;
    
    modal.style.display = 'block';
}

function cerrarModal() {
    const modal = document.getElementById('detalle-modal');
    modal.style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('detalle-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}


function borrarAlerta(nombre) {
    fetch('/raspinfo/borrar_alerta', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre: nombre })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.message || 'Error al borrar la alerta');
            });
        }
        return response.json();
    })
    .then(data => {
        alert('Alerta borrada con éxito');
        location.reload();
    })
    .catch(error => {
        alert(`Error: ${error.message}`);
    });
}