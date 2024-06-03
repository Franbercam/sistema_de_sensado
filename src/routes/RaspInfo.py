from flask import Blueprint, render_template, request
from flask_login import login_required


main = Blueprint('raspinfo_blueprint', __name__, url_prefix='/raspinfo')

from ..services import influxdb_service as db

@main.route('/')
@login_required
def index():
    machine_name = request.args.get('machine_name')
    machine_data =db.get_data_by_name_db(machine_name)

    data_dict = {"data_list": machine_data}
    return render_template("raspinfo.html", machine_name=machine_name, machine_data=data_dict)