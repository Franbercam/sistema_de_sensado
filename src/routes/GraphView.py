from flask import Blueprint, render_template, request
from flask_login import login_required

from datetime import datetime

from ..services import influxdb_service as db

main = Blueprint('graph_blueprint', __name__, url_prefix='/graph')



@main.route('/')
@login_required
def index():
    machine_name = request.args.get('machine_name')
    
    # Obtener los datos de la base de datos
    data = (db.get_data_by_name_db(machine_name))[machine_name]
    
    # Convertir las claves a objetos datetime si son cadenas
    formatted_data = {}
    for key, value in data.items():
        if isinstance(key, str):
            key = datetime.fromisoformat(key)  # Convierte la cadena a datetime
        formatted_data[key] = value
    
    # Formatear los datos para Chart.js
    labels = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in formatted_data.keys()]
    temperatures = [values[0] for values in formatted_data.values()]
    humidities = [values[1] for values in formatted_data.values()]

    return render_template('graph.html', labels=labels, temperatures=temperatures, humidities=humidities)

