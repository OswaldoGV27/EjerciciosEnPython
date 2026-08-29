import socket
import time # Importamos time para medir la transferencia

HOST = "192.168.56.104"  # Direccion de la interfaz
PORT = 5005 # Puerto que usa el cliente
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(5)
    print("El servidor TCP está disponible y en espera de solicitudes")

    Client_conn, Client_addr = TCPServerSocket.accept()
    
    # Extraemos la IP y el puerto de la tupla Client_addr
    ip_cliente = Client_addr[0]
    puerto_cliente = Client_addr[1]

    with Client_conn:
        print(f"Conectado a {ip_cliente}:{puerto_cliente}")
        
        # --- INICIO DEL CONTROL ESTADÍSTICO ---
        total_bytes = 0
        total_bloques = 0
        start_time = time.time() # Iniciamos el cronómetro
        
        while True:
            data = Client_conn.recv(buffer_size)
            if not data:
                break # Si ya no hay datos, salimos del bucle
            
            # Actualizamos las variables por cada bloque recibido
            total_bytes += len(data)
            total_bloques += 1
            
            # Decodificamos el mensaje para obtener la 'X' (el número)
            numero_mensaje = data.decode()
            
            # Imprimimos la frase exacta solicitada
            print(f"El cliente TCP con la ip '{ip_cliente}' y puerto '{puerto_cliente}' mandó el mensaje numero '{numero_mensaje}'")
            
            # Enviamos una respuesta genérica al cliente
            Client_conn.sendall(b"OK")
            
        # --- FIN DEL BUCLE Y CÁLCULO FINAL ---
        end_time = time.time() # Detenemos el cronómetro
        tiempo_total = end_time - start_time
        
        # Mostramos los resultados en pantalla
        print("\n" + "="*40)
        print(" Control Estadístico (TCP)")
        print("="*40)
        print(f"Número total de bytes recibidos: {total_bytes}")
        print(f"Número total de bloques recibidos: {total_bloques}")
        print(f"Tiempo total de transferencia: {tiempo_total:.4f} segundos")