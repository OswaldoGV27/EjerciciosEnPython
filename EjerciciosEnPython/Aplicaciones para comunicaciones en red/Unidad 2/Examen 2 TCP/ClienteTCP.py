#!/usr/bin/env python3
import socket
import time

HOST = '192.168.56.102'
PORT = 5050

def iniciar_cliente():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            print(f"Conectado al pool de control. Enviando Keep-Alives cada 2s...")
            
            while True:
                # RF1.2 Envío periódico
                sock.sendall(b"Keep-Alive")
                data = sock.recv(1024)
                print(f"Respuesta: {data.decode('utf-8').strip()} - {time.ctime()}")
                time.sleep(2)
                
    except Exception as e:
        print(f"Conexión perdida: {e}")

if __name__ == "__main__":
    iniciar_cliente()