import sys
import base64
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes

# 1. Generar clave 3DES aleatoria y guardarla en base64 en un archivo de texto
def generar_clave_y_guardar(nombre_archivo_clave):
    while True:
        clave = get_random_bytes(24)  # 24 bytes para clave 3DES (168 bits)
        try:
            clave = DES3.adjust_key_parity(clave)
            break
        except ValueError:
            continue  # Reintenta si la clave no es válida

    clave_b64 = base64.b64encode(clave).decode()

    with open(nombre_archivo_clave, "w") as archivo:
        archivo.write(clave_b64)

    print(f"Clave generada y guardada en: {nombre_archivo_clave}")

# 2. Cifrar un archivo de texto con 3DES y guardar en base64
def cifrar_archivo(nombre_archivo_clave, archivo_entrada, archivo_salida):
    with open(nombre_archivo_clave, "r") as archivo:
        clave_b64 = archivo.read().strip()

    clave = base64.b64decode(clave_b64)
    cifrador = DES3.new(clave, DES3.MODE_ECB)

    with open(archivo_entrada, "rb") as archivo:
        texto_plano = archivo.read()

    longitud_relleno = 8 - (len(texto_plano) % 8)
    texto_plano += bytes([longitud_relleno]) * longitud_relleno

    texto_cifrado = cifrador.encrypt(texto_plano)
    texto_cifrado_b64 = base64.b64encode(texto_cifrado).decode()

    with open(archivo_salida, "w") as archivo:
        archivo.write(texto_cifrado_b64)

    print(f"Archivo cifrado y guardado en: {archivo_salida}")

# 3. Descifrar archivo cifrado con 3DES
def descifrar_archivo(nombre_archivo_clave, archivo_entrada, archivo_salida):
    with open(nombre_archivo_clave, "r") as archivo:
        clave_b64 = archivo.read().strip()

    clave = base64.b64decode(clave_b64)
    cifrador = DES3.new(clave, DES3.MODE_ECB)

    with open(archivo_entrada, "r") as archivo:
        texto_cifrado_b64 = archivo.read()

    texto_cifrado = base64.b64decode(texto_cifrado_b64)
    texto_plano = cifrador.decrypt(texto_cifrado)

    longitud_relleno = texto_plano[-1]
    texto_plano = texto_plano[:-longitud_relleno]

    with open(archivo_salida, "wb") as archivo:
        archivo.write(texto_plano)

    print(f"Archivo descifrado y guardado en: {archivo_salida}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso del programa:")
        print("  Generar clave: python script.py -g <archivo_clave.txt>")
        print("  Cifrar: python script.py -c <archivo_clave.txt> <archivo_entrada.txt> <archivo_salida.txt>")
        print("  Descifrar: python script.py -d <archivo_clave.txt> <archivo_entrada.txt> <archivo_salida.txt>")
        sys.exit(1)

    if sys.argv[1] == "-g":
        if len(sys.argv) != 3:
            print("Uso: python script.py -g <archivo_clave.txt>")
            sys.exit(1)
        generar_clave_y_guardar(sys.argv[2])

    elif sys.argv[1] == "-c":
        if len(sys.argv) != 5:
            print("Uso: python script.py -c <archivo_clave.txt> <archivo_entrada.txt> <archivo_salida.txt>")
            sys.exit(1)
        cifrar_archivo(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "-d":
        if len(sys.argv) != 5:
            print("Uso: python script.py -d <archivo_clave.txt> <archivo_entrada.txt> <archivo_salida.txt>")
            sys.exit(1)
        descifrar_archivo(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        print("Opción no reconocida.")
