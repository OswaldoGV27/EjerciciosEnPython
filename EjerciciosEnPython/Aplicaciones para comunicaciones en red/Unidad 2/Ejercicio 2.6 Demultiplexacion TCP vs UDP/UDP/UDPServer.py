#!/usr/bin/env python3

import socket

HOST = '192.168.56.102'
PORT = 5050

def procesar_mensaje(mensaje):
    #Misma lógica matemática que el TCP
    partes = mensaje.split(':')
    if len(partes) != 3:
        return None, "ERROR: Formato incorrecto."

    id_cliente, operacion, valor_str = partes

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
        return id_cliente, "ERROR: Operación no soportada."

    return id_cliente, str(resultado)

def main():
    #Creamos un socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        server_sock.bind((HOST, PORT))
        
        print(f"Servidor UDP Matemático escuchando en el puerto {PORT}...")

        try:
            while True:
                #Recibimos el datagrama y la dirección del remitente (IP, Puerto)
                data, addr = server_sock.recvfrom(1024)
                
                mensaje = data.decode('utf-8').strip()
                print(f"[Paquete de {addr}] -> {mensaje}")

                #Procesamos los datos
                id_recibido, resultado = procesar_mensaje(mensaje)

                #Armamos la respuesta
                id_respuesta = id_recibido if id_recibido else "DESCONOCIDO"
                respuesta = f"{id_respuesta}:{resultado}\n"

                #Enviamos la respuesta de vuelta directamente al remitente (addr)
                server_sock.sendto(respuesta.encode('utf-8'), addr)

        except KeyboardInterrupt:
            print("\nApagando servidor UDP...")

if __name__ == "__main__":
    main()