document.addEventListener("DOMContentLoaded", function() {
    // Se ejecuta al cargar index.html
    obtenerDatosInfluxDB();

});

function insertarAlertaDB(datosFormulario) {
    // Realizar una solicitud HTTP POST al servidor Flask
    fetch('/mail/agregar_dato', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datosFormulario)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Hubo un problema al enviar los datos.');
        }
        return response.text();
    })
    .then(data => {
        console.log("Exito al actualizar la alerta"); // Mensaje de confirmación del servidor
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.getElementById('formulario-alerta').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar que se envíe el formulario de la manera tradicional

    // Recoger los datos del formulario
    let nombre = document.getElementById('nombre').value;
    let maquina = document.getElementById('select-maquinas').value
    let correo = document.getElementById('correo').value;
    let temperatura = document.getElementById('temperatura').value;
    let humedad = document.getElementById('humedad').value;

    // Crear un objeto con los datos del formulario
    let datosFormulario = {
        nombre: nombre,
        maquina: maquina,
        correo: correo,
        temperatura: temperatura,
        humedad: humedad
    };
    console.log(datosFormulario)
    insertarAlertaDB(datosFormulario)

});

function obtenerDatosInfluxDB() {
    fetch('/mail/obtener_datos')
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
            console.log(error)
        });
}

function mostrarMaquinasEnPantalla(data) {
    var select = document.getElementById("select-maquinas");
    // Limpiar select antes de agregar nuevos datos
    select.innerHTML = "";

    // Verificar si no hay máquinas conectadas
    if (Object.keys(data).length === 0) {
        var opcion = document.createElement("option");
        opcion.textContent = "No se detectan máquinas conectadas";
        opcion.disabled = true;
        opcion.selected = true;
        select.appendChild(opcion);
        return;
    }

    // Iterar sobre las claves del diccionario 'data'
    Object.keys(data).forEach(function(key) {
        // Crear una nueva opción
        var opcion = document.createElement("option");
        opcion.value = key; // Valor de la opción (nombre de la máquina)
        opcion.textContent = key; // Texto de la opción (nombre de la máquina)

        // Agregar la opción al select
        select.appendChild(opcion);
    });
}

