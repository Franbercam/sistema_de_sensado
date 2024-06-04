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
        
        // Acceder al segundo elemento del array para obtener el nombre
        if (alerta.length > 1) {
            alertaNombre.textContent = alerta[1];
        } else {
            console.warn('El objeto alerta no tiene un segundo elemento:', alerta);
            alertaNombre.textContent = 'Nombre desconocido';
        }
        
        const botonBorrar = document.createElement('button');
        botonBorrar.textContent = 'Borrar';
        botonBorrar.classList.add('boton-borrar');
        botonBorrar.onclick = () => borrarAlerta(alerta[1]); // Usar el nombre para borrar
        
        alertaDiv.appendChild(alertaNombre);
        alertaDiv.appendChild(botonBorrar);
        listaAlertas.appendChild(alertaDiv);
    });
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