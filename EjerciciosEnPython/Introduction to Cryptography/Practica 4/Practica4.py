import os
import base64
import sys
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

#  Generación de claves DES 
def generar_des_llave():
    clave = get_random_bytes(8)
    return base64.b64encode(clave).decode()

# Cifrado y Descifrado con DES 
def cifrar_archivo(clave_b64, archivo_entrada, archivo_salida):
    clave = base64.b64decode(clave_b64)
    cifrador = DES.new(clave, DES.MODE_ECB)

    with open(archivo_entrada, "rb") as archivo:
        texto_plano = archivo.read()

    longitud_relleno = 8 - (len(texto_plano) % 8)
    texto_plano += bytes([longitud_relleno]) * longitud_relleno

    texto_cifrado = cifrador.encrypt(texto_plano)
    texto_cifrado_b64 = base64.b64encode(texto_cifrado).decode()

    with open(archivo_salida, "w") as archivo:
        archivo.write(texto_cifrado_b64)

    print(f"Archivo cifrado en {archivo_salida}")

def decifrar_archivo(clave_b64, archivo_entrada, archivo_salida):
    clave = base64.b64decode(clave_b64)
    cifrador = DES.new(clave, DES.MODE_ECB)

    with open(archivo_entrada, "r") as archivo:
        texto_cifrado_b64 = archivo.read()

    texto_cifrado = base64.b64decode(texto_cifrado_b64)
    texto_plano = cifrador.decrypt(texto_cifrado)

    # Eliminar el relleno
    longitud_relleno = texto_plano[-1]
    texto_plano = texto_plano[:-longitud_relleno]

    with open(archivo_salida, "wb") as archivo:
        archivo.write(texto_plano)

    print(f"Archivo descifrado en {archivo_salida}")

# Generación de subclaves S-DES
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]   

def permutar(bits: str, tabla: list) -> str:
    return ''.join(bits[i - 1] for i in tabla)

def desplazar_izquierda(bits: str, n: int) -> str:
    return bits[n:] + bits[:n]

def generar_subclaves(clave_binaria: str) -> tuple:
    clave_permutada = permutar(clave_binaria, P10)
    izquierda, derecha = clave_permutada[:5], clave_permutada[5:]

    izquierda1 = desplazar_izquierda(izquierda, 1)
    derecha1 = desplazar_izquierda(derecha, 1)
    k1 = permutar(izquierda1 + derecha1, P8)

    izquierda2 = desplazar_izquierda(izquierda1, 2)
    derecha2 = desplazar_izquierda(derecha1, 2)
    k2 = permutar(izquierda2 + derecha2, P8)

    return k1, k2

# Codificación y Decodificación en Base64
def binario_a_base64(binario: str) -> str:
    datos_bytes = int(binario, 2).to_bytes((len(binario) + 7) // 8)
    return base64.b64encode(datos_bytes).decode()

def base64_a_binario(cadena_base64: str, longitud_original: int) -> str:
    datos_bytes = base64.b64decode(cadena_base64)
    binario = ''.join(f"{byte:08b}" for byte in datos_bytes)
    return binario[:longitud_original]

# Programa Principal
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  Generar clave DES: python script.py -g")
        print("  Cifrar archivo: python script.py -e <clave_base64> <archivo_entrada> <archivo_salida>")
        print("  Descifrar archivo: python script.py -d <clave_base64> <archivo_entrada> <archivo_salida>")
        print("  Generar subclaves S-DES: python script.py -s <clave_binaria_10bits>")
        print("  Codificar binario a Base64: python script.py -b64e <cadena_binaria>")
        print("  Decodificar Base64 a binario: python script.py -b64d <cadena_base64> <longitud_original>")
        sys.exit(1)

    if sys.argv[1] == "-g":
        print("Clave DES (Base64):", generar_des_llave())

    elif sys.argv[1] == "-c":
        if len(sys.argv) != 5:
            print("Uso: python script.py -e <clave_base64> <archivo_entrada> <archivo_salida>")
            sys.exit(1)
        cifrar_archivo(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "-d":
        if len(sys.argv) != 5:
            print("Uso: python script.py -d <clave_base64> <archivo_entrada> <archivo_salida>")
            sys.exit(1)
        decifrar_archivo(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "-k":
        if len(sys.argv) != 3:
            print("Uso: python script.py -k <clave_binaria_10bits>")
            sys.exit(1)
        k1, k2 = generar_subclaves(sys.argv[2])
        print("K1:", k1)
        print("K2:", k2)

    elif sys.argv[1] == "-bb64":
        if len(sys.argv) != 3:
            print("Uso: python script.py -bb64 <cadena_binaria>")
            sys.exit(1)
        print("Base64:", binario_a_base64(sys.argv[2]))

    elif sys.argv[1] == "-b64b":
        if len(sys.argv) != 4:
            print("Uso: python script.py -b64b <cadena_base64> <longitud_original>")
            sys.exit(1)
        print("Binario:", base64_a_binario(sys.argv[2], int(sys.argv[3])))

    else:
        print("Opción no reconocida.")
