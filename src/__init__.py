from flask import Flask
from .routes import ControlPanel


app = Flask(__name__)

def init_app(config):

    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(ControlPanel.main, url_prefix='/')
    #app.register_blueprint(influx_config.main, url_prefix='/historial.html')

    return app
   
