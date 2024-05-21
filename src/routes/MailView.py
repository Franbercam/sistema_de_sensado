from flask import Blueprint, render_template


main = Blueprint('mail_blueprint', __name__)

@main.route('/')



def index():     


    return (render_template("mail.html"))