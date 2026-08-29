#!/usr/bin/python3

import socket
import time

# Configuración del servidor
HOST = "192.168.56.102" 
PORT = 5005
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ServerAccept:
    ServerAccept.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ServerAccept.bind((HOST, PORT))
    ServerAccept.listen() 
    print(f"Servidor TCP esperando en {PORT}...") #Se indica el puerto en el que espera el servidor
    
    conn, addr = ServerAccept.accept()
    with conn:
        print(f"Conectado a {addr}")
        total_bytes = 0
        total_bloques = 0
        start_time = time.time()
        
        # Reconstrucción del archivo
        with open("MOBY_DICK_recibido.txt", "wb") as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break # Para detectar el fin del archivo una vez se tenga vacio
                
                f.write(data)
                total_bytes += len(data)
                total_bloques += 1
        
        # El tiempo final se toma justo al salir del bucle de recepción
        end_time = time.time()

    # --- Cálculo y despliegue de estadísticas ---
    tiempo_total = end_time - start_time
    throughput = total_bytes / tiempo_total if tiempo_total > 0 else 0
    
    print("\n--- Resultados de la Transferencia ---")
    print(f"Total de bytes recibidos: {total_bytes} bytes")
    print(f"Total de bloques recibidos: {total_bloques} bloques")
    print(f"Tiempo total: {tiempo_total:.4f} segundos")
    print(f"Throughput: {throughput:.2f} bytes/segundo")
