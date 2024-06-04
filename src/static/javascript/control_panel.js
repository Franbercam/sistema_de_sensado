document.addEventListener("DOMContentLoaded", function() {
    // Se ejecuta al cargar index.html
    obtenerDatosInfluxDB();
    obtenerDatosSQlite();

});


function obtenerDatosInfluxDB() {
    fetch('/control_panel/obtener_datos')
        .then(response => {
            if (!response.ok) {
                console.log(response);
                throw new Error('Error al obtener datos de InfluxDB');
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos obtenidos de InfluxDB:', data);
            mostrarMaquinasEnPantalla(data); // Llamar a la función para mostrar máquinas en pantalla
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarInformacionBD()
        });
}

function mostrarMaquinasEnPantalla(data) {
    var tabla = document.getElementById("tabla-maquinas");
    tabla.innerHTML = "";

    if (tabla.getElementsByTagName('tr').length === 0) {
        var encabezado = tabla.insertRow();
        var th1 = document.createElement("th");
        th1.textContent = "Máquinas conectadas";
        var th2 = document.createElement("th");
        th2.textContent = "Información";
        encabezado.appendChild(th1);
        encabezado.appendChild(th2);
    }

    if (Object.keys(data).length === 0) {
        var fila = tabla.insertRow();
        var celdaMensaje = fila.insertCell();
        celdaMensaje.colSpan = 2;
        celdaMensaje.textContent = "No se detectan máquinas conectadas";
        celdaMensaje.style.textAlign = "center";
        return;
    }

    Object.keys(data).forEach(function(key) {
        var value = data[key];
        var fila = tabla.insertRow();

        var celdaNombre = fila.insertCell();
        celdaNombre.textContent = key;

        var celdaInformacion = fila.insertCell();
        var botonVer = document.createElement("button");
        botonVer.textContent = "Ver";
        celdaInformacion.appendChild(botonVer);

        var botonGrafica = document.createElement("button");
        botonGrafica.textContent = "Gráfica";
        celdaInformacion.appendChild(botonGrafica);

        botonVer.addEventListener("click", function() {
            window.location.href = `/raspinfo?machine_name=${encodeURIComponent(key)}`;
        });
        botonGrafica.addEventListener("click", function() {
            window.location.href = `/graph?machine_name=${encodeURIComponent(key)}`;
        });
    });
}



function obtenerDatosSQlite() {
    fetch('/control_panel/obtener_alertas')
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
    fetch('/control_panel/borrar_alerta', {
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


