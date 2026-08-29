#!/usr/bin/env python3

import socket
import threading

HOST = "192.168.56.102"  
PORT = 5050
buffer_size = 1024

def recibir_mensajes(sock):
    """Hilo secundario dedicado EXCLUSIVAMENTE a escuchar al servidor."""
    while True:
        try:
            data = sock.recv(buffer_size)
            if not data:
                print("\n[El servidor ha cerrado la conexión]")
                break
            
            # Imprimimos el mensaje que llegó de la sala
            print("\n" + data.decode('utf-8'))
            # Volvemos a colocar el prompt visual para que el usuario sepa que puede escribir
            print("Tu mensaje: ", end="", flush=True)
            
        except Exception:
            print("\n[Se perdió la conexión con el chat]")
            break

def main():
    nickname = input("Ingresa tu nickname para entrar al chat: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
        try:
            TCPClientSocket.connect((HOST, PORT))
            
            # Lo primero que le mandamos al servidor es nuestro nombre
            TCPClientSocket.sendall(nickname.encode('utf-8'))
            print("¡Conexión exitosa! Escribe 'salir' en cualquier momento para abandonar.\n")

            # Lanzamos el hilo secundario para poder RECIBIR mensajes todo el tiempo
            hilo_recepcion = threading.Thread(target=recibir_mensajes, args=(TCPClientSocket,))
            hilo_recepcion.daemon = True #Este hilo es solo un ayudante de fondo.
            hilo_recepcion.start()

            while True:
                mensaje = input("Tu mensaje: ")
                
                if mensaje.lower() == 'salir':
                    break
                
                if mensaje:
                    TCPClientSocket.sendall(mensaje.encode('utf-8'))

        except ConnectionRefusedError:
            print("No se pudo conectar al servidor. ¿Revisaste que esté encendido y la IP sea correcta?")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()