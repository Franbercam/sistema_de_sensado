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

    if (Object.keys(data).length === 0) {
        var fila = tabla.insertRow();
        var celdaMensaje = fila.insertCell();
        celdaMensaje.colSpan = 2;
        celdaMensaje.textContent = "No se detectan máquinas conectadas";
        celdaMensaje.style.textAlign = "center";
        return;
    }

    Object.keys(data).forEach(function(lugar) {
        var maquinas = data[lugar];
        var filaLugar = tabla.insertRow();
        var celdaLugar = filaLugar.insertCell();
        celdaLugar.colSpan = 2;
        celdaLugar.textContent = lugar;
        celdaLugar.style.fontWeight = "bold";
        celdaLugar.style.textAlign = "center";

        Object.keys(maquinas).forEach(function(maquina) {
            var detalles = maquinas[maquina];
            var filaMaquina = tabla.insertRow();

            var celdaMaquina = filaMaquina.insertCell();
            celdaMaquina.textContent = maquina;

            var celdaBotones = filaMaquina.insertCell();
            
            // Crear botón Ver
            var botonVer = document.createElement("a");
            botonVer.textContent = "Ver";
            botonVer.href = `/raspinfo?machine_name=${encodeURIComponent(maquina)}&location=${encodeURIComponent(lugar)}`;
            botonVer.target = "_blank";
            botonVer.className = "boton-sensor";
            celdaBotones.appendChild(botonVer);

            // Crear botón Gráfica
            var botonGrafica = document.createElement("a");
            botonGrafica.textContent = "Gráfica";
            botonGrafica.href = `/graph?machine_name=${encodeURIComponent(maquina)}&location=${encodeURIComponent(lugar)}`;
            botonGrafica.target = "_blank";
            botonGrafica.className = "boton-sensor";
            celdaBotones.appendChild(botonGrafica);
        });
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
    recuadroMantenimiento.textContent = "La base de datos se encuentra inaccesible. Por favor, compruebe su estado. ";
    
    // Insertar el recuadro en el lugar de la tabla
    var contenedor = document.getElementById("contenedor-tabla");
    contenedor.appendChild(recuadroMantenimiento);
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


