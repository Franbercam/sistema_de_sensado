document.addEventListener("DOMContentLoaded", function() {
    // Se ejecuta al cargar index.html
    obtenerDatosInfluxDB();

     // Agregar evento al botón cerrar
     var botonCerrar = document.getElementById("cerrar-detalles");
     botonCerrar.addEventListener("click", function() {
        ocultarDetallesMaquina();
     });
});


function obtenerDatosInfluxDB() {
    fetch('/obtener_datos')
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
        });
}

function mostrarMaquinasEnPantalla(data) {
    var tabla = document.getElementById("tabla-maquinas");
    // Limpiar tabla antes de agregar nuevos datos
    tabla.innerHTML = "";

    // Crear fila de encabezado si aún no existe
    if (tabla.getElementsByTagName('tr').length === 0) {
        var encabezado = tabla.insertRow();
        var th1 = document.createElement("th");
        th1.textContent = "Máquinas conectadas";
        var th2 = document.createElement("th");
        th2.textContent = "Información";
        encabezado.appendChild(th1);
        encabezado.appendChild(th2);
    }

    // Iterar sobre las claves del diccionario 'data'
    Object.keys(data).forEach(function(key) {
        // Obtener el valor asociado a la clave actual
        var value = data[key];

        // Crear una nueva fila
        var fila = tabla.insertRow();

        // Insertar celdas con los datos de la máquina
        var celdaNombre = fila.insertCell();
        celdaNombre.textContent = key; // Nombre de la máquina

        var celdaInformacion = fila.insertCell();
        // Crear un botón "Ver" y agregarlo a la celda de información
        var botonVer = document.createElement("button");
        botonVer.textContent = "Ver";
        celdaInformacion.appendChild(botonVer);

        // Agregar un evento al botón "Ver" para manejar su clic
        botonVer.addEventListener("click", function() {
            // Mostrar detalles de la máquina seleccionada
            mostrarDetallesMaquina(key, value);
        });
    });
}

/*
function mostrarDetallesMaquina(nombre, detalles) {
    var detallesMaquina = document.getElementById("detalles-maquina");
    var contenedorDetalles = document.getElementById("contenedor-detalles");

    // Mostrar área de detalles
    detallesMaquina.style.display = "block";

    // Mostrar nombre y detalles de la máquina
    contenedorDetalles.innerHTML = "<h2>" + nombre + "</h2>" + "<p>" + JSON.stringify(detalles) + "</p>";
}
*/

function mostrarDetallesMaquina(nombre, detalles) {
    var detallesMaquina = document.getElementById("detalles-maquina");

    // Mostrar área de detalles
    detallesMaquina.style.display = "block";

    // Mostrar nombre y detalles de la máquina
    var contenedorDetalles = document.getElementById("contenedor-detalles");
    contenedorDetalles.innerHTML = "<h2>" + nombre + "</h2>" + "<p>" + JSON.stringify(detalles) + "</p>";

    // Agregar la clase para mostrar los detalles
    var sensor = document.querySelector('.sensor');
    sensor.classList.add('mostrar-detalles');
}

function ocultarDetallesMaquina() {
    var detallesMaquina = document.getElementById("detalles-maquina");

    // Ocultar área de detalles
    detallesMaquina.style.display = "none";

    // Quitar la clase que muestra los detalles
    var sensor = document.querySelector('.sensor');
    sensor.classList.remove('mostrar-detalles');
}

