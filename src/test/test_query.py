import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUXDB_TOKEN = 'YytQyoZl4naJMXTQwwFYCxDAoVEFME_A24YeX7g0qikyyU4uLi8APMgjgFgaNNRskWQw-bJa42ANoFutXadkww=='
token = INFLUXDB_TOKEN
org = "Universidad de Sevilla"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
query_api = write_client.query_api()

query = """from(bucket: "sistema_de_sensado")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "my_measurement")
 |> filter(fn: (r) => r._field == "humedad")"""
tables = query_api.query(query, org="Universidad de Sevilla")

for table in tables:
  for record in table.records:
    print(record)
