import socket

HOST = "192.168.56.102"  # El hostname o IP del servidor
PORT = 5005  # El puerto que usa el servidor
bufferSize = 1024
msgFromServer = "OK"
bytesToSend = str.encode(msgFromServer)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))

    print("Servidor UDP activo, esperando peticiones...")
    
    while True:
        # data contiene el mensaje, address es una tupla (IP, Puerto)
        data, address = UDPServerSocket.recvfrom(bufferSize)

        # Si recibimos el paquete vacío (b''), rompemos el ciclo
        if not data:
            print("Fin de transmisión recibido. Cerrando servidor.")
            break
            
        # Extraemos la IP y el puerto de la tupla address
        ip_cliente = address[0]
        puerto_cliente = address[1]
        
        # Decodificamos el número del mensaje
        numero_mensaje = data.decode()

        # Imprimimos la frase exacta solicitada
        print(f"El cliente UDP con la ip '{ip_cliente}' y puerto '{puerto_cliente}' mandó el mensaje numero '{numero_mensaje}'")
        
        # Enviando una respuesta de confirmación al cliente
        UDPServerSocket.sendto(bytesToSend, address)