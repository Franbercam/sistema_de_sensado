from flask import Blueprint, render_template, jsonify
from ..utils import tcp_connection as rb
from ..database import influxdb_controller as db

main = Blueprint('index_blueprint', __name__)

@main.route('/')
def index():
    RB1_HOST = '169.254.249.146'
    RB1_PORT = 8888

    datos_sensor = rb.conectar_servidor(RB1_HOST,RB1_PORT)
    sensor_ip=datos_sensor[0]
    sensor_datos_rb=(datos_sensor[1]).split(",")
    sensor_datos = sensor_datos_rb[0]
    sensor_rb = sensor_datos_rb[1]  

    return (render_template("index.html",IP_SENSOR=sensor_ip,DATOS_SENSOR=sensor_datos,RB_SENSOR=sensor_rb,LINEA=datos_sensor))
    

@main.route('/insertar_datos', methods=['POST'])
def insertar_datos_en_influx():
    RB1_HOST = '169.254.249.146'
    RB1_PORT = 8888
    # Conecta con el servidor TCP y obtén los datos
    datos_rb = rb.conectar_servidor(RB1_HOST,RB1_PORT)
    
    # Extrae los valores de humedad, temperatura e ID del servidor
    humedad = float(datos_rb[1].split('\t')[0].split(' ')[1])
    temperatura = float(datos_rb[1].split('\t')[1].split(' ')[1])
    rb_id = datos_rb[1].split(',')[-1].strip()

    # Conecta con InfluxDB
    cliente_influx = db.conectar_influxdb()
    
    # Inserta los datos en InfluxDB
    db.insertar_datos(cliente_influx, rb_id,temperatura,humedad)

    return 'Datos insertados en InfluxDB correctamente'


@main.route('/leer_datos/<rb_id>', methods=['GET'])
def leer_datos_desde_influx(rb_id):
    try:
        cliente_influx = db.conectar_influxdb()
        datos = db.leer_datos(cliente_influx, rb_id)
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500