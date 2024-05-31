from flask import Flask
from .routes import ControlPanel, MailView, LoginView
from .database import local_db_controller as db


app = Flask(__name__)

def init_app(config):

    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(LoginView.main,url_prefix='/')
    app.register_blueprint(ControlPanel.main, url_prefix='/control_panel')
    app.register_blueprint(MailView.main, url_prefix='/mail')

    #Inicializamos la base de datos para las alertas
    db.initialize_database()

  
    return app
   
