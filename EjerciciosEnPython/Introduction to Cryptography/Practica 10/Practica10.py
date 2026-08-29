#pip install cryptography (Para instalar la librería)
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

def generar_clave(tamano_bits):
    if tamano_bits not in [128, 192, 256]:
        print("Tamaño inválido. Usa 128, 192 o 256.")
        return
    clave = os.urandom(tamano_bits // 8)
    clave_b64 = base64.b64encode(clave)
    with open("clave.txt", "wb") as f:
        f.write(clave_b64)
    print("Clave AES generada y guardada en 'clave.txt'.")

def cifrar_archivo_ctr(archivo_clave, archivo_entrada):
    with open(archivo_clave, "rb") as f:
        clave = base64.b64decode(f.read())

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(clave), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(archivo_entrada, "rb") as f:
        datos = f.read()

    cifrado = encryptor.update(datos) + encryptor.finalize()
    salida = base64.b64encode(iv + cifrado)

    with open("cifrado_ctr.txt", "wb") as f:
        f.write(salida)
    print("Archivo cifrado con AES-CTR y guardado como 'cifrado_ctr.txt'.")

def descifrar_archivo_ctr(archivo_clave, archivo_cifrado):
    with open(archivo_clave, "rb") as f:
        clave = base64.b64decode(f.read())
    with open(archivo_cifrado, "rb") as f:
        datos = base64.b64decode(f.read())

    iv, cifrado = datos[:16], datos[16:]
    cipher = Cipher(algorithms.AES(clave), modes.CTR(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    descifrado = decryptor.update(cifrado) + decryptor.finalize()

    with open("descifrado_ctr", "wb") as f:
        f.write(descifrado)
    print("Archivo descifrado con AES-CTR y guardado como 'descifrado_ctr'.")

def cifrar_archivo_gcm(archivo_clave, archivo_entrada):
    with open(archivo_clave, "rb") as f:
        clave = base64.b64decode(f.read())

    aesgcm = AESGCM(clave)
    nonce = os.urandom(12)

    with open(archivo_entrada, "rb") as f:
        datos = f.read()

    cifrado = aesgcm.encrypt(nonce, datos, None)
    salida = base64.b64encode(nonce + cifrado)

    with open("cifrado_gcm.txt", "wb") as f:
        f.write(salida)
    print("Archivo cifrado con AES-GCM y guardado como 'cifrado_gcm.txt'.")

def descifrar_archivo_gcm(archivo_clave, archivo_cifrado):
    with open(archivo_clave, "rb") as f:
        clave = base64.b64decode(f.read())
    with open(archivo_cifrado, "rb") as f:
        datos = base64.b64decode(f.read())

    nonce, cifrado = datos[:12], datos[12:]
    aesgcm = AESGCM(clave)
    descifrado = aesgcm.decrypt(nonce, cifrado, None)

    with open("descifrado_gcm", "wb") as f:
        f.write(descifrado)
    print("Archivo descifrado con AES-GCM y guardado como 'descifrado_gcm'.")

def menu():
    while True:
        print("\n===== Menú =====")
        print("1. Generar clave AES")
        print("\n===== Para Modo CTR =====")
        print("2. Cifrar archivo modo CTR")
        print("3. Descifrar archivo modo CTR")
        print("\n===== Para GCM =====")
        print("4. Cifrar archivo modo GCM")
        print("5. Descifrar archivo modo GCM")
        print("6. Salir")
        opcion = input("Elige una opción: ")

        try:
            if opcion == "1":
                bits = int(input("Tamaño de clave (128/192/256): "))
                generar_clave(bits)

            elif opcion == "2":
                clave = input("Ruta de archivo de clave: ")
                entrada = input("Ruta de archivo a cifrar: ")
                cifrar_archivo_ctr(clave, entrada)

            elif opcion == "3":
                clave = input("Ruta de archivo de clave: ")
                cifrado = input("Ruta de archivo cifrado (.txt): ")
                descifrar_archivo_ctr(clave, cifrado)

            elif opcion == "4":
                clave = input("Ruta de archivo de clave: ")
                entrada = input("Ruta de archivo a cifrar: ")
                cifrar_archivo_gcm(clave, entrada)

            elif opcion == "5":
                clave = input("Ruta de archivo de clave: ")
                cifrado = input("Ruta de archivo cifrado (.txt): ")
                descifrar_archivo_gcm(clave, cifrado)

            elif opcion == "6":
                print("Saliendo...")
                break

            else:
                print("Opción inválida.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    menu()
