import heapq
import math
import sys
import time
from collections import deque

sys.setrecursionlimit(10000)
INF = math.inf


class PesoNegativoError(ValueError):
    """Dijkstra no es aplicable cuando existe alguna arista con peso negativo."""


def _verificar_vertice(g, v, rol="inicial"):
    if v not in g.vertices:
        raise ValueError(f"El nodo {rol} '{v}' no existe en el grafo.")


def reconstruir_camino(pred, destino):
    
    if destino not in pred:
        return None
    camino, v = [], destino
    while v is not None:
        camino.append(v)
        v = pred[v]
    return camino[::-1]


def aristas_del_camino(g, camino):
    
    res = []
    for u, v in zip(camino, camino[1:]):
        a = g.obtener_arista(u, v)
        res.append((u, v, a["peso"]))
    return res


def medir_tiempo(fn, *args, repeticiones=200):
    
    t0 = time.perf_counter()
    for _ in range(repeticiones):
        fn(*args)
    return (time.perf_counter() - t0) / repeticiones


# ====================================================================== DFS
def dfs(g, inicio):
    
    _verificar_vertice(g, inicio)
    visitado, en_pila = set(), set()
    orden, arbol, ciclos, pasos = [], [], [], []
    padre = {inicio: None}

    def visitar(u):
        visitado.add(u)
        en_pila.add(u)
        orden.append(u)
        pasos.append(f"Visito {u}")
        for w, peso, _ in g.vecinos(u):
            if w not in visitado:
                arbol.append((u, w, peso))
                padre[w] = u
                pasos.append(f"  Arista {u}→{w} (peso {peso:g}) entra al árbol DFS")
                visitar(w)
            elif g.dirigido:
                if w in en_pila:          # arista de retroceso => ciclo dirigido
                    ciclos.append((u, w, peso))
                    pasos.append(f"  Arista {u}→{w}: retroceso, hay un ciclo")
            elif w != padre[u]:           # no dirigido: arista a visitado que no es el padre
                par = tuple(sorted((u, w)))
                if par not in {tuple(sorted((a, b))) for a, b, _ in ciclos}:
                    ciclos.append((u, w, peso))
                    pasos.append(f"  Arista {u}-{w}: ya visitado, forma un ciclo / camino alternativo")
        en_pila.discard(u)

    t0 = time.perf_counter()
    visitar(inicio)
    t = time.perf_counter() - t0
    todos = sorted(g.vertices)
    return {"inicio": inicio, "orden": orden, "aristas_arbol": arbol,
            "aristas_ciclo": ciclos, "alcanzables": sorted(visitado),
            "no_alcanzables": [v for v in todos if v not in visitado],
            "pasos": pasos, "tiempo_s": t}


def componentes_conexos(g):
    ady = {v: set() for v in g.vertices}
    for a in g.aristas:
        ady[a["origen"]].add(a["destino"])
        ady[a["destino"]].add(a["origen"])
    vistos, comps = set(), []

    def explorar(u, comp):
        vistos.add(u)
        comp.append(u)
        for w in sorted(ady[u]):
            if w not in vistos:
                explorar(w, comp)

    for v in sorted(g.vertices):
        if v not in vistos:
            comp = []
            explorar(v, comp)
            comps.append(sorted(comp))
    return comps


def es_conexo(g):
    return len(g.vertices) > 0 and len(componentes_conexos(g)) == 1


# ====================================================================== BFS
def bfs(g, inicio, destino=None):
    
    _verificar_vertice(g, inicio)
    if destino is not None:
        _verificar_vertice(g, destino, "destino")
    cola = deque([inicio])
    visto = {inicio}
    nivel = {inicio: 0}
    padre = {inicio: None}
    orden, arbol, pasos = [], [], []
    t0 = time.perf_counter()
    while cola:
        u = cola.popleft()
        orden.append(u)
        nuevos = []
        for w, peso, _ in g.vecinos(u):
            if w not in visto:
                visto.add(w)
                nivel[w] = nivel[u] + 1
                padre[w] = u
                cola.append(w)
                arbol.append((u, w, peso))
                nuevos.append(w)
        pasos.append({"paso": len(pasos) + 1, "extraido": u, "encolados": nuevos,
                      "cola": list(cola), "visitados": list(orden)})
    t = time.perf_counter() - t0
    niveles = {}
    for v, n in nivel.items():
        niveles.setdefault(n, []).append(v)
    niveles = {n: sorted(vs) for n, vs in sorted(niveles.items())}
    res = {"inicio": inicio, "orden": orden, "niveles": niveles, "aristas_arbol": arbol,
           "padre": padre, "distancia_aristas": nivel, "pasos": pasos,
           "alcanzables": sorted(visto), "tiempo_s": t,
           "no_alcanzables": [v for v in sorted(g.vertices) if v not in visto]}
    if destino is not None:
        res["destino"] = destino
        res["camino"] = reconstruir_camino(padre, destino)
        res["num_aristas"] = nivel.get(destino)
    return res


# ================================================================== DIJKSTRA
def dijkstra(g, origen, destino=None):
    
    _verificar_vertice(g, origen, "origen")
    if destino is not None:
        _verificar_vertice(g, destino, "destino")
    if g.tiene_pesos_negativos():
        neg = ", ".join(f"{a['origen']}-{a['destino']} ({a['peso']:g})" for a in g.aristas_negativas())
        raise PesoNegativoError("Dijkstra no es aplicable: hay pesos negativos → " + neg)
    dist = {v: INF for v in g.vertices}
    pred = {v: None for v in g.vertices}
    dist[origen] = 0.0
    heap = [(0.0, origen)]
    fijados, pasos = set(), []
    t0 = time.perf_counter()
    while heap:
        d, u = heapq.heappop(heap)
        if u in fijados:
            continue
        fijados.add(u)
        mejoras = []
        for w, peso, _ in g.vecinos(u):
            if w not in fijados and d + peso < dist[w]:
                dist[w] = d + peso
                pred[w] = u
                heapq.heappush(heap, (dist[w], w))
                mejoras.append(f"{w}={dist[w]:g}")
        pasos.append({"paso": len(pasos) + 1, "nodo_fijado": u, "distancia": d,
                      "relajaciones": mejoras})
    t = time.perf_counter() - t0
    tabla = [{"nodo": v, "distancia": (None if dist[v] == INF else dist[v]),
              "predecesor": pred[v]} for v in sorted(g.vertices)]
    res = {"origen": origen, "dist": dist, "pred": pred, "tabla": tabla,
           "pasos": pasos, "tiempo_s": t}
    if destino is not None:
        camino = reconstruir_camino(pred, destino) if dist[destino] < INF else None
        res.update({"destino": destino, "camino": camino,
                    "costo": None if camino is None else dist[destino],
                    "aristas_camino": [] if camino is None else aristas_del_camino(g, camino)})
    return res


def dijkstra_con_cierre(g, origen, destino, cerrar_vertices=(), cerrar_aristas=()):
    
    base = dijkstra(g, origen, destino)
    g2 = g.sin(cerrar_vertices, cerrar_aristas)
    if origen not in g2.vertices or destino not in g2.vertices:
        alt = None
    else:
        alt = dijkstra(g2, origen, destino)
    return {"original": base, "con_cierre": alt}


# ================================================================== KRUSKAL
class UnionFind:
    def __init__(self, elementos):
        self.padre = {e: e for e in elementos}
        self.rango = {e: 0 for e in elementos}

    def buscar(self, x):
        while self.padre[x] != x:
            self.padre[x] = self.padre[self.padre[x]]   # compresión de camino
            x = self.padre[x]
        return x

    def unir(self, a, b):
        ra, rb = self.buscar(a), self.buscar(b)
        if ra == rb:
            return False
        if self.rango[ra] < self.rango[rb]:
            ra, rb = rb, ra
        self.padre[rb] = ra
        if self.rango[ra] == self.rango[rb]:
            self.rango[ra] += 1
        return True


def verificar_para_arbol_expansion(g):
    
    if g.dirigido:
        raise ValueError("El grafo es dirigido: Kruskal/Prim requieren un grafo NO dirigido.")
    if not g.vertices:
        raise ValueError("El grafo no tiene vértices.")
    if not g.aristas:
        raise ValueError("El grafo no tiene aristas (no es ponderado ni conexo).")
    comps = componentes_conexos(g)
    if len(comps) > 1:
        det = " | ".join("{" + ", ".join(c) + "}" for c in comps)
        raise ValueError(f"El grafo NO es conexo ({len(comps)} componentes): {det}. "
                         "No existe un árbol de expansión; solo un bosque.")


def kruskal(g):
    verificar_para_arbol_expansion(g)
    t0 = time.perf_counter()
    ordenadas = sorted(g.aristas, key=lambda a: (a["peso"], min(a["origen"], a["destino"]),
                                                  max(a["origen"], a["destino"])))
    uf = UnionFind(g.vertices)
    arbol, aceptadas, rechazadas, pasos = [], [], [], []
    costo = 0.0
    for a in ordenadas:
        o, d, p = a["origen"], a["destino"], a["peso"]
        ro, rd = uf.buscar(o), uf.buscar(d)
        if uf.unir(o, d):
            arbol.append((o, d, p))
            aceptadas.append((o, d, p))
            costo += p
            pasos.append({"arista": f"{o}-{d}", "peso": p, "decision": "ACEPTADA",
                          "motivo": f"{o} y {d} estaban en componentes distintas"})
        else:
            rechazadas.append((o, d, p))
            pasos.append({"arista": f"{o}-{d}", "peso": p, "decision": "RECHAZADA",
                          "motivo": f"{o} y {d} ya están conectados: formaría un ciclo"})
    t = time.perf_counter() - t0
    return {"aristas_ordenadas": [(a["origen"], a["destino"], a["peso"]) for a in ordenadas],
            "aristas_arbol": arbol, "aceptadas": aceptadas, "rechazadas": rechazadas,
            "costo": costo, "pasos": pasos, "tiempo_s": t,
            "orden_seleccion": [f"{o}-{d}" for o, d, _ in arbol]}


# ===================================================================== PRIM
def prim(g, inicio):
    verificar_para_arbol_expansion(g)
    _verificar_vertice(g, inicio)
    t0 = time.perf_counter()
    en_arbol = {inicio}
    incorporados = [inicio]
    arbol, pasos = [], []
    costo = 0.0
    heap = []
    for w, p, _ in g.vecinos(inicio):
        heapq.heappush(heap, (p, inicio, w))
    while heap and len(en_arbol) < len(g.vertices):
        p, u, w = heapq.heappop(heap)
        if w in en_arbol:
            continue
        en_arbol.add(w)
        incorporados.append(w)
        arbol.append((u, w, p))
        costo += p
        pasos.append({"iteracion": len(arbol), "arista": f"{u}-{w}", "peso": p,
                      "incorporados": list(incorporados)})
        for x, px, _ in g.vecinos(w):
            if x not in en_arbol:
                heapq.heappush(heap, (px, w, x))
    t = time.perf_counter() - t0
    return {"inicio": inicio, "aristas_arbol": arbol, "incorporados": incorporados,
            "costo": costo, "pasos": pasos, "tiempo_s": t,
            "orden_seleccion": [f"{u}-{w}" for u, w, _ in arbol]}


# ================================================================ COMPARACIÓN
def _pares(aristas):
    return {frozenset((o, d)) for o, d, _ in aristas}


def comparar_kruskal_prim(kr, pr, t_kruskal=None, t_prim=None):
    """Devuelve las filas de la tabla comparativa y la verificación de costos."""
    mismo_costo = math.isclose(kr["costo"], pr["costo"], rel_tol=1e-9, abs_tol=1e-9)
    mismas = _pares(kr["aristas_arbol"]) == _pares(pr["aristas_arbol"])
    tk = kr["tiempo_s"] if t_kruskal is None else t_kruskal
    tp = pr["tiempo_s"] if t_prim is None else t_prim
    filas = [
        {"Criterio": "Costo total", "Kruskal": f"{kr['costo']:.2f}", "Prim": f"{pr['costo']:.2f}"},
        {"Criterio": "Número de aristas", "Kruskal": len(kr["aristas_arbol"]), "Prim": len(pr["aristas_arbol"])},
        {"Criterio": "Orden de selección", "Kruskal": ", ".join(kr["orden_seleccion"]),
         "Prim": ", ".join(pr["orden_seleccion"])},
        {"Criterio": "Tiempo de ejecución (ms)", "Kruskal": f"{tk * 1000:.4f}", "Prim": f"{tp * 1000:.4f}"},
    ]
    if mismo_costo:
        msg = ("Los costos coinciden. " + ("Además generaron exactamente el mismo árbol."
               if mismas else "Los árboles son distintos: hay empates de peso y ambos son óptimos."))
    else:
        msg = "¡Los costos NO coinciden! Revisa la implementación o los datos."
    return {"filas": filas, "mismo_costo": mismo_costo, "mismo_arbol": mismas, "mensaje": msg}


# ====================================================== ANÁLISIS ADICIONAL
def estaciones_criticas(g):
    """Vértices cuyo cierre desconecta la red (puntos de articulación), por fuerza bruta."""
    base = len(componentes_conexos(g))
    criticas = []
    for v in sorted(g.vertices):
        if len(componentes_conexos(g.sin(vertices=[v]))) > base:
            criticas.append(v)
    return criticas
