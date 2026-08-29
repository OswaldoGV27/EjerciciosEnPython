SIZE = 16
# Permutación propuesta convertida a base 0
perm = [8, 6, 12, 1, 9, 4, 10, 0, 15, 7, 3, 14, 11, 2, 13, 5]
# Permutación inversa convertida a base 0
invperm = [7, 3, 13, 10, 5, 15, 1, 9, 0, 4, 6, 12, 2, 14, 11, 8]
# Aplicar permutación
def permutacion(data):
    return [data[perm[i]] for i in range(SIZE)]
# Aplicar permutación inversa
def inversa(data):
    return [data[invperm[i]] for i in range(SIZE)]
# Mostrar arreglo en hexadecimal
def muestra(data, etiqueta):
    print(f"{etiqueta}: ", end="")
for byte in data:
    print(f"{byte:02X}", end=" ")
print()
# Leer datos del usuario
def usuario():
    datos = []
    print(f"Ingrese {SIZE} valores en hexadecimal:")
    for i in range(SIZE):
        while True: 
            try:
                entrada = input(f"Valor {i+1}: ").strip()
                valor = int(entrada, 16)
                if 0 <= valor <= 255:
                    datos.append(valor)
                    break
                else:
                    print("Debe ser un número entre 00 y FF.")
            except ValueError:
                    print("No es valido lo que ingresaste ):")
            return datos

# Programa principal
def main():
    datos = usuario()
    muestra(datos, "Datos originales")
    permutado = permutacion(datos)
    muestra(permutado, "Después de permutar")
    recuperado = inversa(permutado)
    muestra(recuperado, "Después de invertir")
    if __name__ == "__main__": main()
