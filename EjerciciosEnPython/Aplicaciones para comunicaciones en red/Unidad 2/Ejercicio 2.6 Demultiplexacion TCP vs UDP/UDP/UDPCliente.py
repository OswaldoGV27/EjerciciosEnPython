#!/usr/bin/env python3

import socket
import time
import random

HOST = "192.168.56.102"
PORT = 5050

def main():
    # El cliente asume su propia identidad
    cliente_id = f"Cliente_{random.randint(100, 999)}"
    print(f"Iniciando {cliente_id} en modo UDP...")
    
    operaciones_validas = ['SQR', 'CUBE', 'NEG']

    #Usamos SOCK_DGRAM para UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        
        #Le ponemos un timeout de 2 segundos. Como UDP no garantiza la entrega,
        #si el servidor no responde en 2s, el cliente no se quedará congelado esperando para siempre.
        sock.settimeout(2.0)
        
        try:
            while True:
                operacion = random.choice(operaciones_validas)
                valor = random.randint(-10, 15)
                
                mensaje = f"{cliente_id}:{operacion}:{valor}"
                
                print(f"[{cliente_id}] Lanzando datagrama: {mensaje}")
                
                #Usamos sendto() enviando al HOST y PORT en cada vuelta
                sock.sendto(mensaje.encode('utf-8'), (HOST, PORT))
                
                try:
                    #Esperamos la respuesta del servidor.
                    data, addr = sock.recvfrom(1024)
                    print(f"[{cliente_id}] Respuesta del servidor: {data.decode('utf-8').strip()}\n")
                except socket.timeout:
                    print(f"[{cliente_id}] [!] El paquete se perdió o el servidor no respondió.\n")
                
                time.sleep(3)

        except KeyboardInterrupt:
            print(f"\nApagando {cliente_id}...")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()