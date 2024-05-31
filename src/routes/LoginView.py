from flask import Blueprint, render_template, request, jsonify, redirect, url_for

import traceback

from ..models import UserModel
from ..services import login_service
from ..utils import Security, Logger


main = Blueprint('login_blueprint', __name__)

@main.route('/')
def index():
    return redirect(url_for('login_blueprint.login'))


@main.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        return render_template('login.html')
    else:
        return render_template('login.html')
