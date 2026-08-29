#!/usr/bin/env python3

import socket

HOST = "192.168.56.104"  # Hostname o dirección IP del servidor
PORT = 5005  # Puerto del servidor
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Conexión establecida. Enviando mensajes...")
    
    # Bucle para enviar 100 mensajes
    for i in range(1, 101):
        # Convertimos el número a string y luego a bytes
        mensaje = str(i)
        TCPClientSocket.sendall(mensaje.encode())
        
        # Esperamos la respuesta del servidor antes de mandar el siguiente
        # Esto evita que los mensajes se "peguen" en la red
        data = TCPClientSocket.recv(buffer_size)
        
    print("Se enviaron los 100 mensajes correctamente.")