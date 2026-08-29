import base64
import os
from random import randint

sbox = [0x4, 0xB, 0x1, 0xA, 0x7, 0x8, 0xE, 0xF,
        0x3, 0xD, 0x9, 0x5, 0x0, 0x6, 0x2, 0xC]
sbox_inv = [0xC, 0x2, 0xE, 0x8, 0x0, 0xB, 0xD, 0x4,
            0x5, 0xA, 0x3, 0x1, 0xF, 0x9, 0x6, 0x7]

def aplicar_sbox(b):
    return sum((sbox[(b >> (4 * (3 - i))) & 0xF] << (4 * (3 - i))) for i in range(4))

def aplicar_sbox_inv(b):
    return sum((sbox_inv[(b >> (4 * (3 - i))) & 0xF] << (4 * (3 - i))) for i in range(4))

perm = [8, 6, 12, 1, 9, 4, 10, 0, 15, 7, 3, 14, 11, 2, 13, 5]
invperm = [7, 3, 13, 10, 5, 15, 1, 9, 0, 4, 6, 12, 2, 14, 11, 8]

def permutar(b):
    bits = format(b, '016b')
    return int(''.join(bits[perm[i]] for i in range(16)), 2)

def permutar_inv(b):
    bits = format(b, '016b')
    return int(''.join(bits[invperm[i]] for i in range(16)), 2)

def gen_llaves(k):
    k_bin = bin(k)[2:].zfill(32)
    return [int(k_bin[4*i:4*i+16], 2) for i in range(5)]

def cifrar_bloque(b, subkeys):
    for i in range(5):
        b ^= subkeys[i]
        b = aplicar_sbox(b)
        b = permutar(b)
    return b

def descifrar_bloque(b, subkeys):
    for i in reversed(range(5)):
        b = permutar_inv(b)
        b = aplicar_sbox_inv(b)
        b ^= subkeys[i]
    return b

def b64encode_int(i, size_bytes):
    return base64.b64encode(i.to_bytes(size_bytes, 'big')).decode()

def b64decode_int(s):
    return int.from_bytes(base64.b64decode(s), 'big')

def texto_a_bloques(texto):
    bytes_data = texto.encode()
    if len(bytes_data) % 2 != 0:
        bytes_data += b'\x00'
    return [int.from_bytes(bytes_data[i:i+2], 'big') for i in range(0, len(bytes_data), 2)]

def bloques_a_texto(bloques):
    b = b''.join(b.to_bytes(2, 'big') for b in bloques)
    return b.rstrip(b'\x00').decode(errors='ignore')

def cifrar_cbc(texto, clave, iv):
    bloques = texto_a_bloques(texto)
    subkeys = gen_llaves(clave)
    cifrados = []
    anterior = iv
    for b in bloques:
        bloque = b ^ anterior
        c = cifrar_bloque(bloque, subkeys)
        cifrados.append(c)
        anterior = c
    return cifrados

def descifrar_cbc(bloques, clave, iv):
    subkeys = gen_llaves(clave)
    descifrados = []
    anterior = iv
    for c in bloques:
        bloque = descifrar_bloque(c, subkeys)
        descifrados.append(bloque ^ anterior)
        anterior = c
    return bloques_a_texto(descifrados)

def cifrar_ctr(texto, clave, iv):
    bloques = texto_a_bloques(texto)
    subkeys = gen_llaves(clave)
    cifrados = []
    for i, b in enumerate(bloques):
        keystream = cifrar_bloque((iv + i) & 0xFFFF, subkeys)
        cifrados.append(b ^ keystream)
    return cifrados

def descifrar_ctr(bloques, clave, iv):
    subkeys = gen_llaves(clave)
    descifrados = []
    for i, c in enumerate(bloques):
        keystream = cifrar_bloque((iv + i) & 0xFFFF, subkeys)
        descifrados.append(c ^ keystream)
    return bloques_a_texto(descifrados)

def bloques_a_base64(bloques):
    return base64.b64encode(b''.join(b.to_bytes(2, 'big') for b in bloques)).decode()

def base64_a_bloques(b64text):
    data = base64.b64decode(b64text)
    return [int.from_bytes(data[i:i+2], 'big') for i in range(0, len(data), 2)]

def main():
    print("\n--- Menu Toy Block Cipher ---")
    print("1. Cifrar mensaje")
    print("2. Descifrar mensaje")
    opcion = input("Selecciona una opción... ")

    if opcion == "1":
        print("\n--- CIFRADO ---")
        texto = input("Ingresa un texto plano de al menos 64 caracteres:\n")
        if len(texto) < 64:
            print("Error: El texto debe tener al menos 64 caracteres.")
            return
        clave = randint(0, 0xFFFFFFFF) #32 bits
        iv = randint(0, 0xFFFF) #16 bits
        modo = input("Modo de cifrado (CBC/CTR): ").strip().upper()
        subkeys = gen_llaves(clave)
        if modo == "CBC":
            cifrados = cifrar_cbc(texto, clave, iv)
        elif modo == "CTR":
            cifrados = cifrar_ctr(texto, clave, iv)
        else:
            print("Modo no válido.")
            return

        print("\n--- RESULTADOS ---")
        print("Clave (Base64):", b64encode_int(clave, 4))
        print("IV (Base64):", b64encode_int(iv, 2))
        print("Texto cifrado (Base64):", bloques_a_base64(cifrados))

    elif opcion == "2":
        print("\n--- DESCIFRADO ---")
        b64clave = input("Ingresa la clave en Base64: ").strip()
        b64iv = input("Ingresa el IV en Base64: ").strip()
        b64cifrado = input("Ingresa el texto cifrado en Base64: ").strip()
        modo = input("Modo de descifrado (CBC/CTR): ").strip().upper()

        try:
            clave = b64decode_int(b64clave)
            iv = b64decode_int(b64iv)
            bloques = base64_a_bloques(b64cifrado)
        except:
            print("Error al decodificar los datos. Verifica que estén en Base64.")
            return

        if modo == "CBC":
            texto = descifrar_cbc(bloques, clave, iv)
        elif modo == "CTR":
            texto = descifrar_ctr(bloques, clave, iv)
        else:
            print("Modo no válido.")
            return

        print("\n--- TEXTO DESCIFRADO ---")
        print(texto)

    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()
