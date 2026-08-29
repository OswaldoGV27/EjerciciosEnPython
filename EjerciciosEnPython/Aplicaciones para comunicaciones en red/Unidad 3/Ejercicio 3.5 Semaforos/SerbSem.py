import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 65432
MAX_JUGADORES = 5

# Mecanismos de Sincronización
arena_semaphore = threading.Semaphore(MAX_JUGADORES)
data_lock = threading.Lock()

arena_state = {}

def handle_player(conn, addr):
    player_id = f"{addr[1]}"
    print(f"[CONEXIÓN] Intento de ingreso: {player_id}")
    
    try:
        # Intentar entrar a la arena (Semaforo)
        conn.sendall(b"Esperando espacio en la arena...")
        with arena_semaphore:
            print(f"[ARENA] {player_id} ha entrado a la arena.")
            conn.sendall(b"ENTRADA_CONCEDIDA")
            
            # Inicializar estado en memoria compartida
            with data_lock:
                arena_state[player_id] = {"salud": 100, "pos": (0,0), "activo": True}

            while True:
                data = conn.recv(1024).decode()
                if not data or data == "QUIT":
                    break
                
                # Procesar actualización de estado
                try:
                    hp, x, y = data.split(',')
                    with data_lock:
                        arena_state[player_id].update({
                            "salud": int(hp),
                            "pos": (int(x), int(y))
                        })
                    
                    if int(hp) <= 0:
                        print(f"[MUERTE] Jugador {player_id} ha caído.")
                        break
                except ValueError:
                    continue

    except Exception as e:
        print(f"[ERROR] Con {player_id}: {e}")
    finally:
        #Liberar recursos y espacio cuando un jugador muere
        with data_lock:
            if player_id in arena_state:
                del arena_state[player_id]
        conn.close()
        print(f"[DESCONEXIÓN] {player_id} salió. Espacio liberado.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_player, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()