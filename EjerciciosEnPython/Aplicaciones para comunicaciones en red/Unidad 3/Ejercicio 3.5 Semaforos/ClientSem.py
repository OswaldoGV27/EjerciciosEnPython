import socket
import time
import random

HOST = '127.0.0.1'
PORT = 65432

def start_player():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    # Recibir estado inicial
    msg = client.recv(1024).decode()
    print(f"[SERVIDOR]: {msg}")
    
    if "Esperando" in msg:
        status = client.recv(1024).decode()
        if status == "ENTRADA_CONCEDIDA":
            print("[SISTEMA] ¡Has entrado a la arena!")

    # Atributos del jugador
    salud = 100
    pos_x, pos_y = random.randint(0, 100), random.randint(0, 100)

    try:
        while salud > 0:
            # Simular combate: reducción aleatoria de salud
            salud -= random.randint(2, 5)
            if salud < 0: salud = 0
            
            # Simular movimiento
            pos_x += random.randint(-3, 3)
            pos_y += random.randint(-1, 1)

            # Enviar actualización: HP,X,Y
            update = f"{salud},{pos_x},{pos_y}"
            client.sendall(update.encode())
            
            print(f"[ESTADO] Salud: {salud}% | Pos: ({pos_x}, {pos_y})")
            time.sleep(5) # Intervalo de actualización

        print("[SISTEMA] Has muerto. Abandonando arena...")
        client.sendall(b"QUIT")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_player()