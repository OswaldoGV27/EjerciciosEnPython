import socket
import threading
import time

HOST = "192.168.56.102"
PORT = 5050
buffer_size = 1024

aplicaciones = [
    "Cliente 1: Spotify",
    "Cliente 2: Netflix",
    "Cliente 3: Youtube",
    "Cliente 4: Discord",
    "Cliente 5: WhatsApp"
]

def simular_cliente_tcp(nombre_app):
    # Creamos un socket TCP nuevo. Windows le asignará un puerto de origen único.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
        try:
            TCPClientSocket.connect((HOST, PORT))
            
            # Extraemos el puerto local que Windows nos acaba de asignar para imprimirlo
            puerto_origen = TCPClientSocket.getsockname()[1]
            print(f"[{nombre_app}] Conectado desde el puerto local {puerto_origen}. Enviando mensaje...")
            
            # Armamos y enviamos el mensaje
            mensaje = f"Hola servidor, soy {nombre_app}"
            TCPClientSocket.sendall(mensaje.encode('utf-8'))
            
            # Esperamos la respuesta
            data = TCPClientSocket.recv(buffer_size)
            print(f"[{nombre_app}] Respuesta: {data.decode('utf-8')}")
            
        except ConnectionRefusedError:
            print(f"[{nombre_app}] Error: El servidor rechazó la conexión. ¿Está encendido?")
        except Exception as e:
            print(f"[{nombre_app}] Error inesperado: {e}")

def main():
    print(f"Iniciando simulación de 5 clientes TCP hacia {HOST}:{PORT}...\n")
    hilos = []
    
    # Lanzamos un hilo por cada aplicación
    for app in aplicaciones:
        hilo = threading.Thread(target=simular_cliente_tcp, args=(app,))
        hilos.append(hilo)
        hilo.start()
        time.sleep(0.2) 

    # Esperamos a que todos los hilos terminen su trabajo
    for hilo in hilos:
        hilo.join()
        
    print("\nSimulación finalizada.")

if __name__ == "__main__":
    main()