from influxdb import InfluxDBClient
import sys

# Configuración de la conexión con InfluxDB
INFLUXDB_HOST = 'localhost'  
INFLUXDB_PORT = 8086
INFLUXDB_USER = 'admin'  
INFLUXDB_PASSWORD = 'admin'  
INFLUXDB_DATABASE = 'sistema_sensado' 



def conectar_influxdb():
    try:
        client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, username=INFLUXDB_USER, password=INFLUXDB_PASSWORD)
        # Verificar si la base de datos ya existe
        databases = client.get_list_database()
        if not any(db['sistema_sensado'] == INFLUXDB_DATABASE for db in databases):
            client.create_database(INFLUXDB_DATABASE)
        return client
    except Exception as e:
        print(f"Error al conectar con InfluxDB: {e}")
        # Log de error o notificación
        raise  # Propagar la excepción para que sea manejada en el nivel superior



def insertar_datos(client, medicion, datos):
    json_body = [
        {
            "measurement": medicion,
            "fields": datos
        }
    ]
    
    client.write_points(json_body)