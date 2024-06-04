import re
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash


data = [
    "FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 5, 9, 16, 21, 32, 655773, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 5, 9, 16, 31, 32, 655773, tzinfo=tzutc()), '_time': datetime.datetime(2024, 5, 9, 16, 31, 12, 573719, tzinfo=tzutc()), '_value': 37.0, '_field': 'humedad', '_measurement': 'my_measurement', 'maquina': 'rb1'}",
    "FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 5, 9, 16, 21, 32, 655773, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 5, 9, 16, 31, 32, 655773, tzinfo=tzutc()), '_time': datetime.datetime(2024, 5, 9, 16, 31, 17, 611439, tzinfo=tzutc()), '_value': 37.0, '_field': 'humedad', '_measurement': 'my_measurement', 'maquina': 'rb1'}",
    "FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 5, 9, 16, 21, 32, 655773, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 5, 9, 16, 31, 32, 655773, tzinfo=tzutc()), '_time': datetime.datetime(2024, 5, 9, 16, 31, 22, 630726, tzinfo=tzutc()), '_value': 37.0, '_field': 'humedad', '_measurement': 'my_measurement', 'maquina': 'rb1'}",
    "FluxRecord() table: 1, {'result': '_result', 'table': 1, '_start': datetime.datetime(2024, 5, 9, 16, 21, 32, 655773, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 5, 9, 16, 31, 32, 655773, tzinfo=tzutc()), '_time': datetime.datetime(2024, 5, 9, 16, 31, 12, 573719, tzinfo=tzutc()), '_value': '169.254.249.146', '_field': 'ip', '_measurement': 'my_measurement', 'maquina': 'rb1'}",
    "FluxRecord() table: 1, {'result': '_result', 'table': 1, '_start': datetime.datetime(2024, 5, 9, 16, 21, 32, 655773, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 5, 9, 16, 31, 32, 655773, tzinfo=tzutc()), '_time': datetime.datetime(2024, 5, 9, 16, 31, 17, 611439, tzinfo=tzutc()), '_value': '169.254.249.146', '_field': 'ip', '_measurement': 'my_measurement', 'maquina': 'rb1'}",
    "FluxRecord() table: 1, {'result': '_result', 'table': 1, '_start': datetime.datetime(2024, 5, 9, 16, 21, 32, 655773, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 5, 9, 16, 31, 32, 655773, tzinfo=tzutc()), '_time': datetime.datetime(2024, 5, 9, 16, 31, 22, 630726, tzinfo=tzutc()), '_value': '169.254.249.146', '_field': 'ip', '_measurement': 'my_measurement', 'maquina': 'rb1'}",
    "FluxRecord() table: 2, {'result': '_result', 'table': 2, '_start': datetime.datetime(2024, 5, 9, 16, 21, 32, 655773, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 5, 9, 16, 31, 32, 655773, tzinfo=tzutc()), '_time': datetime.datetime(2024, 5, 9, 16, 31, 12, 573719, tzinfo=tzutc()), '_value': 24.8, '_field': 'temperatura', '_measurement': 'my_measurement', 'maquina': 'rb1'}",
    "FluxRecord() table: 2, {'result': '_result', 'table': 2, '_start': datetime.datetime(2024, 5, 9, 16, 21, 32, 655773, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 5, 9, 16, 31, 32, 655773, tzinfo=tzutc()), '_time': datetime.datetime(2024, 5, 9, 16, 31, 17, 611439, tzinfo=tzutc()), '_value': 24.8, '_field': 'temperatura', '_measurement': 'my_measurement', 'maquina': 'rb1'}",
    "FluxRecord() table: 2, {'result': '_result', 'table': 2, '_start': datetime.datetime(2024, 5, 9, 16, 21, 32, 655773, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 5, 9, 16, 31, 32, 655773, tzinfo=tzutc()), '_time': datetime.datetime(2024, 5, 9, 16, 31, 22, 630726, tzinfo=tzutc()), '_value': 24.8, '_field': 'temperatura', '_measurement': 'my_measurement', 'maquina': 'rb1'}"
]
"""
0 -> humedad
1-> ip
2 -> temperatura
"""

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
            id_value[time] = extract_values(data_list,time)  

        else:
            time = get_datetime(data)
            id_value[time] = extract_values(data_list,time)  

        res[id] = id_value
    
    return res

dic = records_to_dict(data)

dic2 =dic['rb1']

print(dic2)