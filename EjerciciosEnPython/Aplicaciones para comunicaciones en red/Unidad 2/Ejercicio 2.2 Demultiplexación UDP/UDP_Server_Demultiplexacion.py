import socket
import threading

HOST = "192.168.1.15" 
PORT = 54321
bufferSize = 1024

# Diccionario para registrar { Puerto : Nombre_App }
clientes_registrados = {}
limite_clientes = 5

def procesar_peticion_udp(data, addr, sock):
    mensaje = data.decode('utf-8').strip()
    puerto_origen = addr[1] # ¡Aquí extraemos y usamos únicamente el puerto!
    
    # Buscamos el nombre de la aplicación usando solo el puerto
    nombre_app = clientes_registrados.get(puerto_origen, "Desconocido")
    print(f"[{nombre_app} - Puerto origen: {puerto_origen}] dice: {mensaje}")
    
    # Respondemos directamente a la aplicación
    respuesta = f"Hola {nombre_app}, el servidor recibió tu petición correctamente.".encode('utf-8')
    sock.sendto(respuesta, addr)

def main():
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((HOST, PORT))
    print(f"Servidor listo y esperando a {limite_clientes} clientes en el puerto {PORT}...")

    while len(clientes_registrados) < limite_clientes:
        data, addr = server_udp.recvfrom(bufferSize)
        puerto_origen = addr[1]
        mensaje = data.decode('utf-8').strip()
        
        # Si el puerto es nuevo, lo registramos
        if puerto_origen not in clientes_registrados:
            # Asumimos que el cliente envía un string como "Cliente 1: Spotify"
            # Separamos por los dos puntos para guardar solo el nombre de la app
            if ":" in mensaje:
                nombre_app = mensaje.split(":")[1].strip()
            else:
                nombre_app = f"App_{puerto_origen}"
                
            clientes_registrados[puerto_origen] = nombre_app
            print(f"--> Nuevo registro: {nombre_app} vinculado al puerto {puerto_origen}")
        
        # Lanzamos el hilo para atender la solicitud (demultiplexación)
        hilo = threading.Thread(target=procesar_peticion_udp, args=(data, addr, server_udp), daemon=True)
        hilo.start()

    print("\n¡Se alcanzó el límite de 5 clientes! El servidor sigue atendiendo exclusivamente a los puertos registrados.")
    
    # El servidor sigue vivo procesando solo a los 5 puertos conocidos
    while True:
        data, addr = server_udp.recvfrom(bufferSize)
        puerto_origen = addr[1]
        
        if puerto_origen in clientes_registrados:
            threading.Thread(target=procesar_peticion_udp, args=(data, addr, server_udp), daemon=True).start()

if __name__ == "__main__":
    main()