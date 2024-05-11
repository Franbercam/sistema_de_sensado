import time
import socket
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuración de InfluxDB
INFLUXDB_TOKEN = 'YytQyoZl4naJMXTQwwFYCxDAoVEFME_A24YeX7g0qikyyU4uLi8APMgjgFgaNNRskWQw-bJa42ANoFutXadkww=='
INFLUXDB_ORG = "Universidad de Sevilla"
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_BUCKET = "sistema_de_sensado"

# Crear cliente y API de escritura para InfluxDB
write_client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

def conectar_servidor(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection_result = client_socket.connect_ex((server_host, server_port))
        if connection_result == 0:
            data = client_socket.recv(1024)
            if not data:
                return [server_host, "No hay lectura del sensor"]
            else:
                return [server_host, data.decode('UTF-8')]
        else:
            return [server_host, f"Código de error: {connection_result}"]
    except Exception as e:
        return [server_host, f"Error: {e}"]
    finally:
        client_socket.close()

def insertar_datos(data_list):
    #print(data_list)
    try:
        point = Point("my_measurement") \
            .tag("maquina", data_list["id"]) \
            .field("temperatura", data_list["temperatura"]) \
            .field("humedad", data_list["humedad"]) \
            .field("ip", data_list["ip"])
        print(point)
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    except Exception as e:
        print(f"Error al insertar datos en InfluxDB: {e}")
        raise

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

    for item in data_list:
        if 'Humedad' in item:
            humedad = float(item.split(':')[1].strip().split()[0][:-1])
        elif 'Temperatura' in item:
            temperatura = float(item.split(':')[1].strip().split()[0])

    return {"id": id, "temperatura": temperatura, "humedad": humedad, "ip": ip}

def buffer_process(RB1_HOST, RB1_PORT):
    while True:
        data = conectar_servidor(RB1_HOST, RB1_PORT)
        time.sleep(5)
        parse_data = data_parsing(data)
        if is_healthy(parse_data):
            insertar_datos(parse_data)

if __name__ == '__main__':
    RB1_HOST = '169.254.249.146'
    RB1_PORT = 8888
    buffer_process(RB1_HOST, RB1_PORT)