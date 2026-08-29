#!/usr/bin/env python3
import socket
import threading

HOST = "192.168.56.102" 
PORT = 5050
buffer_size = 1024

# 1. Definimos la función que será el Hilo Secundario
def manejar_cliente(conn, addr):
    print(f"[NUEVO HILO] Atendiendo la conexión de {addr}")
    with conn:
        while True:
            try:
                # Este hilo SÍ se bloquea aquí esperando a su cliente específico
                data = conn.recv(buffer_size) 
                
                if not data:
                    print(f"[{addr}] El cliente cerró la conexión formalmente.")
                    break
                
                print(f"[{addr}] Recibió: {data.decode('utf-8').strip()}")
                conn.sendall(data)
                
            except ConnectionResetError:
                print(f"[{addr}] ¡Conexión perdida abruptamente!")
                break

def main():
    # 2. El Hilo Principal configura el servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.bind((HOST, PORT))
        TCPServerSocket.listen(5)
        
        print(f"Servidor TCP Multihilo en espera de solicitudes en el puerto {PORT}...")

        while True:
            Client_conn, Client_addr = TCPServerSocket.accept()
            
            # Se crea un hilo nuevo para atender al cliente
            # Le pasamos a la función 'manejar_cliente' el socket y la IP que acabamos de aceptar
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(Client_conn, Client_addr))
            
            # arranca el hilo en paralelo y el Hilo Principal regresa inmediatamente al accept()
            hilo_cliente.start() 

if __name__ == "__main__":
    main()