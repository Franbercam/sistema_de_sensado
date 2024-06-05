from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, username, password, is_admin=False) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)