import time

from ..utils import tcp_connection as rb
from ..database import influxdb_controller as db


RB1_HOST = '169.254.249.146'
RB1_PORT = 8888

def buffer_process(RB1_HOST,RB1_PORT):
    while True:
        
        data = rb.conectar_servidor(RB1_HOST,RB1_PORT) #Comienza a recibir mediciones
        time.sleep(5)  # Delay del sensor (dht11)
        
        parse_data = data_parsing(data)
        
        if is_healthy(parse_data):        
            db.insertar_datos(parse_data)


def is_healthy(data_list):
     return all(element is not None for element in data_list)

def data_parsing(data):
    humedad = None
    temperatura = None
    id = None
    ip = None

    ip = data[0]
    id = data[1].split(',')[-1].strip()
    data_list = data[1].strip().split('\t')

    # Extraer los valores de humedad, temperatura e ID
    for item in data_list:
        if 'Humedad' in item:
            humedad = float(item.split(':')[1].strip().split()[0][:-1])  # Eliminar el símbolo '%' al final
        elif 'Temperatura' in item:
            temperatura = float(item.split(':')[1].strip().split()[0])  

    return {"id": id, "temperatura": temperatura, "humedad": humedad, "ip": ip}


if __name__ == '__main__':
    buffer_process(RB1_HOST,RB1_PORT)