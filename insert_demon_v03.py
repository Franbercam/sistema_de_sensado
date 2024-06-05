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
                print("mio:", data.decode('UTF-8'))
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
            .tag("maquina", data_list["nombre"]) \
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
    required_fields = ["nombre", "ubicacion", "temperatura", "humedad", "ip"]
    return all(data.get(field) is not None for field in required_fields)

def data_parsing(data):
    humedad = None
    temperatura = None
    nombre = None
    ubicacion = None
    ip = data[0]

    try:
        nombre, ubicacion, *sensor_data = data[1].split(',')
        if sensor_data:
            sensor_info = ','.join(sensor_data).strip().split('\t')
            for item in sensor_info:
                if 'Humedad' in item:
                    humedad = float(item.split(':')[1].strip().split()[0][:-1])
                elif 'Temperatura' in item:
                    temperatura = float(item.split(':')[1].strip().split()[0])

    except ValueError as e:
        logging.error(f"Error al analizar los datos: {e}")

    return {"nombre": nombre, "ubicacion": ubicacion, "temperatura": temperatura, "humedad": humedad, "ip": ip}

def buffer_process(RB1_HOST, RB1_PORT):
    while True:
        try:
            data = conectar_servidor(RB1_HOST, RB1_PORT)
            logging.info(f"Datos recibidos del servidor: {data}")

            if "Error" in data[1]:
                logging.warning(f"Error al conectar con el servidor: {data[1]}")
                time.sleep(5)
                continue

            parse_data = data_parsing(data)
            logging.info(f"Datos analizados: {parse_data}")

            if is_healthy(parse_data):
                check_measure_to_email(parse_data)
                insertar_datos(parse_data)
            else:
                logging.warning("Datos no saludables recibidos")

            time.sleep(5)
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
        if data["nombre"] == alert_rb:
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
