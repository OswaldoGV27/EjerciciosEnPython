#!/usr/bin/env python3

import socket
import time
import random

HOST = "192.168.56.102"
PORT = 5050

def main():
    operaciones_validas = ['SQR', 'CUBE', 'NEG']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print("Conectando al servidor central...")
            sock.connect((HOST, PORT))
            
            # 1. FASE DE HANDSHAKE: Esperamos que el servidor nos dé un ID
            print("Esperando asignación de identidad...")
            data_inicial = sock.recv(1024).decode('utf-8').strip()
            
            # Verificamos que el servidor haya respondido con el formato correcto
            if data_inicial.startswith("ASSIGN:"):
                # Extraemos la parte derecha de los dos puntos
                cliente_id = data_inicial.split(":")[1] 
                print(f"ID Asignada: {cliente_id}\n")
            else:
                print("Error crítico: El servidor no asignó un ID válido.")
                return # Salimos del programa porque no podemos operar sin ID

            # 2. FASE NORMAL: Iniciamos el ciclo de envíos usando nuestro nuevo ID
            while True:
                operacion = random.choice(operaciones_validas)
                valor = random.randint(-10, 15)
                
                # Armamos el mensaje respetando el formato <ID_CLIENTE>:<OPERACIÓN>:<VALOR>
                mensaje = f"{cliente_id}:{operacion}:{valor}"
                
                print(f"[{cliente_id}] Enviando cálculo: {mensaje}")
                sock.sendall(mensaje.encode('utf-8'))
                
                # Esperamos respuesta
                data = sock.recv(1024)
                if not data:
                    print(f"[{cliente_id}] El servidor cerró la conexión.")
                    break
                    
                print(f"[{cliente_id}] Respuesta recibida: {data.decode('utf-8').strip()}\n")
                
                time.sleep(3)

        except ConnectionRefusedError:
            print("No se pudo conectar. ¿El servidor está encendido?")
        except KeyboardInterrupt:
            try:
                print(f"\nApagando {cliente_id}...")
            except NameError:
                print("\nApagando cliente...")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()