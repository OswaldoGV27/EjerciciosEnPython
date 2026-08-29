# Libreria usada es Criptodome (Ejercicio 3)
# Recordatorio para intalarla 
# 1.-Abrir CMD
# 2.-Escribir: pip install pycryptome

# Biblioteca para numeros grandes especializada para RSA: cryptography (Ejercicio 2)
# pip install cryptography
from Crypto.Util.number import getPrime
from secrets import token_bytes
import random
from math import gcd

# Nuevas importaciones para RSA (Ejercicio 2)
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generar_primo(bits):
    return getPrime(bits)

tamaños = [256, 512, 1014, 2048, 3072]

print("========================Ejercicio 1========================")
for bits in tamaños:
    primo = generar_primo(bits)
    print(f"\nPrimo de {bits} bits:\n{primo}")

def generar_claves_rsa(bits=512):
    print("\n========================Ejercicio 2========================")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bits*2,  # Tamaño del módulo n = p*q
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def imprimir_claves(private_key, public_key):
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    print("\n=== CLAVE PRIVADA ===")
    print(priv_pem.decode())
    
    print("=== CLAVE PÚBLICA ===")
    print(pub_pem.decode())

private_key, public_key = generar_claves_rsa(512)
imprimir_claves(private_key, public_key)

def factoriza(n):
    factores = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factores.add(d)
            n //= d
        d += 1
    if n > 1:
        factores.add(n)
    return list(factores)

def es_generador(g, p):
    phi = p - 1
    factores = factoriza(phi)
    for q in factores:
        if pow(g, phi // q, p) == 1:
            return False
    return True

primos_15 = [getPrime(15) for _ in range(3)]
print("========================Ejercicio 3========================")
for p in primos_15:
    print(f"\nPrimo p = {p}")
    candidatos = list(range(2, p))
    random.shuffle(candidatos)
    for g in candidatos:
        if gcd(g, p) != 1:
            continue
        if es_generador(g, p):
            print(f"  Generador encontrado: g = {g}")
            break