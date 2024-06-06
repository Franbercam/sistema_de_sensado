import time
import socket
import logging

import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from src.database import local_db_controller as alert
from src.services import mail_services as mail

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    client_socket.settimeout(10)  # Añadir tiempo de espera
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
    except socket.timeout:
        return [server_host, "Tiempo de espera agotado al conectar con el servidor"]
    except Exception as e:
        return [server_host, f"Error: {e}"]
    finally:
        client_socket.close()

def insertar_datos(data_list):
    try:
        point = Point("my_measurement") \
            .tag("maquina", data_list["id"]) \
            .tag("ubicacion", data_list["ubicacion"]) \
            .field("temperatura", data_list["temperatura"]) \
            .field("humedad", data_list["humedad"]) \
            .field("ip", data_list["ip"])
        logging.info(point)
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    except Exception as e:
        logging.error(f"Error al insertar datos en InfluxDB: {e}")
        raise

def is_healthy(data):
    return data["temperatura"] is not None and data["humedad"] is not None and data["id"] is not None and data["ip"] is not None and data["ubicacion"] is not None

def data_parsing(data):
    humedad = None
    temperatura = None
    id = None
    ubicacion = None
    ip = None

    ip = data[0]
    split_data = data[1].strip().split(',')
    if len(split_data) >= 3:
        id = split_data[-2].strip()
        ubicacion = split_data[-1].strip()
        sensor_data = split_data[0].strip()

        data_list = sensor_data.split('\t')

        for item in data_list:
            if 'Humedad' in item:
                humedad = float(item.split(':')[1].strip().split()[0][:-1])
            elif 'Temperatura' in item:
                temperatura = float(item.split(':')[1].strip().split()[0])

    return {"id": id, "temperatura": temperatura, "humedad": humedad, "ip": ip, "ubicacion": ubicacion}

def buffer_process(RB1_HOST, RB1_PORT):
    while True:
        try:
            data = conectar_servidor(RB1_HOST, RB1_PORT)
            if "Error" in data[1]:
                logging.warning(f"Error al conectar con el servidor: {data[1]}")
                time.sleep(5)
                continue
            parse_data = data_parsing(data)
            if is_healthy(parse_data):
                check_measure_to_email(parse_data)
                insertar_datos(parse_data)
            else:
                logging.warning("Datos no saludables recibidos")
            time.sleep(5)  # Mover el sleep al final para no esperar si hay un error al conectar
        except Exception as e:
            logging.error(f"Error en buffer_process: {e}")
            time.sleep(5)

def get_alert():
   alerts = alert.get_alerts_db()
   return alerts

def check_measure_to_email(data):
    alerts_list = get_alert()

    if not isinstance(alerts_list, list):
        logging.info("No alerts found.")
        return
    
    for a in alerts_list:
        _, alert_nombre, alert_rb, alert_mail, alert_temp_max, alert_temp_min, alert_hum_max, alert_hum_min = a
        if data["id"] == alert_rb:
            
            temp_exceeds_max = data["temperatura"] > alert_temp_max
            temp_exceeds_min = data["temperatura"] < alert_temp_min
            hum_exceeds_max = data["humedad"] > alert_hum_max
            hum_exceeds_min = data["humedad"] < alert_hum_min
            
            if temp_exceeds_max or temp_exceeds_min or hum_exceeds_max or hum_exceeds_min:
                mail.send_alert(a)
                alert.add_alert_issued_db(alert_nombre, alert_rb, alert_mail, alert_temp_max, alert_temp_min, alert_hum_max, alert_hum_min)
                alert.delete_alert_db(alert_nombre)

if __name__ == '__main__':
    RB1_HOST = '169.254.249.146'
    RB1_PORT = 8888
    buffer_process(RB1_HOST, RB1_PORT)
