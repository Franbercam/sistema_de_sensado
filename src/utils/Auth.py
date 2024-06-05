from flask import redirect, url_for, request
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('login_blueprint.index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function