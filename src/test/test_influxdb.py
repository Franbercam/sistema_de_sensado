import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUXDB_TOKEN = 'YytQyoZl4naJMXTQwwFYCxDAoVEFME_A24YeX7g0qikyyU4uLi8APMgjgFgaNNRskWQw-bJa42ANoFutXadkww=='

token = INFLUXDB_TOKEN
org = "Universidad de Sevilla"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="bucket_prueba"


write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="Universidad de Sevilla", record=point)
  time.sleep(1) # separate points by 1 second


query_api = write_client.query_api()

query = """from(bucket: "sistema_de_sensado")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "my_measurement")
 |> filter(fn: (r) => r._field == "humedad")"""
tables = query_api.query(query, org="Universidad de Sevilla")

def get_data_by_name_db(name):
    try:
        query = f"""
        from(bucket: "sistema_de_sensado")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "my_measurement" and r.maquina == "{name}")
        |> tz(tz: "America/Chicago")
        """
        tables = query_api.query(query, org="Universidad de Sevilla")

        data = []
        for table in tables:
            for record in table.records:
                data.append(str(record))

      
        return data

    except Exception as e:
        return f"An error occurred: {e}"

    
print(get_data_by_name_db("rb1"))


