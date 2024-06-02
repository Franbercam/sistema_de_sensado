from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from ..database import local_db_controller as db

main = Blueprint('users_edit_blueprint', __name__, url_prefix='/users_edit')

@main.route('/')
@login_required
def index():  

    return (render_template("users_edit.html"))

@main.route('/annadir_usuario', methods=['POST'])
def annadir_usuario():
    data = request.json

    usuario = data.get('username')
    contrasenna = data.get('password')


     # Validar que se recibieron todos los campos requeridos
    if not all([usuario, contrasenna]):
        return jsonify({'error': 'Faltan campos requeridos'}), 400  # Bad request
    
    db.add_user_db(usuario,contrasenna)


    return jsonify({'message': 'Usuario agregado correctamente'}), 200  # OK


@main.route('/get_users', methods=['GET'])
def get_users():
    usuarios = db.get_users_name_db()  
    return jsonify({'users': usuarios}), 200

@main.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    data = request.json
    
    usuario = data.get('username')
    
    if not usuario:
        return jsonify({'error': 'Falta el nombre de usuario'}), 400

    db.delete_user_db(usuario[0])
    return jsonify({'message': 'Usuario eliminado correctamente'}), 200