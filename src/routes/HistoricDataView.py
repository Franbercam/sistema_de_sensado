from flask import Blueprint, render_template


main = Blueprint('historic_blueprint', __name__)

@main.route('/')



def index():     


    return (render_template("historial.html"))