#!/usr/bin/env python3

import socket
import time
import random

HOST = "192.168.56.102"
PORT = 5050

def main():
    sensor_id = random.randint(100, 999)
    print(f"Iniciando Sensor #{sensor_id}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
            print("Conectado al servidor central. Iniciando envío periódico...\n")
            
            while True:
                # Simulamos una lectura de temperatura entre 20.0 y 40.0 grados
                temperatura = round(random.uniform(20.0, 30.0), 2)
                mensaje = f"Temp: {temperatura}°C"
                
                print(f"[Sensor {sensor_id}] Enviando: {mensaje}")
                sock.sendall(mensaje.encode('utf-8'))
                
                # Esperamos el acuse de recibo (ACK) del servidor
                data = sock.recv(1024)
                print(f"[Sensor {sensor_id}] Respuesta del servidor: {data.decode('utf-8').strip()}\n")
                
                time.sleep(3)

        except ConnectionRefusedError:
            print("No se pudo conectar. ¿El servidor está encendido?")
        except KeyboardInterrupt:
            print(f"\nApagando Sensor #{sensor_id}...")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()