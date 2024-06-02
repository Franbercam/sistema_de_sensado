import time
import socket

import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from src.database import local_db_controller as alert
from src.services import mail_services as mail


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

def is_healthy(data):
    return data["temperatura"]!=None and data["humedad"] != None and data["id"] !=None and data["ip"] != None

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
        parse_data = data_parsing(data) #{'id': 'rb1', 'temperatura': 24.5, 'humedad': 51.0, 'ip': '169.254.249.146'}
        if is_healthy(parse_data):
            check_measure_to_email(parse_data)
            insertar_datos(parse_data)



def get_alert():
   alerts = alert.get_alerts_db()
   return alerts

def check_measure_to_email(data):
    alerts_list = get_alert()
    
    
    if not isinstance(alerts_list, list):
        print("No alerts found.")
        return
    
    for alert in alerts_list:
        print(alert)
        _, alert_nombre, alert_rb, alert_mail, alert_temp_max, alert_temp_min, alert_hum_max, alert_hum_min = alert
        if data["id"] == alert_rb:
            temp_exceeds_max = data["temperatura"] > alert_temp_max
            temp_exceeds_min = data["temperatura"] < alert_temp_min
            hum_exceeds_max = data["humedad"] > alert_hum_max
            hum_exceeds_min = data["humedad"] < alert_hum_min
            
            if temp_exceeds_max or temp_exceeds_min or hum_exceeds_max or hum_exceeds_min:
                mail.send_alert(alert)
                alert.add_alert_issued_db(alert_nombre, alert_rb, alert_mail, alert_temp_max, alert_temp_min, alert_hum_max, alert_hum_min)
                alert.delete_alert_db(alert_nombre)

   
    

if __name__ == '__main__':
    RB1_HOST = '169.254.249.146'
    RB1_PORT = 8888
    buffer_process(RB1_HOST, RB1_PORT)
    

