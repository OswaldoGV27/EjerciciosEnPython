import socket
import os

# Configuración
HOST = "192.168.56.102"  
PORT = 5005
BUFFER_SIZE = 1024

# Usamos una ruta absoluta o verificamos la existencia para evitar errores en Windows
ruta_archivo = "../libros/MOBY_DICK.txt" 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    try:
        print(f"Conectando a {HOST}...")
        TCPClientSocket.connect((HOST, PORT))
        print("¡Conectado! Enviando archivo...")

        if not os.path.exists(ruta_archivo):
            print(f"Error: No se encuentra el archivo en {ruta_archivo}")
        else:
            with open(ruta_archivo, "rb") as archivo:
                while True:
                    data = archivo.read(BUFFER_SIZE)
                    if not data:
                        break
                    TCPClientSocket.sendall(data)
            
            # Avisamos al servidor que terminamos de escribir
            TCPClientSocket.shutdown(socket.SHUT_WR)
            print("Transferencia completa. Esperando cierre del servidor...")
            
    except Exception as e:
        print(f"Error de conexión: {e}")

print("Cliente finalizado.")