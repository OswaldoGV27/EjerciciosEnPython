import socket

HOST = "192.168.56.102"  # El hostname o IP del servidor
PORT = 5005  # El puerto usado por el servidor
serverAddressPort = (HOST, PORT)
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPClientSocket:
    print("Enviando 100 mensajes al servidor UDP...")
    
    # Bucle para enviar los 100 mensajes
    for i in range(1, 101):
        # Convertimos el número a string y luego a bytes
        bytesToSend = str(i).encode()
        
        # Enviando mensaje al servidor
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        
        # Esperamos el acuse de recibo del servidor (opcional, pero ordena el flujo)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        
    print("Se enviaron los 100 mensajes correctamente.")
    
    # Mandamos un paquete vacío para que el servidor sepa que terminamos y cierre su ciclo
    UDPClientSocket.sendto(b'', serverAddressPort)