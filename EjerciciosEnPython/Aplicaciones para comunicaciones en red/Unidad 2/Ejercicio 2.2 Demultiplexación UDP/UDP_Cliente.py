import socket
import time

HOST = "192.168.1.15"  
PORT = 54321
bufferSize = 1024

aplicaciones = [
    "Cliente 1: Spotify",
    "Cliente 2: Netflix",
    "Cliente 3: Youtube",
    "Cliente 4: Discord",
    "Cliente 5: WhatsApp"
]

def simular_cliente(identificador_app):
    # Al crear un nuevo socket, Windows le asignará un puerto de origen (source port) aleatorio y único
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_client:
        
        # 1. Armamos y enviamos el mensaje con la identificación
        mensaje_a_enviar = f"Saludos desde {identificador_app}"
        udp_client.sendto(mensaje_a_enviar.encode('utf-8'), (HOST, PORT))
        
        # 2. Esperamos la respuesta del servidor para este cliente en específico
        try:
            udp_client.settimeout(2.0) # Un límite de 2 segundos para no quedarnos colgados si algo falla
            msgFromServer, addr = udp_client.recvfrom(bufferSize)
            print(f"Respuesta para {identificador_app.split(':')[1].strip()} -> {msgFromServer.decode('utf-8')}")
        except socket.timeout:
            print(f"Alerta: El servidor no respondió a {identificador_app}")

def main():
    print("Iniciando simulación de envío masivo de 5 clientes...\n")
    for app in aplicaciones:
        simular_cliente(app)
        # Una pequeñísima pausa para que en la consola del servidor se vea todo en orden
        time.sleep(0.2) 

if __name__ == "__main__":
    main()