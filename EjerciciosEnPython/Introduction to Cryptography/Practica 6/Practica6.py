def gf2_multiplicacion_mod(a, b, m):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        carry = a & 0x80
        a <<= 1
        if carry:
            a ^= m
        a &= 0xFF
    return result

def generar_tabla_multiplicacion(m):
    size = 256  # 2^8
    tabla = []

    for i in range(size):
        fila = []
        for j in range(size):
            resultado = gf2_multiplicacion_mod(i, j, m)
            fila.append(f"{resultado:02X}")
        tabla.append(fila)

    with open("tabla_gf2_8.txt", "w") as f:
        for fila in tabla:
            f.write(" ".join(fila) + "\n")
    
    print("\nTabla de multiplicación GF(2^8) guardada en 'tabla_gf2_8.txt'.")

def encontrar_inverso(a_hex):
    a = int(a_hex, 16)
    if a == 0:
        print("El cero no tiene inverso en ningún campo.")
        return

    with open("tabla_gf2_8.txt", "r") as f:
        tabla = [line.strip().split() for line in f]

    for i in range(256):
        if tabla[a][i] == "01":
            print(f"Inverso de {a_hex.upper()} en GF(2^8): {i:02X}")
            return

    print(f"No se encontró inverso para {a_hex.upper()}.")

def multiplicar_polinomios_gf2_8(c, d, m):
    producto = [0] * 7 

    for i in range(4):
        for j in range(4):
            producto[i + j] ^= gf2_multiplicacion_mod(c[i], d[j], m)

    # Reducimos mod x^4 + 1 (es decir, x^4 ≡ 1)
    # x^4 → x^0, x^5 → x^1, x^6 → x^2
    reducido = producto[:4]
    if len(producto) > 4:
        for i in range(4, 7):
            reducido[i - 4] ^= producto[i]
    return reducido

def verificar_identidad():
    c = [0x02, 0x01, 0x01, 0x03]
    d = [0x0E, 0x09, 0x0D, 0x0B]
    m = 0x11B

    resultado = multiplicar_polinomios_gf2_8(c, d, m)
    print("Resultado de c(x) * d(x) mod (x^4 + 1):")
    print(" + ".join(f"{coef:02X}x^{i}" for i, coef in enumerate(resultado)))

    if resultado == [0x01, 0x00, 0x00, 0x00]:
        print("Verificado: c(x) * d(x) ≡ 1 mod (x^4 + 1)")
    else:
        print("No se cumple la identidad.")

def main():
    print("== MULTIPLICACIÓN EN GF(2^8) ==")
    a_hex = input("Introduce el valor de a en hexadecimal: ").strip()
    b_hex = input("Introduce el valor de b en hexadecimal: ").strip()
    m_hex = input("Introduce el polinomio irreducible m(x) en hexadecimal (grado ≤ 16): ").strip()

    a = int(a_hex, 16)
    b = int(b_hex, 16)
    m = int(m_hex, 16)

    product = gf2_multiplicacion_mod(a, b, m)
    print(f"\nProducto: {a_hex.upper()} × {b_hex.upper()} mod {m_hex.upper()} = {product:02X}")

    generar_tabla_multiplicacion(m)

    print("\n== INVERSO EN GF(2^8) ==")
    encontrar_inverso(a_hex)

    print("\n== VERIFICACIÓN DE PUNTO 5 ==")
    verificar_identidad()

if __name__ == "__main__":
    main()