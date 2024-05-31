document.addEventListener("DOMContentLoaded", function() {
    // Se ejecuta al cargar index.html
    obtenerDatosInfluxDB();
    obtenerDatosSQlite();

     // Agregar evento al botón cerrar
     var botonCerrar = document.getElementById("cerrar-detalles");
     botonCerrar.addEventListener("click", function() {
        ocultarDetallesMaquina();
     });
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
            mostrarAlertasEnPantalla(data); // Llamar a la función para mostrar máquinas en pantalla
        })
        .catch(error => {
            console.error('Error:', error);
          
        });
}

function mostrarAlertasEnPantalla(data) {
    const listaAlertas = document.getElementById('lista-alertas');
    listaAlertas.innerHTML = ''; // Limpiar cualquier contenido existente

    if (!data || data.length === 0) {
        listaAlertas.innerHTML = '<p>Añada una alerta</p>';
        return;
    }

    data.forEach(alerta => {
        const alertaDiv = document.createElement('div');
        alertaDiv.classList.add('alerta');
        alertaDiv.textContent = alerta;
        listaAlertas.appendChild(alertaDiv);
    });
}

function mostrarInformacionBD() {
    var tabla = document.getElementById("tabla-maquinas");
    
    // Eliminar la tabla si existe
    if (tabla) {
        tabla.parentNode.removeChild(tabla);
    }
    
    // Crear el recuadro de mantenimiento
    var recuadroMantenimiento = document.createElement("div");
    recuadroMantenimiento.className = "recuadro-mantenimiento";
    recuadroMantenimiento.textContent = "La base de datos está en mantenimiento. Por favor, inténtelo más tarde.";
    
    // Insertar el recuadro en el lugar de la tabla
    var contenedor = document.getElementById("contenedor-tabla");
    contenedor.appendChild(recuadroMantenimiento);
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

    // Verificar si no hay máquinas conectadas
    if (Object.keys(data).length === 0) {
        var fila = tabla.insertRow();
        var celdaMensaje = fila.insertCell();
        celdaMensaje.colSpan = 2;
        celdaMensaje.textContent = "No se detectan máquinas conectadas";
        celdaMensaje.style.textAlign = "center";
        return;
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


function mostrarDetallesMaquina(nombre, detalles) {
    var detallesMaquina = document.getElementById("detalles-maquina");

    // Mostrar área de detalles
    detallesMaquina.style.display = "block";

    // Mostrar nombre y detalles de la máquina
    var contenedorDetalles = document.getElementById("contenedor-detalles");
    
    // Construir el HTML para los detalles de la máquina
    var htmlDetalles = "<h2 id='nombre-detalles'>" + nombre + "</h2>";

    // Crear tabla para mostrar detalles
    htmlDetalles += "<table border='1'><tr><th>Fecha y Hora</th><th>Temperatura</th><th>Humedad</th><th>IP</th></tr>";
    
    for (var key in detalles) {
        if (detalles.hasOwnProperty(key)) {
            var dato = detalles[key];
            htmlDetalles += "<tr><td>" + key + "</td><td>" + dato[0] + "</td><td>" + dato[1] + "</td><td>" + dato[2] + "</td></tr>";
        }
    }
    htmlDetalles += "</table>";

    contenedorDetalles.innerHTML = htmlDetalles;

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

