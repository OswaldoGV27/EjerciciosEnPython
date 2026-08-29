import socket
import threading
import time
import random

HOST = '192.168.56.102'
PORT = 5050

# --- CREAMOS EL EVENTO GLOBAL PARA ESTE CLIENTE ---
evento_fin_partida = threading.Event()
mi_id_jugador = None

def escuchar_servidor(sock):
    global mi_id_jugador
    try:
        while True:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break
            
            mensajes = data.strip().split('\n')
            for msg in mensajes:
                if msg.startswith("ID:"):
                    mi_id_jugador = msg.split(":")[1]
                    print(f"Conectado. Soy el Jugador {mi_id_jugador}")
                
                elif msg.startswith("FIN:"):
                    perdedor = msg.split(":")[1]
                    print(f"\n[ALERTA DE RED] El servidor indica que el Jugador {perdedor} perdio!")
                    
                    # --- ACTIVAMOS EL EVENTO ---
                    #Esto rompera el ciclo 'while' del hilo principal al instante
                    evento_fin_partida.set()
                    return
    except Exception:
        evento_fin_partida.set()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print("Buscando partida...")
            sock.connect((HOST, PORT))
            
            hilo_red = threading.Thread(target=escuchar_servidor, args=(sock,), daemon=True)
            hilo_red.start()

            # Esperamos un instante a que el servidor nos asigne nuestro ID
            while mi_id_jugador is None and not evento_fin_partida.is_set():
                time.sleep(0.1)

            # --- CICLO DEL JUEGO ---
            #Mientras el Hilo Escucha no encienda el Evento, seguimos jugando
            while not evento_fin_partida.is_set():
                print(f"Jugador {mi_id_jugador} sigue jugando...")
                time.sleep(random.uniform(0.5, 1.5))
            
            # Si el codigo sale del while, es porque evento_fin_partida.is_set() == True
            print(f"Jugador {mi_id_jugador} ha sido notificado del fin de la partida.")

        except ConnectionRefusedError:
            print("No se pudo conectar al servidor.")

if __name__ == "__main__":
    main()