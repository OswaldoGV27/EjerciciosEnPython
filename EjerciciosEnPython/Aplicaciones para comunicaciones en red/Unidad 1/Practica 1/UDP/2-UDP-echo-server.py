import socket
import time

# Configuración
HOST = "192.168.56.104"  
PORT = 5005
bufferSize = 1024
msgFromServer = "OK"
bytesToSend = str.encode(msgFromServer)

# Crear socket UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    try:
        UDPServerSocket.bind((HOST, PORT))
        print(f"Servidor UDP activo en el puerto {PORT}, esperando peticiones...")
    except Exception as e:
        print(f"Error al levantar el servidor: {e}")
        exit()

    total_bytes = 0
    total_bloques = 0
    start_time = None

    while True:
        try:
            # Recibir datos del cliente
            data, address = UDPServerSocket.recvfrom(bufferSize)

            if start_time is None:
                start_time = time.time()
                print("¡Transferencia iniciada!")

            # Si recibimos el paquete de cierre
            if not data:
                print("Fin de transmisión recibido.")
                break
                
            total_bytes += len(data)
            total_bloques += 1
            
            # Decodificar y mostrar mensaje (opcional si son muchos)
            numero_mensaje = data.decode()
            print(f"Mensaje {numero_mensaje} recibido de {address}")
            
            # Enviar respuesta al cliente
            UDPServerSocket.sendto(bytesToSend, address)

        except ConnectionResetError:
            # Este catch evita que el servidor se cierre por el error 10054
            print("Aviso: Se perdió la conexión con un cliente (ICMP Port Unreachable).")
            continue

    end_time = time.time()
    tiempo_total = end_time - start_time if start_time else 0

    # --- Resultados (Control Estadístico) ---
    print("\n" + "="*40)
    print(" Control Estadístico (UDP)")
    print("="*40)
    print(f"Número total de bytes recibidos: {total_bytes}")
    print(f"Número total de bloques recibidos: {total_bloques}")
    print(f"Tiempo total de transferencia: {tiempo_total:.4f} segundos")