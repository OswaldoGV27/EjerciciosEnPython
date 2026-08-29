import math

def calcular_vlsm():
    print("\n=== CALCULADORA VLSM ===")
    
    ip = input("Ingrese la red principal (ej: 192.168.1.0): ")
    prefijo = int(input("Ingrese el prefijo de red (ej: 24): "))
    num_subredes = int(input("Ingrese el número de subredes: "))
    
    hosts_por_subred = []
    for i in range(num_subredes):
        hosts = int(input(f"Número de hosts para la subred {i+1}: "))
        hosts_por_subred.append(hosts)
    
    hosts_por_subred.sort(reverse=True)
    
    hosts_totales = sum(hosts_por_subred)
    hosts_disponibles = (2 ** (32 - prefijo)) - 2
    if hosts_totales > hosts_disponibles:
        print(f"\n¡Error! La red {ip}/{prefijo} solo soporta {hosts_disponibles} hosts.")
        return
    
    subredes = []
    ip_actual = list(map(int, ip.split('.')))
    
    for i, hosts in enumerate(hosts_por_subred):
        n = math.ceil(math.log2(hosts + 2))
        R = (32 - prefijo) - n
        M = prefijo + R
        
        bits_ultimo_octeto = max(0, M - 24)
        salto = 2 ** (8 - bits_ultimo_octeto)
        
        ip_subred = ".".join(map(str, ip_actual))
        primer_host = ip_actual.copy()
        primer_host[3] += 1
        ultimo_host = ip_actual.copy()
        ultimo_host[3] += (2 ** (8 - bits_ultimo_octeto)) - 2
        broadcast = ip_actual.copy()
        broadcast[3] += (2 ** (8 - bits_ultimo_octeto)) - 1
        
        subredes.append({
            "Subred": i + 1,
            "Hosts": hosts,
            "IP Subred": ip_subred,
            "Máscara": f"/{M} (255.255.255.{256 - (2 ** (8 - bits_ultimo_octeto))})",
            "Primer Host": ".".join(map(str, primer_host)),
            "Último Host": ".".join(map(str, ultimo_host)),
            "Broadcast": ".".join(map(str, broadcast))
        })
        
        ip_actual[3] += (2 ** (8 - bits_ultimo_octeto))
    
    print("\nRESULTADOS:")
    print("-" * 100)
    print(f"{'Subred':<8} {'Hosts':<8} {'IP Subred':<15} {'Máscara':<25} {'Primer Host':<15} {'Último Host':<15} {'Broadcast':<15}")
    print("-" * 100)
    for subred in subredes:
        print(f"{subred['Subred']:<8} {subred['Hosts']:<8} {subred['IP Subred']:<15} {subred['Máscara']:<25} {subred['Primer Host']:<15} {subred['Último Host']:<15} {subred['Broadcast']:<15}")

calcular_vlsm()