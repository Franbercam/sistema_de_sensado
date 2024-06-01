from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user,logout_user

from ..models import UserModel
from ..models.entities import User


main = Blueprint('login_blueprint', __name__)

@main.route('/')
def index():
    return redirect(url_for('login_blueprint.login'))


@main.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.User(0,request.form['username'],request.form['password'])
        logged_user= UserModel.UserModel.login(user)

        if logged_user!=None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('control_panel_blueprint.index'))
            else:
                flash("Usuario o contraseña incorrecta")
                return render_template('login.html')
        else:
            flash("Usuario o contraseña incorrecta")
            return render_template('login.html')
       
    else:
        return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_blueprint.login'))