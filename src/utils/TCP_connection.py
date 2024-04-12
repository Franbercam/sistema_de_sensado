import socket


def conectar_servidor(server_host, server_port):
    # Socket para la conexión TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Intentar conectar al servidor
        connection_result = client_socket.connect_ex((server_host, server_port))

        if connection_result == 0:
            # Recibir datos del servidor
            data = client_socket.recv(1024) 
            if not data:
                return [server_host,"No existe lectura del sensor"]
            else:
                return [server_host,data.decode('UTF-8')]
                
        else:
            return [server_host,f"Código de error: {connection_result}"]
    except Exception as e:
        return [server_host,f"Error: {e}"]
    finally:
        client_socket.close()
