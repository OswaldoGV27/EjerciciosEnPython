import random
from math import gcd, isqrt

def texto_a_entero(texto):
    return int.from_bytes(texto.encode('utf-8'), byteorder='big')

def entero_a_texto(numero):
    longitud = (numero.bit_length() + 7) // 8
    return numero.to_bytes(longitud, byteorder='big').decode('utf-8', errors='replace')

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)

def modinverso(e, phi):
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise Exception("No hay inverso modular.")
    return x % phi

def es_primo(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n-1
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generar_primo(bits):
    while True:
        p = random.getrandbits(bits)
        if p % 2 == 0:
            p += 1
        if es_primo(p):
            return p

def generar_clavesRSA(bits=64):
    p = generar_primo(bits)
    q = generar_primo(bits)
    while p == q:
        q = generar_primo(bits)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 5
    while gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)
    d = modinverso(e, phi)
    return (e, d, n, p, q)

def exp_mod_rapida(b, e, m):
    res = 1
    base = b % m
    while e > 0:
        if e % 2 == 1:
            res = (res * base) % m
        base = (base * base) % m
        e //= 2
    return res

def cifrar(m, e, n):
    return exp_mod_rapida(m, e, n)

def descifrar(c, d, n):
    return exp_mod_rapida(c, d, n)

def factor(n):
    for i in range(2, isqrt(n)+1):
        if n % i == 0:
            return i, n // i
    raise Exception('n no tiene dos factores primos pequeños')

def decrypt(n, e, c):
    p, q = factor(n)
    phi = (p-1)*(q-1)
    d = modinverso(e, phi)
    m = pow(c, d, n)
    return m

def menu():
    while True:
        print("\n===== MENÚ Práctica 9 (RSA) =====")
        print("1. Ejercicio 1: Encontrar m a partir de c, n, e.")
        print("2. Generar claves RSA de 64 bits.")
        print("3. Cifrar mensaje.")
        print("4. Descifrar mensaje.")
        print("5. Salir.")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            casos = [
                ('a', 10000000000, 10002200057, 5),
                ('b', 3200000, 250019000261, 5),
                ('c', 752582208917, 1000036000099, 7),
            ]
            for etiqueta, c, n, e in casos:
                m = decrypt(n, e, c)
                print(f"Resultado inciso {etiqueta})")
                print(f"c = {c}\nn = {n}\ne = {e}\nm (descifrado) = {m}")
                print("-" * 40)

        elif opcion == "2":
            e, d, n, p, q = generar_clavesRSA(64)
            print(f"\nClaves RSA generadas correctamente:")
            print(f"Clave pública: (e = {e}, n = {n})")
            print(f"Clave privada: (d = {d})")
            print(f"p = {p}")
            print(f"q = {q}")
            print(f"phi(n) = {(p-1)*(q-1)}")

        elif opcion == "3":
            e = int(input("Ingrese e: "))
            n = int(input("Ingrese n: "))
            texto = input("Ingrese el mensaje de texto a cifrar: ")
            m = texto_a_entero(texto)
            if m >= n:
                print("El mensaje es demasiado largo para la clave. Usa una clave más grande.")
                continue
            c = cifrar(m, e, n)
            print(f"\nMensaje cifrado (como entero): {c}")

        elif opcion == "4":
            d = int(input("Ingrese d (clave privada): "))
            n = int(input("Ingrese n: "))
            c = int(input("Ingrese el mensaje cifrado (como entero): "))
            m = descifrar(c, d, n)
            try:
                texto = entero_a_texto(m)
                print(f"\nMensaje descifrado: {texto}")
            except:
                print(f"\nDescifrado fallido. Mensaje como número: {m}")

        elif opcion == "5":
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
