from flask import Blueprint, render_template
from ..utils import TCP_connection as rb1

main = Blueprint('index_blueprint', __name__)

@main.route('/')



def index():
    RB1_HOST = '169.254.249.146'
    RB1_PORT = 8888

    datos_sensor = rb1.conectar_servidor(RB1_HOST,RB1_PORT)
    sensor_ip=datos_sensor[0]
    sensor_datos=datos_sensor[1]
    


    return (render_template("index.html",IP_SENSOR=sensor_ip,DATOS_SENSOR=sensor_datos))
    