import socket
import time
import random

HOST = '192.168.56.102'
PORT = 5050
NUM_JUGADORES = 4

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(NUM_JUGADORES)

    print(f"--- SERVIDOR INICIADO EN {PORT} ---")
    print(f"Esperando a {NUM_JUGADORES} jugadores...")
    
    clientes = []

    #Recibir a los jugadores
    for i in range(1, NUM_JUGADORES + 1):
        conn, addr = server_sock.accept()
        print(f"Jugador {i} conectado desde {addr}.")
        
        #Le enviamos al cliente que numero de jugador es
        conn.sendall(f"ID:{i}\n".format(i).encode('utf-8'))
        clientes.append(conn)
    print("\nTodos los jugadores conectados! La partida comienza.")

    #El servidor mantiene la partida un tiempo aleatorio
    tiempo_partida = random.uniform(6.0, 15.0)
    time.sleep(tiempo_partida)

    #Se selecciona al perdedor
    perdedor = random.randint(1, NUM_JUGADORES)
    print("\n" + "="*55)
    print(f"[SERVIDOR] El jugador {perdedor} ha perdido. Fin de la partida.")
    print("="*55 + "\n")

    #Notificar el "Evento Global" a todos los clientes por red
    for conn in clientes:
        try:
            #Enviamos el mensaje de FIN y el ID del perdedor
            conn.sendall(f"FIN:{perdedor}\n".encode('utf-8'))
            conn.close()
        except Exception:
            pass

    server_sock.close()
    print("--- SERVIDOR CERRADO CORRECTAMENTE ---")

if __name__ == "__main__":
    main()