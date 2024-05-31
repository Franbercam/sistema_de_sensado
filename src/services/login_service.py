import traceback

# Database
from src.database.local_db_controller import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.UserModel import User


class AuthService():

    @classmethod
    def login_user(cls, user):
        try:
            connection = get_connection()
            authenticated_user = None
            with connection:
                cursor = connection.cursor()
                cursor.execute('SELECT id, nombre FROM users WHERE nombre=? AND contraseña=?', (user.username, user.password))
                row = cursor.fetchone()
                if row is not None:
                    authenticated_user = User(int(row[0]), row[1], None, row[2])
            return authenticated_user
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
