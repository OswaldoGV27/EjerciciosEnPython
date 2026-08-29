#!/usr/bin/env python3

import socket
import sys

HOST = '192.168.56.102'
PORT = 5051

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print("Conectando al servidor del juego...")
            sock.connect((HOST, PORT))
            
            data = sock.recv(1024).decode('utf-8')
            
            if not data:
                print("El servidor cerró la conexión prematuramente.")
                return

            print("Bloqueado en sala de espera... (No cierres la ventana)")
            data_start = sock.recv(1024).decode('utf-8')
                
            if data_start:
                mensaje_inicio = data_start.strip()
                if "INICIANDO:" in mensaje_inicio:
                    print(f"\n>> {mensaje_inicio} <<")
                    print("Goku ganó el juego XD")
                else:
                    print(f"Mensaje inesperado: {mensaje_inicio}")
                    
        except ConnectionRefusedError:
            print("Error: No se pudo conectar. ¿El servidor está encendido?")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()