import socket
import threading
import time

HOST = '192.168.56.102'
PORT = 5050
NUM_HILOS_POOL = 3 #Numero maximo de hilos permitidos

def manejar_hilo_control(id_hilo, server_sock):
    while True:
        print(f"[Hilo {id_hilo}] Listo y esperando conexión en accept()...")
        
        # RF1.1 El hilo se bloquea aquí hasta que llegue un cliente
        conn, addr = server_sock.accept()
        
        # RF1.4 Identificación por tupla completa
        local_info = conn.getsockname()
        peer_info = conn.getpeername()
        tupla_id = f"LOCAL({local_info[0]}:{local_info[1]}) <-> REMOTO({peer_info[0]}:{peer_info[1]})"
        
        print(f"\n[Hilo {id_hilo}] [+] Conexión establecida!")
        print(f"[Hilo {id_hilo}] Identificador de Sesión: {tupla_id}")

        with conn:
            try:
                while True:
                    # RF1.2 Esperamos el mensaje de Keep-Alive
                    conn.settimeout(5.0)  # Ponemos un timeout de 5 segundos (si no llega en 5s, asumimos que falla)
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    mensaje = data.decode('utf-8').strip()
                    if mensaje == "Keep-Alive":
                        print(f"[Hilo {id_hilo}] Heartbeat recibido de {peer_info[1]}")
                        conn.sendall(b"ACK-Alive\n")
                    else:
                        print(f"[Hilo {id_hilo}] Comando desconocido: {mensaje}")
                        conn.sendall(b"ERROR: Comando no soportado\n")

            except socket.timeout:
                print(f"\n[Hilo {id_hilo}] [!] TIMEOUT: El cliente dejó de enviar Keep-Alives.")
            except Exception as e:
                print(f"\n[Hilo {id_hilo}] [!] ERROR: {e}")
            
            # RF1.3 Limpiar estado y reponer
            print(f"[Hilo {id_hilo}] [-] Cerrando canal. Regresando a la funcion de accept()...\n")

def main():
    # Configuramos el socket principal
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    # Sala de espera del server
    server_sock.listen(10)

    print(f"--- Examen 2 SERVIDOR TCP ---")
    print(f"Escuchando en {HOST}:{PORT} con un pool de {NUM_HILOS_POOL} hilos.\n")

    # RF1.1 Pre-asignación del pool de hilos
    hilos = []
    for i in range(NUM_HILOS_POOL):
        t = threading.Thread(target=manejar_hilo_control, args=(i+1, server_sock))
        t.daemon = True
        t.start()
        hilos.append(t)

    try:
        # El hilo principal se queda vivo para mantener el proceso
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nApagando servidor...")

if __name__ == "__main__":
    main()