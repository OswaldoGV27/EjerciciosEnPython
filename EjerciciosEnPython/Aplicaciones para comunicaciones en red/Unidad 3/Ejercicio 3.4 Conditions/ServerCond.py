#!/usr/bin/env python3

import socket
import threading

HOST = '192.168.56.102' 
PORT = 5050
NUM_JUGADORES = 3
RONDAS_MAXIMAS = 3

turno_actual = 1
tablero_compartido = []

condicion_turno = threading.Condition()

def manejar_cliente(conn, addr, id_jugador):
    #Hilo del servidor que representa a un cliente y pelea por los turnos.
    global turno_actual, tablero_compartido
    
    for ronda in range(1, RONDAS_MAXIMAS + 1):
        #Obtenemos el candado de la variable de condicion
        with condicion_turno:
            
            #Si no es su turno, se va a dormir (Bloqueo sin espera activa)
            while turno_actual != id_jugador:
                condicion_turno.wait() 
                
            #INICIO DE SECCION CRITICA (TURNO ACTIVO)
            print(f"\n[Servidor] Otorgando turno al Jugador {id_jugador} (Ronda {ronda})...")
            mensaje = f"TURNO:Ronda {ronda}. Es tu turno, ingresa tu jugada:\n"
            conn.sendall(mensaje.encode('utf-8'))
            
            #Nos quedamos esperando a que el cliente responda
            try:
                jugada_cliente = conn.recv(1024).decode('utf-8').strip()
            except Exception:
                jugada_cliente = "Desconectado"
                
            #Modificamos el tablero compartido con lo que mando el cliente
            movimiento = f"[J{id_jugador}]: {jugada_cliente}"
            tablero_compartido.append(movimiento)
            print(f"[Servidor] Tablero actualizado: {tablero_compartido}")
            
            #Actualizamos el turno actual
            if turno_actual < NUM_JUGADORES:
                turno_actual += 1
            else:
                turno_actual = 1
                
            #Despertamos a los demas hilos del servidor
            condicion_turno.notify_all()
            
    conn.sendall(b"FIN:El juego ha terminado.\n")
    conn.close()

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(NUM_JUGADORES)

    print("=== SERVIDOR DE TURNOS INICIADO ===")
    print(f"Esperando a {NUM_JUGADORES} jugadores en el puerto {PORT}...\n")

    hilos_servidor = []
    
    # Aceptamos a los clientes y creamos un hilo por cada uno
    for i in range(1, NUM_JUGADORES + 1):
        conn, addr = server_sock.accept()
        print(f"Jugador {i} conectado desde {addr}.")
        
        t = threading.Thread(target=manejar_cliente, args=(conn, addr, i), name=f"Hilo-J{i}")
        hilos_servidor.append(t)
        t.start()

    # Esperamos a que todos terminen
    for t in hilos_servidor:
        t.join()

    print("\n" + "="*50)
    print("=== FIN DEL JUEGO ===")
    print("El tablero final (Historial de jugadas de los clientes) es:")
    for jugada in tablero_compartido:
        print(f" -> {jugada}")
    print("="*50)

if __name__ == "__main__":
    main()