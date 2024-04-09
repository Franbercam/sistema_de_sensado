import socket

"""
#Dirección y puerto del servidor
server_host = '169.254.249.146' 
server_port = 8888

#Socket para la conexión TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_host, server_port))
    print("[*] Conexión exitosa al servidor")
except Exception as e:
    print(f"Error al conectar al servidor: {e}")
    exit()

while True:
    try:
        data = client_socket.recv(1024) 
        if not data:
            break
        print("Datos del sensor "+server_host+":" , data.decode('UTF-8'))
    except Exception as e:
        print(f"Error al recibir datos del servidor: {e}")
        break

client_socket.close()
"""

class TCP_connection:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print("[*] Conexión exitosa al servidor")
        except Exception as e:
            print(f"Error al conectar al servidor: {e}")
            exit()

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print("Datos del sensor " + self.server_host + ":", data.decode('UTF-8'))
            except Exception as e:
                print(f"Error al recibir datos del servidor: {e}")
                break

    def close_connection(self):
        self.client_socket.close()

    def tcp_prueba(self):
        return "Datos del sensor " + self.server_host

# Dirección y puerto del servidor
server_host = '169.254.249.146'
server_port = 8888

# Crear una instancia de la clase TCP_connection
connection = TCP_connection(server_host, server_port)


connection.connect()

# Recibir datos del servidor
connection.receive_data()

# Cerrar conexión
connection.close_connection()



