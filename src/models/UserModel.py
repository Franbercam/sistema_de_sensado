from .entities.User import User
from ..database import local_db_controller 

class UserModel():

    def login(self,user):
        try:
            cursor = local_db_controller.get_connection()
            sql = """SELECT id, nombre, contraseña FROM user
                        WHERE username = '{}'""".format(user.username)
        except Exception as ex:
            raise Exception(ex)
