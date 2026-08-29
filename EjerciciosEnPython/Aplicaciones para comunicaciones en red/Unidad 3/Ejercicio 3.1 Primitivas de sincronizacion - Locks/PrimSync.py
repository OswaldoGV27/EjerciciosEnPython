import threading
import logging
import random
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
SALDO = 10000
# Este es el mecanismo de sincronizacion que evitara las condiciones de carrera
lock_saldo = threading.Lock() 

def worker(num):
    global SALDO
    
    # Haremos que cada hilo intente hacer 3 operaciones para generar bastante trafico
    for_operations = 3
    
    for _ in range(for_operations):
        # Hacemos una pausa aleatoria antes de operar para que los hilos se mezclen y compitan
        time.sleep(random.uniform(0.1, 0.10))
        
        # Generamos la operacion aleatoria
        operacion = random.choice(['deposito', 'retiro'])
        monto = random.randint(100, 3000)
        
        #'''''SECCION CRITICA'''''
        # Solo un hilo a la vez puede entrar a esta estructura `with`
        with lock_saldo:
            if operacion == 'deposito':
                logging.debug(f"Iniciando {operacion} de ${monto}...")
                SALDO += monto
                logging.info(f"DEPOSITO EXITOSO. Nuevo Saldo: ${SALDO}")
                
            elif operacion == 'retiro':
                logging.debug(f"Intentando {operacion} de ${monto}...")
                #Validacion de saldo
                if SALDO >= monto:
                    SALDO -= monto
                    logging.info(f"RETIRO EXITOSO. Nuevo Saldo: ${SALDO}")
                else:
                    logging.warning(f"RETIRO RECHAZADO (Fondos insuficientes). Saldo actual: ${SALDO}")
        # Al salir de la estructura `with`, el candado se suelta automaticamente para el siguiente hilo
    return

#''''' Creacion y Ejecucion de Hilos '''''
threads = []
print(f"=== INICIANDO OPERACIONES BANCARIAS. SALDO INICIAL: ${SALDO} ===\n")

for i in range(5):
    #Ennumeramos los hilos
    t = threading.Thread(target=worker, args=(i,), name=f"Cliente-{i+1}")
    threads.append(t)
    t.start()

#Esperamos a que TODOS los hilos terminen sus operaciones antes de continuar
for t in threads:
    t.join()

print("\n" + "="*60)
print(f"TODOS LOS CLIENTES TERMINARON. SALDO FINAL DE LA CUENTA: ${SALDO}")
print("="*60)