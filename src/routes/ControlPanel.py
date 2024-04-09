from flask import Blueprint
from ..utils import TCP_connection

main = Blueprint('index_blueprint', __name__)

@main.route('/')

def index():

    return tcp_prueba()