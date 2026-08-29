#!/usr/bin/env python3

import socket
import threading
import sys
import time

HOST = '192.168.56.102'
PORT = 5051

#Esta funcion se activa cuando se libera la barrera.
def iniciar_partida_server():
    print("\n" + "="*60)
    print("[SERVER] BARRERA ALCANZADA: Partida Iniciada")
    print("="*60 + "\n")

#Maneja la conexion de red de un jugador individual.
def manejar_jugador(conn, addr, barrera, id_jugador):
    print(f"[Lobby] Jugador {id_jugador} conectado desde {addr}.")
    
    try:
        #Mensaje de bienvenida al cliente
        mensaje_espera = f"Bienvenido Jugador {id_jugador}. Eres el {barrera.n_waiting + 1}/{barrera.parties} en la sala. Esperando a mas jugadores...\n"
        conn.sendall(mensaje_espera.encode('utf-8'))
        
        #Mensaje de espera en la barrera
        print(f"[Lobby] Jugador {id_jugador} esperando mas jugadores...")
        barrera.wait()

        time.sleep(0.2)
        #Enviamos la señal por red al cliente
        print(f"[Juego] Partida Iniciada {id_jugador}...")
        conn.sendall(b"INICIANDO:\n")
        
    except threading.BrokenBarrierError:
        print(f"[!] Error: La barrera se rompio inesperadamente para el Jugador {id_jugador}.")
    except Exception as e:
        print(f"[!] Error de red con Jugador {id_jugador}: {e}")
    finally:
        conn.close()
        print(f"[-] Conexion cerrada para el Jugador {id_jugador}.")

def main():
    try:
        n_jugadores = int(input("¿Cuantos jugadores se necesitan para iniciar la partida?: "))
        if n_jugadores < 2:
            print("Se necesitan al menos 2 jugadores.")
            sys.exit(1)
    except ValueError:
        print("Error: Debes ingresar un numero entero.")
        sys.exit(1)

    # Creamos la barrera pasandole el action
    barrera_juego = threading.Barrier(n_jugadores, action=iniciar_partida_server)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(n_jugadores)

        print(f"\n--- SERVIDOR DE JUEGO INICIADO ---")
        print(f"Lobby abierto en {HOST}:{PORT}...")

        hilos_jugadores = []
        
        for i in range(n_jugadores):
            conn, addr = server_sock.accept()
            id_jugador = i + 1
            
            t = threading.Thread(target=manejar_jugador, args=(conn, addr, barrera_juego, id_jugador))
            t.start()
            hilos_jugadores.append(t)

        for t in hilos_jugadores:
            t.join()
            
        print("\n[Servidor] El lobby ha expulsado a todos. Fin de la simulacion.")

if __name__ == "__main__":
    main()