import serial
import socket
import threading

class SensorServer:
    def __init__(self, serial_port, serial_baudrate, server_host, server_port):
        self.serial_port = serial_port
        self.serial_baudrate = serial_baudrate
        self.server_host = server_host
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def read_config(self):
        try:
            with open("config.txt", "r") as file:
                lines = file.readlines()
                name = lines[0].strip()
                location = lines[1].strip()
                return name, location
        except FileNotFoundError:
            print("Archivo 'config.txt' no encontrado.")
            return "", ""
        except IndexError:
            print("Archivo 'config.txt' no contiene suficientes líneas.")
            return "", ""

    def start(self):
        # Inicializa la conexión serial
        self.T = serial.Serial(self.serial_port, self.serial_baudrate)

        # Configura el servidor TCP/IP
        self.server_socket.bind((self.server_host, self.server_port))
        self.server_socket.listen(5)
        print(f"[*] Escuchando en {self.server_host}:{self.server_port}")

        while True:
            # Acepta conexiones de clientes entrantes
            client_socket, addr = self.server_socket.accept()
            print(f"[*] Conexión aceptada desde {addr[0]}:{addr[1]}")
            
            # Lee el contenido del archivo config.txt
            name, location = self.read_config()
            config_data = f"{name},{location}"

            # Inicia un hilo para manejar la conexión del cliente y pasa el contenido de config.txt
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, config_data))
            client_handler.start()

    def handle_client(self, client_socket, config_data):
        while True:
            # Lee los datos del sensor
            try:
                sArduino = self.T.readline()
                s = sArduino.decode('UTF-8').strip()
                print("Datos del sensor:", s)
                
                # Verifica si el socket del cliente está cerrado
                if not client_socket._closed:
                    try:
                        # Envía los datos al cliente conectado junto con el contenido de config.txt
                        data_to_send = f"{s},{config_data}"
                        client_socket.send(data_to_send.encode('UTF-8'))
                    except OSError as e:
                        print("Error al enviar datos al cliente:", e)
                        break  # Sale del bucle si hay un error al enviar datos
                else:
                    print("El socket del cliente está cerrado.")
                    break  # Sale del bucle si el socket del cliente está cerrado
            except serial.SerialException as e:
                print("Error al leer datos del sensor:", e)
                break  # Sale del bucle si hay un error al leer datos del sensor

def main():
    serial_port = '/dev/ttyACM0'
    serial_baudrate = 9600
    server_host = '0.0.0.0'
    server_port = 8888

    sensor_server = SensorServer(serial_port, serial_baudrate, server_host, server_port)
    sensor_server.start()

if __name__ == "__main__":
    main()
