import socket
import time

HOST = "192.168.56.102"
PORT = 5005
BUFFER_SIZE = 1024

# Creamos el socket UDP
server = socket.socket(socket.AF_INET, socket.socket.SOCK_DGRAM)
server.bind((HOST, PORT))

#Tiempo para el fin de transferencia si ya no recibe paquetes:
server.settimeout(3.0) 

print(f"Servidor UDP en puerto {PORT} esperando archivo...")

received_seqs = set() # Usamos un Set para contar solo paquetes unicos (sin duplicados)
total_packets_expected = 0
total_bytes_received = 0
start_time = None

while True:
    try:
        data, addr = server.recvfrom(BUFFER_SIZE)
        
        # Iniciar cronometro con el primer paquete que llegue
        if start_time is None:
            start_time = time.time() 
            print("¡Transferencia iniciada! Recibiendo datos...")

        # Separar el encabezado de los datos: seq|total|datos
        # maxsplit=2 asegura que no rompa el archivo si el texto original contiene el simbolo "|"
        parts = data.split(b"|", 2) 
        if len(parts) == 3:
            seq = int(parts[0].decode())
            total = int(parts[1].decode())
            chunk = parts[2]

            total_packets_expected = total
            received_seqs.add(seq) # Guardar el numero de secuencia
            total_bytes_received += len(chunk)

    except socket.timeout:
        # Si salto el timeout y ya habiamos empezado a recibir, significa que termino
        if start_time is not None:
            print("Timeout de 3s alcanzado. Calculando estadísticas...")
            break

# Restamos los 3 segundos de espera del timeout para tener el tiempo real
transfer_time = time.time() - start_time - 3.0 

# Calculos estadisticos
received_unique = len(received_seqs)
lost_packets = total_packets_expected - received_unique

# Formula de porcentaje de perdida
if total_packets_expected > 0:
    loss_percent = (lost_packets / total_packets_expected) * 100
else:
    loss_percent = 0

throughput = total_bytes_received / transfer_time if transfer_time > 0 else 0

print("\n" + "="*40)
print(" ESTADÍSTICAS DE TRANSFERENCIA UDP")
print("="*40)
print(f"Paquetes totales esperados: {total_packets_expected}")
print(f"Paquetes recibidos (únicos): {received_unique}")
print(f"Paquetes perdidos: {lost_packets}")
print(f"Porcentaje de pérdida: {loss_percent:.2f}%")
print(f"Total de bytes recibidos: {total_bytes_received} bytes")
print(f"Tiempo de transferencia: {transfer_time:.4f} segundos")
print(f"Throughput: {throughput:.2f} bytes/segundo")