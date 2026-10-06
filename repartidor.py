import heapq

grafo = {
    'A': {'G': 9, 'N': 5}, 'B': {'S': 4, 'C': 1, 'I': 3, 'D': 5},
    'C': {'B': 1, 'S': 2, 'F': 8, 'E': 10, 'P': 21}, 'D': {'B': 5, 'O': 13, 'T': 6, 'E': 2},
    'E': {'C': 10, 'F': 12, 'D': 2, 'T': 2, 'L': 7}, 'F': {'I': 7, 'C': 8, 'E': 12},
    'G': {'A': 9}, 'H': {}, 'I': {'B': 3, 'F': 7}, 'J': {'T': 9}, 'K': {}, 'L': {'E': 7},
    'M': {}, 'N': {'A': 5, 'Q': 4}, 'O': {'D': 13}, 'P': {'C': 21}, 'Q': {'N': 4},
    'R': {}, 'S': {'B': 4, 'C': 2}, 'T': {'D': 6, 'E': 2, 'J': 9}
}

def dijkstra_ruta(grafo, origen):
    dist = {nodo: float("inf") for nodo in grafo}
    prev = {nodo: None for nodo in grafo}
    dist[origen] = 0
    cola = [(0, origen)]
    cerrados = set()

    while cola:
        d, u = heapq.heappop(cola)
        if u in cerrados:
            continue
        cerrados.add(u)

        for v, peso in grafo[u].items():
            if d + peso < dist[v]:
                dist[v] = d + peso
                prev[v] = u
                heapq.heappush(cola, (dist[v], v))
    return dist, prev

def obtener_camino(prev, destino):
    camino = []
    actual = destino
    while actual is not None:
        camino.insert(0, actual)
        actual = prev[actual]
    return camino

sitios_utiles = {'F': ['recoger_pedido_1', 'recoger_pedido_2'], 'T': ['recoger_pedido_3']}
pendientes_entrega = {}
posicion_actual = 'S'
coste_total = 0
ruta_total = ['S']

print(" SIMULACIÓN DE LA RUTA DEL REPARTIDOR ")

while sitios_utiles or pendientes_entrega:
    dist, prev = dijkstra_ruta(grafo, posicion_actual)
    
    candidatos = list(sitios_utiles.keys()) + list(pendientes_entrega.keys())
    candidatos = list(set(candidatos))
    
    mejor_nodo = None
    mejor_dist = float('inf')
    
    for nodo in candidatos:
        if dist[nodo] < mejor_dist:
            mejor_dist = dist[nodo]
            mejor_nodo = nodo
            
    camino = obtener_camino(prev, mejor_nodo)
    ruta_total.extend(camino[1:])
    coste_total += mejor_dist
    posicion_actual = mejor_nodo
    
    print(f"\nMe muevo a '{mejor_nodo}' (Coste tramo: {mejor_dist}). Camino: {' -> '.join(camino)}")
    
    if mejor_nodo in sitios_utiles:
        acciones = sitios_utiles.pop(mejor_nodo)
        for accion in acciones:
            print(f"  [+] Acción: {accion}")
            if accion == 'recoger_pedido_1': 
                pendientes_entrega['T'] = pendientes_entrega.get('T', []) + ['entregar_pedido_1']
            if accion == 'recoger_pedido_2': 
                pendientes_entrega['E'] = pendientes_entrega.get('E', []) + ['entregar_pedido_2']
            if accion == 'recoger_pedido_3': 
                pendientes_entrega['D'] = pendientes_entrega.get('D', []) + ['entregar_pedido_3']
                
    if mejor_nodo in pendientes_entrega:
        acciones = pendientes_entrega.pop(mejor_nodo)
        for accion in acciones:
            print(f"  [-] Acción: {accion}")

print(f"\n RESULTADO FINAL ")
print(f"Ruta completa seguida: {' -> '.join(ruta_total)}")
print(f"Coste total: {coste_total}")