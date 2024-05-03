from influxdb import InfluxDBClient

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
        if not any(db['name'] == INFLUXDB_DATABASE for db in databases):
            client.create_database(INFLUXDB_DATABASE)
        return client
    except Exception as e:
        print(f"Error al conectar con InfluxDB: {e}")
        # Log de error o notificación
        raise  # Propagar la excepción para que sea manejada en el nivel superior

def insertar_datos(client, rb_id, temperatura, humedad):
    try:
        json_body = [
            {
                "measurement": rb_id,
                "fields": {
                    "temperatura": temperatura,
                    "humedad": humedad
                }
            }
        ]
        
        client.write_points(json_body)
    except Exception as e:
        print(f"Error al insertar datos en InfluxDB: {e}")
        # Log de error o notificación
        raise  # Propagar la excepción para que sea manejada en el nivel superior

def leer_datos(client, rb_id, limit=None):
    try:
        query = f'SELECT * FROM "{rb_id}"'
        if limit:
            query += f' LIMIT {limit}'
        
        result = client.query(query)
        return list(result.get_points())
    except Exception as e:
        print(f"Error al leer datos de InfluxDB: {e}")
        # Log de error o notificación
        raise  # Propagar la excepción para que sea manejada en el nivel superior