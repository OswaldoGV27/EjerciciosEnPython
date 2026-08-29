#pip install numpy scipy
import numpy as np
from scipy.optimize import linprog
import sys

def leer_lista_float(mensaje):
    """Ayuda a leer una lista de números separados por espacio."""
    while True:
        try:
            entrada = input(mensaje)
            datos = [float(x) for x in entrada.split()]
            return np.array(datos)
        except ValueError:
            print("Error: Asegúrate de ingresar solo números separados por espacios.")

def resolver_y_mostrar(c, A, b, etiqueta):
    print(f"\n--- RESOLVIENDO: {etiqueta} ---")
    
    # Scipy minimiza por defecto, así que invertimos C para maximizar
    c_neg = [-1 * i for i in c]
    
    res = linprog(c_neg, A_ub=A, b_ub=b, method='highs')
    
    if res.success:
        z_optimo = -res.fun  # Invertimos de nuevo para obtener el valor positivo
        print(f"Estado: Solución Óptima encontrada")
        print(f"Valor Z Máximo: {z_optimo}")
        print("Valores de las variables de decisión:")
        for i, val in enumerate(res.x):
            print(f"  x{i+1} = {val:.2f}")
        return z_optimo, res.x
    else:
        print("No se encontró solución óptima (el problema puede ser infactible o ilimitado).")
        return None, None

def main():
    print("=== SIMULADOR DE CAMBIO EN EL VECTOR A (SENSITIVIDAD) ===\n")
    
    # 1. Configuración Inicial
    try:
        n_vars = int(input("¿Cuántas variables de decisión (x) tienes?: "))
        n_restricciones = int(input("¿Cuántas restricciones tienes?: "))
    except ValueError:
        print("Por favor ingresa números enteros.")
        return

    print("\n--- PASO 1: DATOS DEL PROBLEMA ORIGINAL ---")
    
    # Leer Función Objetivo
    print(f"Ingresa los coeficientes de Z (separados por espacio). Ej: 3 5")
    c = leer_lista_float("Coeficientes Z (Max): ")
    if len(c) != n_vars:
        print(f"Error: Debes ingresar exactamente {n_vars} coeficientes.")
        return

    # Leer Matriz A
    print("\nIngresa los coeficientes de las restricciones (Matriz A).")
    print("Por cada restricción, ingresa los valores de x1, x2... separados por espacio.")
    A = []
    for i in range(n_restricciones):
        fila = leer_lista_float(f"Restricción {i+1} (lado izquierdo): ")
        if len(fila) != n_vars:
            print(f"Error: La fila debe tener {n_vars} números.")
            return
        A.append(fila)
    A = np.array(A)

    # Leer Vector b
    print("\nIngresa los valores del lado derecho (disponibilidad) separados por espacio.")
    b = leer_lista_float(f"Lado derecho (b): ")
    if len(b) != n_restricciones:
        print(f"Error: Debes ingresar {n_restricciones} valores.")
        return

    # 2. Resolver Original
    z_original, x_original = resolver_y_mostrar(c, A, b, "PROBLEMA ORIGINAL")
    
    if z_original is None:
        return

    # 3. Realizar el cambio en el Vector A
    while True:
        print("\n--- PASO 2: MODIFICAR EL VECTOR A ---")
        opcion = input("¿Deseas modificar una columna (vector tecnológico)? (s/n): ").lower()
        if opcion != 's':
            print("Saliendo del programa.")
            break
        
        try:
            col_idx = int(input(f"¿Qué variable quieres modificar? (1 a {n_vars}): ")) - 1
            if col_idx < 0 or col_idx >= n_vars:
                print("Índice fuera de rango.")
                continue
        except ValueError:
            print("Entrada inválida.")
            continue
            
        print(f"La columna actual para x{col_idx+1} es: {A[:, col_idx]}")
        print(f"Ingresa los NUEVOS coeficientes tecnológicos para x{col_idx+1}.")
        print(f"Necesitas ingresar {n_restricciones} valores (uno por cada restricción).")
        
        nueva_columna = leer_lista_float(f"Nuevos valores para x{col_idx+1}: ")
        
        if len(nueva_columna) != n_restricciones:
            print(f"Error: Debes ingresar exactamente {n_restricciones} valores.")
            continue
            
        # Crear copia de A para no borrar la original si queremos seguir probando
        A_nueva = A.copy()
        A_nueva[:, col_idx] = nueva_columna
        
        # 4. Resolver Modificado
        z_nuevo, x_nuevo = resolver_y_mostrar(c, A_nueva, b, "PROBLEMA MODIFICADO")
        
        # Comparación rápida
        if z_nuevo is not None:
            diff = z_nuevo - z_original
            print(f"\n--- CONCLUSIÓN ---")
            if diff > 0.0001:
                print(f"El cambio MEJORÓ la utilidad en: +{diff:.2f}")
            elif diff < -0.0001:
                print(f"El cambio EMPEORÓ la utilidad en: {diff:.2f}")
            else:
                print("El cambio NO afectó el valor de la utilidad total.")

if __name__ == "__main__":
    main()


#¿Cuántas variables...?: 2
#¿Cuántas restricciones...?: 2
#Coeficientes Z: 50 40
#Restricción 1 (Madera): 2 1
#Restricción 2 (Mano de obra): 1 2
#Lado derecho (b): 20 24

#(El programa te dará la solución original)
#¿Deseas modificar...?: s
#¿Qué variable...?: 1 (Queremos cambiar las mesas)
#Nuevos valores para x1: 1 2