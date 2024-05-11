import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS


INFLUXDB_TOKEN = 'YytQyoZl4naJMXTQwwFYCxDAoVEFME_A24YeX7g0qikyyU4uLi8APMgjgFgaNNRskWQw-bJa42ANoFutXadkww=='
INFLUXDB_ORG = "Universidad de Sevilla"
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_BUCKET="sistema_de_sensado"

write_client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

write_api = write_client.write_api(write_options=SYNCHRONOUS)

def insertar_datos(data_list):
    try:
        print(data_list)
        point = Point("my_measurement") \
        .tag("maquina", data_list["id"]) \
        .field("temperatura", data_list["temperatura"]) \
        .field("humedad", data_list["humedad"]) \
        .field("ip", data_list["ip"])
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

    except Exception as e:
        print(f"Error al insertar datos en InfluxDB: {e}")
        # Log de error o notificación
        raise  # Propagar la excepción para que sea manejada en el nivel superior
