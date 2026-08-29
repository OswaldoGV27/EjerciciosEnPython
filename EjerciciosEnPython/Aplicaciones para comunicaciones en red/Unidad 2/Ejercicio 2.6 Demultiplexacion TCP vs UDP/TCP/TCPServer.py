#!/usr/bin/env python3

import socket
import threading

HOST = '192.168.56.102' 
PORT = 5050

# Estructura requerida: clientes[socket] = ID_CLIENTE
clientes = {}
# Candado para evitar condiciones de carrera al modificar el diccionario desde múltiples hilos
clientes_lock = threading.Lock()
# Contador global para asignar IDs únicos
contador_clientes = 0 

def procesar_mensaje(mensaje):
    #Retorna una tupla: (id_cliente, resultado_o_error)
    partes = mensaje.split(':')
    # Validamos la estructura básica
    if len(partes) != 3:
        return None, "ERROR: Formato incorrecto."

    id_cliente, operacion, valor_str = partes

    #Validamos que el valor sea numérico
    try:
        valor = int(valor_str)
    except ValueError:
        return id_cliente, "ERROR: El valor no es numérico."

    if operacion == 'SQR':
        resultado = valor ** 2
    elif operacion == 'CUBE':
        resultado = valor ** 3
    elif operacion == 'NEG':
        resultado = -valor
    else:
        return id_cliente, f"ERROR: Operación no soportada."

    return id_cliente, str(resultado)

def manejar_cliente(conn, addr):
    global contador_clientes

    # --- FASE DE HANDSHAKE (SALUDO INICIAL) ---
    with clientes_lock:
        contador_clientes += 1
        id_asignado = f"Cliente_{contador_clientes}"
        clientes[conn] = id_asignado # Lo registramos inmediatamente

    print(f"\n[+] CONEXIÓN: {addr} ha sido registrado como '{id_asignado}'")
    
    # Le enviamos un mensaje especial al cliente diciéndole quién es
    mensaje_bienvenida = f"ASSIGN:{id_asignado}\n"
    conn.sendall(mensaje_bienvenida.encode('utf-8'))

    # --- FASE DE COMUNICACIÓN NORMAL ---
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break 

                mensaje = data.decode('utf-8').strip()
                id_recibido, resultado = procesar_mensaje(mensaje)

                # Armamos la respuesta según el formato <ID_CLIENTE>:<RESULTADO>
                respuesta = f"{id_recibido}:{resultado}\n"
                conn.sendall(respuesta.encode('utf-8'))

            except ConnectionResetError:
                print(f"\n[!] DESCONEXIÓN ABRUPTA: Se perdió a {id_asignado}.")
                break
            except Exception as e:
                print(f"\n[!] ERROR con {id_asignado}: {e}")
                break

    # Cuando el ciclo termina por desconexión
    with clientes_lock:
        if conn in clientes:
            id_guardado = clientes.pop(conn)
            print(f"\n[-] DESCONEXIÓN: {id_guardado} abandonó el servidor.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(10)

        print(f"Servidor Autoritativo escuchando en el puerto {PORT}...")

        try:
            while True:
                conn, addr = server_sock.accept()
                # Por cada cliente, se crea un nuevo hilo que lo atiende
                hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
                hilo_cliente.daemon = True 
                hilo_cliente.start()
        except KeyboardInterrupt:
            print("\nApagando servidor...")

if __name__ == "__main__":
    main()