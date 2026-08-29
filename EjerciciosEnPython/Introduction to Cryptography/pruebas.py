import os
import base64
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

# Función para generar una clave DES en Base64
def generate_des_key():
    key = get_random_bytes(8)  # DES usa claves de 8 bytes
    return base64.b64encode(key).decode()

# Función para cifrar un archivo con DES y almacenar el resultado en Base64
def encrypt_file(key_b64, input_filename, output_filename):
    key = base64.b64decode(key_b64)
    cipher = DES.new(key, DES.MODE_ECB)

    with open(input_filename, "rb") as f:
        plaintext = f.read()

    # Rellenar el texto si no es múltiplo de 8 bytes (DES necesita bloques de 8 bytes)
    padding_length = 8 - (len(plaintext) % 8)
    plaintext += bytes([padding_length]) * padding_length

    ciphertext = cipher.encrypt(plaintext)
    ciphertext_b64 = base64.b64encode(ciphertext).decode()

    with open(output_filename, "w") as f:
        f.write(ciphertext_b64)

    print(f"Archivo cifrado en {output_filename}")

# Función para descifrar un archivo con DES
def decrypt_file(key_b64, input_filename, output_filename):
    key = base64.b64decode(key_b64)
    cipher = DES.new(key, DES.MODE_ECB)

    with open(input_filename, "r") as f:
        ciphertext_b64 = f.read()

    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = cipher.decrypt(ciphertext)

    # Eliminar el padding
    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]

    with open(output_filename, "wb") as f:
        f.write(plaintext)

    print(f"Archivo descifrado en {output_filename}")

# Programa principal
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso:")
        print("  Generar clave: python des_cipher.py -g")
        print("  Cifrar: python des_cipher.py -e <clave_base64> <archivo_entrada> <archivo_salida>")
        print("  Descifrar: python des_cipher.py -d <clave_base64> <archivo_entrada> <archivo_salida>")
        sys.exit(1)

    if sys.argv[1] == "-g":
        print("Clave DES (Base64):", generate_des_key())

    elif sys.argv[1] == "-e":
        if len(sys.argv) != 5:
            print("Uso: python des_cipher.py -e <clave_base64> <archivo_entrada> <archivo_salida>")
            sys.exit(1)
        encrypt_file(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "-d":
        if len(sys.argv) != 5:
            print("Uso: python des_cipher.py -d <clave_base64> <archivo_entrada> <archivo_salida>")
            sys.exit(1)
        decrypt_file(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        print("Opción no reconocida.")