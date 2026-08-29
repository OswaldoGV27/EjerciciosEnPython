#!/usr/bin/env python3

import socket
import selectors

# Elige automáticamente el mecanismo de E/S más eficiente del SO (epoll en Linux, select en Windows)
sel = selectors.DefaultSelector()
sensores_activos = 0

def accept_client(sock_a, mask):
    global sensores_activos 
    
    sock_conn, addr = sock_a.accept()
    
    # Evita que el servidor se congele esperando a este cliente en específico
    sock_conn.setblocking(False)
    
    # Registramos el nuevo socket para que el selector nos avise SOLO cuando haya datos listos para leer (EVENT_READ)
    # y le asignamos la función que debe ejecutar cuando eso pase (read_sensor_data)
    sel.register(sock_conn, selectors.EVENT_READ, read_sensor_data)
    
    sensores_activos += 1
    print(f"\n[+] EVENTO DE CONEXIÓN: Nuevo sensor conectado desde {addr}")
    print(f"[*] Total de sensores activos: {sensores_activos}")

def read_sensor_data(sock_c, mask):
    global sensores_activos
    addr = sock_c.getpeername()
    
    try:
        data = sock_c.recv(1024)
        
        if data:
            # Procesamiento de los datos y envío del acuse de recibo (ACK)
            mensaje = data.decode('utf-8').strip()
            print(f"[Sensor {addr[1]}] Datos: {mensaje}")
            respuesta = f"Servidor ACK: '{mensaje}' procesado.\n".encode('utf-8')
            sock_c.sendall(respuesta) 
            
        else:
            # En TCP, recibir un dato vacío (b'') significa que el cliente solicitó cerrar la conexión formalmente
            sel.unregister(sock_c) # Dejamos de vigilar este socket para liberar recursos
            sock_c.close()
            
            sensores_activos -= 1
            print(f"\n[-] EVENTO DE DESCONEXIÓN: El sensor {addr} cerró la conexión correctamente.")
            print(f"[*] Total de sensores activos: {sensores_activos}")
            
    except ConnectionResetError:
        # Maneja cierres forzados en el sensor
        sel.unregister(sock_c)
        sock_c.close()
        
        sensores_activos -= 1
        print(f"\n[!] EVENTO DE DESCONEXIÓN ABRUPTA: Se perdió la comunicación con el sensor {addr}.")
        print(f"[*] Total de sensores activos: {sensores_activos}")

def main():
    HOST = '192.168.56.102' 
    PORT = 5050

    sock_accept = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reiniciar el servidor rápidamente sin que el SO bloquee el puerto temporalmente
    sock_accept.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_accept.bind((HOST, PORT))
    sock_accept.listen(100)
    
    # El socket principal del server
    sock_accept.setblocking(False)

    # Registramos el socket principal para que avise al servidor solo cuando haya nuevas solicitudes de conexión
    sel.register(sock_accept, selectors.EVENT_READ, accept_client)

    print(f"Servidor de Sensores (Selectors) escuchando en el puerto {PORT}...")
    print(f"[*] Total inicial de sensores activos: {sensores_activos}\n")

    try:
        while True:
            # Bucle de eventos: Pausa la ejecución hasta que ocurra actividad en algún socket registrado
            events = sel.select()
            for key, mask in events:
                # key.data contiene la función callback registrada (accept_client o read_sensor_data)
                callback = key.data 
                # Ejecutamos la función pasándole el socket específico que se activó (key.fileobj)
                callback(key.fileobj, mask)
                
    except KeyboardInterrupt:
        print("\nApagando servidor...")
    finally:
        sel.close()

if __name__ == "__main__":
    main()