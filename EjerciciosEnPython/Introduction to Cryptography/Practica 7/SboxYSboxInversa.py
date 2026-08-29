# Definición de la S-box
sbox = [
    0x4, 0xB, 0x1, 0xA, 0x7, 0x8, 0xE, 0xF,
    0x3, 0xD, 0x9, 0x5, 0x0, 0x6, 0x2, 0xC
]

# Definición de la S-box inversa
sbox_inv = [
    0xC, 0x2, 0xE, 0x8, 0x0, 0xB, 0xD, 0x4,
    0x5, 0xA, 0x3, 0x1, 0xF, 0x9, 0x6, 0x7
]

# Función para aplicar la S-box a un bloque de 16 bits
def aplicar_sbox(bloque_16_bits):
    resultado = 0
    for i in range(4):
        nibble = (bloque_16_bits >> (4 * (3 - i))) & 0xF
        resultado = (resultado << 4) | sbox[nibble]
    return resultado

# Función para aplicar la S-box inversa
def aplicar_sbox_inversa(bloque_16_bits):
    resultado = 0
    for i in range(4):
        nibble = (bloque_16_bits >> (4 * (3 - i))) & 0xF
        resultado = (resultado << 4) | sbox_inv[nibble]
    return resultado

# Bucle principal
while True:
    print("\n--MENÚ--")
    print("1. Aplicar S-box")
    print("2. Aplicar S-box inversa")
    print("3. Salir")

    opcion = input("Selecciona una opción (1, 2 o 3): ")

    if opcion == "3":
        print("Saliendo del programa.")
        break
    elif opcion not in ["1", "2"]:
        print("Opción inválida. Intenta de nuevo.")
        continue

    entrada = input("Ingresa un bloque de 16 bits en hexadecimal (por ejemplo, 0x1234 o 1234): ")

    try:
        bloque = int(entrada, 16)
        if bloque > 0xFFFF:
            print("Error: El valor ingresado excede los 16 bits.")
        else:
            print(f"\nBloque original:     {hex(bloque)}")
            if opcion == "1":
                resultado = aplicar_sbox(bloque)
                print(f"Después de S-box:    {hex(resultado)}")
            else:
                resultado = aplicar_sbox_inversa(bloque)
                print(f"Después de S-box⁻¹:  {hex(resultado)}")
    except ValueError:
        print("Error: Entrada no válida. Asegúrate de ingresar un número hexadecimal.")
