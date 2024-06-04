from flask import Flask, redirect, url_for
from flask_login import LoginManager

from .routes import ControlPanel, MailView, LoginView, UsersEdit, RaspInfo, GraphView
from .database import local_db_controller as db
from .models import UserModel


app = Flask(__name__)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return UserModel.UserModel.get_by_id(id)

def status_401_404(error):
    return redirect((url_for('login_blueprint.index')))


def init_app(config):

    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(LoginView.main,url_prefix='/')
    app.register_blueprint(ControlPanel.main, url_prefix='/control_panel')
    app.register_blueprint(MailView.main, url_prefix='/mail')
    app.register_blueprint(UsersEdit.main, url_prefix='/users_edit')
    app.register_blueprint(RaspInfo.main, url_prefix='/raspinfo')
    app.register_blueprint(GraphView.main, url_prefix='/graph')

    #Manejo de errores
    app.register_error_handler(401,status_401_404)
    app.register_error_handler(404,status_401_404)

    #Inicializamos la base de datos local
    db.initialize_database()

  
    return app
   
