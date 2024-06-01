from .entities.User import User
from ..database import local_db_controller 
 

class UserModel():

    @classmethod
    def login(self, user):
        try:
            # Conexión a la base de datos SQLite
            conn = local_db_controller.get_connection()   
            cursor = conn.cursor()
            
            # Consulta SQL para obtener el usuario
            sql = """SELECT id, nombre, contraseña FROM users WHERE nombre = ?"""
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            # Verificar si se encontró el usuario
            if row != None:
                user = User(row[0],row[1],User.check_password(row[2],user.password))                
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
            # Conexión a la base de datos SQLite
            conn = local_db_controller.get_connection()   
            cursor = conn.cursor()
            
            # Consulta SQL para obtener el usuario
            sql = """SELECT id, nombre FROM users WHERE id = ?"""
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            # Verificar si se encontró el usuario
            if row != None:
                user = User(row[0],row[1],None)                
                return user
            else:
                return None            

        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()
            conn.close()
