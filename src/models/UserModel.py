from .entities.User import User
from ..database import local_db_controller 

class UserModel():

    @classmethod
    def login(self, user):
        try:
            conn = local_db_controller.get_connection()   
            cursor = conn.cursor()
            sql = """SELECT id, nombre, contraseña, es_admin FROM users WHERE nombre = ?"""
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])                
                return user
            else:
                return None            
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_by_id(self, id):
        try:
            conn = local_db_controller.get_connection()   
            cursor = conn.cursor()
            sql = """SELECT id, nombre, es_admin FROM users WHERE id = ?"""
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], None, row[2])                
                return user
            else:
                return None            
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()
            conn.close()

