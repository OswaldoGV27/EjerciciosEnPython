#!/usr/bin/env python3
import socket
import time

HOST = "192.168.56.102" 
PORT = 5050
buffer_size = 1024
clientes_activos = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(5)
    #Modo no bloqueante
    TCPServerSocket.setblocking(False)
    
    print(f"Servidor en cámara lenta iniciado en el puerto {PORT}. Observando excepciones...\n") 

    while True:
        # CAZANDO EXCEPCIÓN A: accept()
        try:
            Client_conn, Client_addr = TCPServerSocket.accept()
            Client_conn.setblocking(False)
            print(f"\n¡NUEVA CONEXIÓN ACEPTADA DE {Client_addr}!")
            clientes_activos.append((Client_conn, Client_addr))
            
        except BlockingIOError as e:
            # Esto se imprimirá constantemente mientras nadie se conecte
            print(f"[Fase accept] Nadie intentando conectarse: Excepción invisible del sistema: {repr(e)}")


        # CAZANDO EXCEPCIONES B y C: recv()
        for conn, addr in clientes_activos[:]:
            try:
                data = conn.recv(buffer_size) 
                if data:
                    print(f"=== Dato recibido de {addr}: {data.decode('utf-8').strip()} ===")
                    conn.sendall(data)
                else:
                    print(f"El cliente {addr} cerró la conexión formalmente.")
                    conn.close()
                    clientes_activos.remove((conn, addr))
                    
            except BlockingIOError as e:
                # Esto se imprimirá cuando el cliente esté conectado pero en silencio
                print(f"[Fase recv] {addr} conectado pero sin enviar datos: Excepción invisible: {repr(e)}")
                
            except ConnectionResetError as e:
                # Esto se imprimirá si cierras el cliente a la fuerza (Ej. cerrando su terminal de golpe)
                print(f"\n[Fase recv] ¡ALERTA! {addr} destruyó la conexión abruptamente: Excepción capturada: {repr(e)}")
                conn.close()
                clientes_activos.remove((conn, addr))
        
        print("-" * 50)
        time.sleep(5)