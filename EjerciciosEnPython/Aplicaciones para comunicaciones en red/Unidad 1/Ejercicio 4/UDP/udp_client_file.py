import socket
import os
import time

HOST = "192.168.56.102" # IP del servidor
PORT = 5005
CHUNK_SIZE = 900 # Usamos 900 para dejar 124 bytes libres para nuestro encabezado

file_path = "MobyDick.txt" 
file_size = os.path.getsize(file_path)

# Calcular cuantos paquetes vamos a enviar en total
total_packets = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE > 0 else 0)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Iniciando transferencia de {file_path}")
print(f"Tamaño: {file_size} bytes")
print(f"Total de paquetes a enviar: {total_packets}")

with open(file_path, "rb") as f:
    seq = 1
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break # Fin del archivo
        
        # Armar el encabezado: "Secuencia|Total|"
        header = f"{seq}|{total_packets}|".encode()
        
        # Enviar encabezado + pedazo de archivo
        client.sendto(header + chunk, (HOST, PORT))
        seq += 1
        
        # Control de flujo manual
        time.sleep(0.0001) 

print("Envio finalizado.")