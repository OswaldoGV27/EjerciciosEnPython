import socket

HOST = "192.168.56.102"  # Direccion de la interfaz (localhost o IP de red)
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
        
        while True:
            data = Client_conn.recv(buffer_size)
            if not data:
                break # Si ya no hay datos o el cliente se desconecta, salimos
            
            # Decodificamos el mensaje para obtener la 'X' (el número)
            numero_mensaje = data.decode()
            
            # Imprimimos la frase exacta solicitada
            print(f"El cliente TCP con la ip '{ip_cliente}' y puerto '{puerto_cliente}' mandó el mensaje numero '{numero_mensaje}'")
            
            # Enviamos una respuesta genérica al cliente para que sepa que puede mandar el siguiente
            Client_conn.sendall(b"OK")