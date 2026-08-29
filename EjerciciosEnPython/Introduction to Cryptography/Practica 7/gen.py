def gen_llave(K):
    # Convertir la clave a binario de 32 bits (rellenando con ceros a la izquierda)
    K_bin = bin(K)[2:].zfill(32)
    subkeys = []
    
    for r in range(1, 6):  # 5 rondas (K1 a K5)
        inicio = 4 * r - 4   # Desplazamiento de 4 bits por ronda
        subkey = K_bin[inicio : inicio + 16]  # Extrae 16 bits
        subkeys.append(subkey)
    return subkeys

def main():
    # Clave y mensaje de ejemplo (en hexadecimal)
    K = 0x3A94D63F
    M = 0x26B7
    
    print(f"Clave principal (K): {hex(K)}")
    print(f"Mensaje (M): {hex(M)}\n")
    
    # Generar subclaves
    subkeys = gen_llave(K)
    
    # Mostrar las subclaves generadas
    print("Subclaves generadas:")
    for i, subkey in enumerate(subkeys, 1):
        # Convertir a hexadecimal (eliminando el prefijo '0b' y rellenando con ceros)
        subkey_hex = hex(int(subkey, 2))[2:].zfill(4)
        print(f"K{i}: {subkey} (bin) = 0x{subkey_hex} (hex)")

if __name__ == "__main__":
    main()
