from flask import Blueprint, render_template
from flask_login import login_required

from ..services import influxdb_service as db
from ..database import local_db_controller as alert


main = Blueprint('control_panel_blueprint', __name__, url_prefix='/control_panel')

@main.route('/')
@login_required
def index():  

    return (render_template("control_panel.html"))


@main.route('/obtener_datos', methods=['GET'])
def obtener_datos():
    datos = db.get_data_db()

    return (datos)

@main.route('/obtener_alertas', methods=['GET'])
def obtener_alertas():
    datos = alert.get_alerts_issued_db()

    return datos