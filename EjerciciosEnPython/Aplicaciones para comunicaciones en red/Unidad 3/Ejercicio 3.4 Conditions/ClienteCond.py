#!/usr/bin/env python3

import socket
import sys

HOST = '192.168.56.102' 
PORT = 5050

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print("Conectando al servidor del tablero...")
            sock.connect((HOST, PORT))
            print("Conectado. Esperando a que el servidor inicie la partida y te asigne tu turno...\n")

            while True:
                #El cliente se queda bloqueado aqui hasta que el servidor le mande algo
                data = sock.recv(1024).decode('utf-8')
                if not data:
                    break
                
                #Procesamos los mensajes por si el servidor mando varios pegados
                mensajes = data.strip().split('\n')
                for msg in mensajes:
                    
                    if msg.startswith("TURNO:"):
                        #Si es nuestro turno, imprimimos las instrucciones y leemos del teclado
                        instruccion = msg.split(":")[1]
                        print(f"{instruccion}")
                        
                        mi_jugada = input("Escribe tu jugada: ")
                        #Mandamos la jugada al servidor
                        sock.sendall(mi_jugada.encode('utf-8'))
                        print("Jugada enviada. Esperando a que los demas terminen su turno...\n")
                        
                    elif msg.startswith("FIN:"):
                        mensaje_fin = msg.split(":")[1]
                        print(f"\n{mensaje_fin}")
                        return

        except ConnectionRefusedError:
            print("Error: No se pudo conectar. ¿El servidor esta encendido?")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()