from flask import Blueprint
from ..utils import TCP_connection as rb1

main = Blueprint('index_blueprint', __name__)

@main.route('/')

#server_host = '192.168.8.109' 
#server_port = 8888

def index():

    valor = rb1.conectar_servidor('192.168.8.109',8888)
    return valor
    #rb1.prueba()
    #rb1.conectar_servidor('192.168.8.109',8888)