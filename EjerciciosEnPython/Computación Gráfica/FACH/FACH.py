import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np

# ==========================================
# 1. ESTRUCTURAS DE DATOS GLOBALES
# ==========================================
puntos = []
envolvente = []
poligono_transformado = []
poligono_recortado = []

dx = 0.0
dy = 0.0

x_min, x_max = 0, 100
y_min, y_max = 0, 100

# ==========================================
# 2. NÚCLEO MATEMÁTICO (Geometría Afín y Algoritmos)
# ==========================================

def producto_cruz(p1, p2, p3):
    # Calcula el determinante (pseudo producto cruz 2D) de los vectores (p1->p2) y (p1->p3).
    # Si el valor es > 0: El giro es a la izquierda (Es un vértice convexo válido).
    # Si el valor es <= 0: El giro es a la derecha o colineal (Vértice cóncavo, debe descartarse).
    
    return (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0])

def calcular_envolvente(lista_puntos):
    # Algoritmo Monotone Chain (Variante de Graham Scan).
    # Genera el polígono convexo mínimo que contiene todos los puntos ingresados.
    
    puntos_unicos = list(set(lista_puntos)) # Filtrar duplicados exactos en memoria
    if len(puntos_unicos) < 3:
        return []
        
    # Ordenamiento lexicográfico (Prioridad X, luego Y) para evitar uso de funciones trigonométricas
    ordenados = sorted(puntos_unicos)
    
    # Construcción de la Cáscara Inferior (Lower Hull)
    lower = []
    for p in ordenados:
        # Retroceso iterativo: elimina vértices si rompen la convexidad (giro a la derecha)
        while len(lower) >= 2 and producto_cruz(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
        
    # Construcción de la Cáscara Superior (Upper Hull)
    upper = []
    for p in reversed(ordenados):
        # Mismo principio, pero iterando de derecha a izquierda
        while len(upper) >= 2 and producto_cruz(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
        
    # Se concatena omitiendo el último vértice de cada mitad porque se superponen con los extremos
    return lower[:-1] + upper[:-1]

def aplicar_traslacion(puntos, tx, ty):
    # Aplica una traslación en el espacio afín sumando el vector de desplazamiento (tx, ty) a cada coordenada del polígono.

    if not puntos:
        return []
    return [(p[0] + tx, p[1] + ty) for p in puntos]

def recortar_poligono_sutherland_hodgman(poligono, xmin, ymin, xmax, ymax):
    # Algoritmo de Sutherland-Hodgman.
    # Recorta un polígono sujeto contra una ventana de recorte (Clip Window) plana.
    # Itera secuencialmente sobre los 4 planos de corte: Izquierda, Derecha, Abajo, Arriba.
    
    if not poligono or len(poligono) < 3:
        return []
    
    # Funciones booleanas para determinar si un vértice está dentro del espacio válido
    def inside_left(p): return p[0] >= xmin
    def inside_right(p): return p[0] <= xmax
    def inside_bottom(p): return p[1] >= ymin
    def inside_top(p): return p[1] <= ymax
    
    # Funciones de intersección: Calculan la coordenada exacta donde la arista corta la frontera
    def intersect_left(p1, p2):
        y = p1[1] + (p2[1]-p1[1]) * (xmin - p1[0]) / (p2[0]-p1[0])
        return (xmin, y)
    def intersect_right(p1, p2):
        y = p1[1] + (p2[1]-p1[1]) * (xmax - p1[0]) / (p2[0]-p1[0])
        return (xmax, y)
    def intersect_bottom(p1, p2):
        x = p1[0] + (p2[0]-p1[0]) * (ymin - p1[1]) / (p2[1]-p1[1])
        return (x, ymin)
    def intersect_top(p1, p2):
        x = p1[0] + (p2[0]-p1[0]) * (ymax - p1[1]) / (p2[1]-p1[1])
        return (x, ymax)
    
    pol = poligono[:]
    
    # PIPELINE DE RECORTE: Pasa la geometría a través de los 4 planos secuencialmente
    # El código procesa: Izquierda -> Derecha -> Inferior -> Superior
    
    # 1. Clip Izquierda
    output = []
    for i in range(len(pol)):
        p1 = pol[i]
        p2 = pol[(i+1) % len(pol)] # Siguiente vértice (cerrando el ciclo)
        if inside_left(p2):
            if not inside_left(p1): # Si entra a la región: Guarda intersección y destino
                output.append(intersect_left(p1, p2))
            output.append(p2)       # Si ambos están dentro: Guarda solo el destino
        elif inside_left(p1):       # Si sale de la región: Guarda solo la intersección
            output.append(intersect_left(p1, p2))
    pol = output

    # 2. Clip Derecha
    output = []
    for i in range(len(pol)):
        p1 = pol[i]
        p2 = pol[(i+1) % len(pol)]
        if inside_right(p2):
            if not inside_right(p1):
                output.append(intersect_right(p1, p2))
            output.append(p2)
        elif inside_right(p1):
            output.append(intersect_right(p1, p2))
    pol = output

    # 3. Clip Inferior
    output = []
    for i in range(len(pol)):
        p1 = pol[i]
        p2 = pol[(i+1) % len(pol)]
        if inside_bottom(p2):
            if not inside_bottom(p1):
                output.append(intersect_bottom(p1, p2))
            output.append(p2)
        elif inside_bottom(p1):
            output.append(intersect_bottom(p1, p2))
    pol = output

    # 4. Clip Superior
    output = []
    for i in range(len(pol)):
        p1 = pol[i]
        p2 = pol[(i+1) % len(pol)]
        if inside_top(p2):
            if not inside_top(p1):
                output.append(intersect_top(p1, p2))
            output.append(p2)
        elif inside_top(p1):
            output.append(intersect_top(p1, p2))
    pol = output
    
    # Filtro final de limpieza para evitar vértices superpuestos por errores de decimales
    if len(pol) >= 2:
        cleaned = [pol[0]]
        for p in pol[1:]:
            if abs(p[0]-cleaned[-1][0]) > 1e-8 or abs(p[1]-cleaned[-1][1]) > 1e-8:
                cleaned.append(p)
        pol = cleaned
    return pol

def area_poligono(poly):
    # Fórmula de Gauss / Shoelace Formula.
    # Calcula el área exacta de cualquier polígono simple (irregular o no) 
    # sumando los determinantes 2x2 de vértices adyacentes.

    if not poly or len(poly) < 3:
        return 0.0
    suma = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        suma += x1*y2 - x2*y1
    return abs(suma) / 2.0

# ==========================================
# 3. ACTUALIZACIÓN DE ESCENA
# ==========================================
def actualizar_geometria():
    # Aplica traslación y recorte a la envolvente actual.
    global poligono_transformado, poligono_recortado
    if not envolvente:
        poligono_transformado = []
        poligono_recortado = []
    else:
        poligono_transformado = aplicar_traslacion(envolvente, dx, dy)
        poligono_recortado = recortar_poligono_sutherland_hodgman(poligono_transformado,
                                                                   x_min, y_min, x_max, y_max)
    actualizar_grafica()

def actualizar_grafica():
    ax.clear()
    ax.set_title("Sistema de Calculo de Cáscara Convexa - FACH", fontsize=14, fontweight='bold')
    ax.set_xlim(x_min-5, x_max+5)
    ax.set_ylim(y_min-5, y_max+5)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xlabel("Eje X (mm)")
    ax.set_ylabel("Eje Y (mm)")
    
    # Siempre dibujar los puntos ingresados
    if puntos:
        xs, ys = zip(*puntos)
        ax.plot(xs, ys, 'ko', markersize=5, label='Vértices originales')
    
    # Dibujar envolvente solo si existe (se calculó con "Procesar")
    if envolvente:
        env_cerrada = envolvente + [envolvente[0]]
        exs, eys = zip(*env_cerrada)
        ax.plot(exs, eys, 'g--', linewidth=1.5, alpha=0.7, label='Envolvente convexa')
    
    # Dibujar polígono transformado (solo si hay envolvente)
    if envolvente and poligono_transformado:
        trans_cerrada = poligono_transformado + [poligono_transformado[0]]
        txs, tys = zip(*trans_cerrada)
        ax.plot(txs, tys, 'gray', linewidth=1, linestyle=':', label='Posición trasladada')
    
    # Dibujar polígono recortado (resultado final)
    if envolvente and poligono_recortado and len(poligono_recortado) >= 3:
        rec_cerrada = poligono_recortado + [poligono_recortado[0]]
        rxs, rys = zip(*rec_cerrada)
        ax.fill(rxs, rys, 'green', alpha=0.4, label='Área útil recortada')
        ax.plot(rxs, rys, 'g-', linewidth=2)
        ax.plot(rxs, rys, 'ro', markersize=4)
    elif envolvente and poligono_transformado and len(poligono_transformado) >= 3:
        # Si no se recortó (está dentro)
        rec_cerrada = poligono_transformado + [poligono_transformado[0]]
        rxs, rys = zip(*rec_cerrada)
        ax.fill(rxs, rys, 'green', alpha=0.4, label='Área útil (dentro de lámina)')
        ax.plot(rxs, rys, 'g-', linewidth=2)
        ax.plot(rxs, rys, 'ro', markersize=4)
    
    # Marco de la lámina
    lamina = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max), (x_min, y_min)]
    lx, ly = zip(*lamina)
    ax.plot(lx, ly, 'k-', linewidth=3, label='Límite de la lámina')
    
    # Métricas (solo si hay envolvente, si no, mostrar ceros)
    area_lamina = (x_max - x_min) * (y_max - y_min)
    if envolvente:
        area_util = area_poligono(poligono_recortado) if poligono_recortado else 0.0
        desperdicio = area_lamina - area_util
        porcentaje = (area_util / area_lamina) * 100 if area_lamina > 0 else 0
    else:
        area_util = 0.0
        desperdicio = area_lamina
        porcentaje = 0.0
    
    texto = (f"Área lámina: {area_lamina:.2f} mm²\n"
             f"Área útil: {area_util:.2f} mm²\n"
             f"Desperdicio: {desperdicio:.2f} mm²\n"
             f"Aprovechamiento: {porcentaje:.2f}%")
    
    # Cuadro de métricas de la figura.
    ax.text(0.98, 0.82, texto, transform=ax.transAxes,
            fontsize=9, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=0.85, edgecolor='black', boxstyle='round,pad=0.4'))
    
    ax.legend(loc='upper left', fontsize=8, framealpha=0.9)
    fig.canvas.draw()

# ==========================================
# 4. EVENTOS
# ==========================================
def al_hacer_clic(event):
    # Solo agrega el punto y limpia la envolvente anterior.
    if event.inaxes != ax:
        return
    global puntos, envolvente, poligono_transformado, poligono_recortado
    puntos.append((event.xdata, event.ydata))
    # Al añadir un nuevo punto, la envolvente anterior ya no es válida
    envolvente = []
    poligono_transformado = []
    poligono_recortado = []
    # También reseteamos traslaciones a cero para evitar confusiones
    global dx, dy
    dx = 0.0
    dy = 0.0
    slider_dx.set_val(dx)
    slider_dy.set_val(dy)
    actualizar_grafica()

def procesar(event):
    # Calcula la envolvente convexa con los puntos actuales.
    global envolvente
    if len(puntos) < 3:
        # Mostrar mensaje en la consola o en la gráfica
        ax.text(0.5, 0.5, "Se necesitan al menos 3 puntos", transform=ax.transAxes,
                ha='center', va='center', fontsize=12, color='red',
                bbox=dict(facecolor='yellow', alpha=0.8))
        fig.canvas.draw()
        # Desaparecer el mensaje después de 2 segundos
        plt.pause(2)
        actualizar_grafica()
        return
    envolvente = calcular_envolvente(puntos)
    actualizar_geometria()   # esto aplica traslación (dx,dy) y recorte

def limpiar(event):
    global puntos, envolvente, poligono_transformado, poligono_recortado, dx, dy
    puntos.clear()
    envolvente.clear()
    poligono_transformado.clear()
    poligono_recortado.clear()
    dx = 0.0
    dy = 0.0
    slider_dx.set_val(dx)
    slider_dy.set_val(dy)
    actualizar_grafica()

def actualizar_dx(val):
    global dx
    dx = val
    if envolvente:   # solo si ya hay una envolvente procesada
        actualizar_geometria()
    else:
        actualizar_grafica()

def actualizar_dy(val):
    global dy
    dy = val
    if envolvente:
        actualizar_geometria()
    else:
        actualizar_grafica()

# ==========================================
# 5. INTERFAZ
# ==========================================
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25)

ax_dx = plt.axes([0.2, 0.20, 0.6, 0.03])
ax_dy = plt.axes([0.2, 0.15, 0.6, 0.03])
slider_dx = Slider(ax_dx, 'Traslación X', -50, 50, valinit=dx, valstep=1)
slider_dy = Slider(ax_dy, 'Traslación Y', -50, 50, valinit=dy, valstep=1)
slider_dx.on_changed(actualizar_dx)
slider_dy.on_changed(actualizar_dy)

ax_procesar = plt.axes([0.3, 0.05, 0.2, 0.04])
ax_limpiar = plt.axes([0.55, 0.05, 0.2, 0.04])
btn_procesar = Button(ax_procesar, 'Procesar Geometría')
btn_limpiar = Button(ax_limpiar, 'Limpiar Lámina')
btn_procesar.on_clicked(procesar)
btn_limpiar.on_clicked(limpiar)

fig.canvas.mpl_connect('button_press_event', al_hacer_clic)

actualizar_grafica()
plt.show()