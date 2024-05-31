import re
from datetime import datetime
import influxdb_client

INFLUXDB_TOKEN = 'YytQyoZl4naJMXTQwwFYCxDAoVEFME_A24YeX7g0qikyyU4uLi8APMgjgFgaNNRskWQw-bJa42ANoFutXadkww=='
token = INFLUXDB_TOKEN
org = "Universidad de Sevilla"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org) 
query_api = write_client.query_api()

def get_data_db():
    try:
        query = """from(bucket: "sistema_de_sensado")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "my_measurement")
        """
        tables = query_api.query(query, org="Universidad de Sevilla")

        data = []
        for table in tables:
            for record in table.records:
                data.append(str(record))

        res = records_to_dict(data)
        return res

    except Exception as e:
        return (f"An error occurred: {e}")



def get_id(text):

    pattern = r"'maquina': '([^']*)'"
    match = re.search(pattern, text)

    if match:
        return match.group(1)
    else:
        return None
    

    
def get_datetime(text):
    pattern = r"_time': datetime\.datetime\((\d{4}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d+), tzinfo=tzutc\(\)\)"
    match = re.search(pattern, text)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        second = int(match.group(6))
        microsecond = int(match.group(7))
        
        return datetime(year, month, day, hour, minute, second, microsecond)
    else:
        return None

def extract_values(data_list, date):
    temperature = None
    humidity = None
    ip = None
    
    for data in data_list:
        if get_datetime(data) == date:
            value = re.search(r"'_value': (.*), '_field': '(.*)'", data)
            
            if value:
                field_value = value.group(1)                
                field_name = value.group(2)
                
                if (field_name.split(","))[0] == "temperatura'":
                    temperature = float(field_value)
                elif (field_name.split(","))[0] == "humedad'":
                    humidity = float(field_value)
                elif (field_name.split(","))[0] == "ip'":
                    ip = field_value
    
    return (temperature, humidity, ip)

def records_to_dict(data_list):
    res = dict()
    for data in data_list:
        id = get_id(data)
        
        if id not in res:            
            id_value = dict()
            time = get_datetime(data)
            id_value[str(time)] = extract_values(data_list,time)  

        else:
            time = get_datetime(data)
            id_value[str(time)] = extract_values(data_list,time)  

        res[id] = id_value
    
    return res

