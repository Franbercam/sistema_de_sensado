from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from ..database import local_db_controller as alert
from ..services import influxdb_service as db

main = Blueprint('mail_blueprint', __name__, url_prefix='/mail')


@main.route('/')
@login_required
def index():   

    return (render_template("mail.html"))

@main.route('/agregar_dato', methods=['POST'])
def agregar_dato():
    # Obtener los datos del formulario en formato JSON
    data = request.json

    # Extraer los datos del formulario
    nombre = data.get('nombre')
    maquina = data.get('maquina')
    email = data.get('correo')  # El campo en el formulario se llama 'correo'
    temperatura_max = data.get('temperatura_max')
    temperatura_min = data.get('temperatura_min')
    humedad_max = data.get('humedad_max')
    humedad_min = data.get('humedad_min')




    # Insertar los datos en la base de datos SQLite
    alert.add_alert_db(nombre, maquina, email, temperatura_max, temperatura_min, humedad_max, humedad_min)

    return jsonify({'message': 'Datos agregados correctamente'}), 200  # OK

@main.route('/obtener_datos', methods=['GET'])
def obtener_datos():
    try:
        datos = db.get_data_db()

        # Flatten the data to have a list of machines with their locations
        flattened_data = {}
        for location, machines in datos.items():
            for machine, details in machines.items():
                flattened_data[machine] = {
                    "location": location,
                    "details": details
                }

        return jsonify(flattened_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
