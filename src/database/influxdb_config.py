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
        client.create_database(INFLUXDB_DATABASE)
        #si la base de datos ya existe, create_database() simplemente no hará nada. Si la base de datos no existe, se creará automáticamente
        return client
    except Exception as e:
        print(f"Error al conectar con InfluxDB: {e}")
        sys.exit(1)


def insertar_datos(client, medicion, datos):
    json_body = [
        {
            "measurement": medicion,
            "fields": datos
        }
    ]
    
    client.write_points(json_body)