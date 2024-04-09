from flask import Flask
from .routes import ControlPanel


app = Flask(__name__)

def init_app(config):

    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(ControlPanel.main, url_prefix='/')

    return app
   
