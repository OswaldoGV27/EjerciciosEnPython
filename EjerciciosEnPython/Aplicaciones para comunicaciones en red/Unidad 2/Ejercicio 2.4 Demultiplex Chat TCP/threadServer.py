#!/usr/bin/env python3

import socket
import sys
import threading

# Estructura compartida: Registrar { socket_cliente: "nickname" }
clientes_activos = {}

def broadcast(mensaje, remitente_conn=None):
    """Envía un mensaje a todos los clientes, excepto a quien lo originó."""
    for conn in list(clientes_activos.keys()):
        if conn != remitente_conn:
            try:
                conn.sendall(mensaje.encode('utf-8'))
            except:
                # Si falla el envío, asumimos que el cliente murió y lo removemos
                conn.close()
                del clientes_activos[conn]

def manejar_cliente(conn, addr):
    """Hilo independiente para cada cliente conectado."""
    try:
        # El primer mensaje que envía el cliente debe ser su nickname
        nickname = conn.recv(1024).decode('utf-8').strip()
        clientes_activos[conn] = nickname
        
        # Anunciamos la llegada a todos los demás
        msg_bienvenida = f"[Servidor]: {nickname} se ha unido al chat."
        print(f"[{addr[0]}:{addr[1]}] Se registró como '{nickname}'")
        broadcast(msg_bienvenida, conn)

        # Ciclo principal para escuchar los mensajes de este cliente en específico
        while True:
            data = conn.recv(1024)
            if not data:
                break # El cliente cerró la conexión
            
            mensaje = data.decode('utf-8')
            
            # Demultiplexación: Mostrar en la consola del servidor de quién viene
            print(f"[Cliente {addr[0]}:{addr[1]} - {nickname}]: {mensaje}")
            
            # Reenviar mensaje al resto de la sala
            mensaje_a_distribuir = f"[{nickname}]: {mensaje}"
            broadcast(mensaje_a_distribuir, conn)

    except Exception as e:
        print(f"Error con el cliente {addr}: {e}")
        
    finally:
        # Manejar desconexiones
        if conn in clientes_activos:
            nickname = clientes_activos[conn]
            del clientes_activos[conn] # Eliminar de la lista
            msg_salida = f"[Servidor]: {nickname} ha abandonado la sala."
            print(msg_salida)
            broadcast(msg_salida) # Notificar al resto
        conn.close()

def main():
    HOST = "192.168.56.102"
    PORT = 5050
    
    if len(sys.argv) == 3:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        # Esta opción permite reiniciar el servidor sin que el puerto se quede "atascado"
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind((HOST, PORT))
        TCPServerSocket.listen(10)
        
        print(f"Servidor de Chat TCP iniciado en el puerto {PORT}")
        print("Esperando conexiones...")

        try:
            while True:
                client_conn, client_addr = TCPServerSocket.accept()
                
                # Crear el thread independiente para el cliente recién llegado
                hilo = threading.Thread(target=manejar_cliente, args=(client_conn, client_addr))
                hilo.daemon = True 
                hilo.start()
                
        except KeyboardInterrupt:
            print("\nApagando el servidor de chat...")

if __name__ == "__main__":
    main()