from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required


main = Blueprint('raspinfo_blueprint', __name__, url_prefix='/raspinfo')

from ..services import influxdb_service as db
from ..database import local_db_controller as alert

@main.route('/')
@login_required
def index():
    machine_name = request.args.get('machine_name')
    machine_data =(db.get_data_by_name_db(machine_name))[machine_name]
    
    return render_template("raspinfo.html", machine_name=machine_name, machine_data=machine_data)

@main.route('/obtener_alertas', methods=['GET'])
def obtener_alertas():
    datos = alert.get_alerts_db()

    return datos

@main.route('/borrar_alerta', methods=['POST'])
def borrar_alerta():
    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({'error': 'No se proporcionó el nombre de la alerta'}), 400

    try:
        result = alert.delete_alert_issued_db(nombre)
        return jsonify({'message': 'Alerta borrada correctamente'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500