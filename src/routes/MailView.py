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


    # Validar que se recibieron todos los campos requeridos
    if not all([nombre, maquina, email, temperatura_max, temperatura_min, humedad_max, humedad_min]):
        return jsonify({'error': 'Faltan campos requeridos'}), 400  # Bad request

    # Insertar los datos en la base de datos SQLite
    alert.add_alert_db(nombre, maquina, email, temperatura_max, temperatura_min, humedad_max, humedad_min)

    return jsonify({'message': 'Datos agregados correctamente'}), 200  # OK

@main.route('/obtener_datos', methods=['GET'])
def obtener_datos():
    datos = db.get_data_db()

    return (datos)
