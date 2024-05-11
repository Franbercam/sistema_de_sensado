import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUXDB_TOKEN = 'HvRPKymduvyxAaOPwqFTY5VjXdxNtufcMXfsbzf2Tu3eNdlStHiMQOt4pHvBNCPVjwm6Mf5cOiqweM6_mw_P_A=='

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