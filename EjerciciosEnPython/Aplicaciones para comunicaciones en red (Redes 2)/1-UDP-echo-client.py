import socket

HOST = "192.168.1.12"  # El hostname o IP del servidor
PORT = 5005  # El puerto usado por el servidor
serverAddressPort = (HOST, PORT)
bufferSize = 1024

# Crea un socket UDP del lado del cliente
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
    for i in range(100):
        msgFromClient = f"Hola servidor UDP, El cliente UDP mando el mensaje numero {i}"
        bytesToSend = str.encode(msgFromClient)

        # Enviando mensaje al servidor usando el socket UDP
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        print(f"EL cliente UDP con la IP 192.168.1.14 y puerto 5005 Envió Mensaje {i}")
        #msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        #print("Mensaje del servidor {}".format(msgFromServer[0]))
        #UDPClientSocket.sendto(b'', serverAddressPort)
