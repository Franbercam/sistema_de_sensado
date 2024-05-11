from flask import Blueprint, render_template, jsonify
from ..services import influxdb_service as db




main = Blueprint('index_blueprint', __name__)

@main.route('/')
def index():  

    return (render_template("index.html"))

@main.route('/obtener_datos', methods=['GET'])
def obtener_datos():
    datos = db.get_data_db()

    return (datos)