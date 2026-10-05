from datetime import datetime

from .algoritmos import componentes_conexos, estaciones_criticas, es_conexo


def _nombre(g, v):
    return g.vertices[v].get("nombre", v)


def _camino_txt(g, camino):
    return " → ".join(f"{_nombre(g, v)} ({v})" for v in camino)


def recomendaciones(g, res):
    
    rec = []
    unidad = (g.unidades() or [""])[0]
    grados = g.grados()
    if not g.dirigido and grados:
        gmax = max(grados.values())
        hubs = [v for v, d in grados.items() if d == gmax]
        rec.append(f"Las estaciones con más conexiones (grado {gmax}) son "
                   + ", ".join(_nombre(g, v) for v in hubs)
                   + ". Son los nodos de transbordo más importantes de la red; conviene reforzar su "
                     "capacidad y señalización.")
        crit = estaciones_criticas(g)
        if crit:
            rec.append("Si se cierra cualquiera de estas estaciones la red se parte en componentes "
                       "desconectadas: " + ", ".join(_nombre(g, v) for v in crit)
                       + ". Hay que prever rutas alternativas (otras líneas, caminata o transporte "
                         "terrestre) para esos casos.")
        else:
            rec.append("Ninguna estación es crítica: la red sigue conectada ante el cierre de cualquiera.")
    kr = res.get("kruskal")
    if kr:
        rec.append(f"El árbol de expansión mínima conecta las {len(g.vertices)} estaciones con costo total "
                   f"{kr['costo']:.2f} {unidad}. Los {len(kr['rechazadas'])} tramo(s) que no entran forman "
                   "ciclos: son la redundancia de la red (rutas alternativas) y no son imprescindibles "
                   "para conectar todo.")
    dj, bf = res.get("dijkstra"), res.get("bfs")
    if dj and dj.get("camino"):
        rec.append(f"La ruta de menor costo de {_nombre(g, dj['origen'])} a {_nombre(g, dj['destino'])} "
                   f"cuesta {dj['costo']:.2f} {unidad}.")
        if bf and bf.get("camino") and bf["camino"] != dj["camino"]:
            rec.append("BFS (menos aristas) y Dijkstra (menor costo) dieron rutas distintas: la ruta con "
                       "menos paradas no siempre es la más rápida.")
    if any(str(a.get("estado", "")).upper() == "ESTIMADO" for a in g.aristas):
        rec.append("Los pesos usados son ESTIMADOS. Antes de tomar decisiones reales se deben reemplazar "
                   "por tiempos medidos en campo (cronometraje de cada tramo y de cada transbordo).")
    return rec


def generar_reporte(g, res, autor="", titulo="Reporte de análisis de la red"):
    unidad = (g.unidades() or [""])[0]
    L = [f"# {titulo}", "",
         f"- **Fecha:** {datetime.now():%d/%m/%Y %H:%M}",
         f"- **Responsable:** {autor or '(sin indicar)'}",
         f"- **Grafo:** {g.nombre} — |V| = {len(g.vertices)}, |E| = {len(g.aristas)}, "
         f"{'dirigido' if g.dirigido else 'no dirigido'}, ponderado ({unidad or 'sin unidad'})",
         f"- **Conexo:** {'sí' if es_conexo(g) else 'no'} "
         f"({len(componentes_conexos(g))} componente(s))", ""]

    if "dfs" in res:
        r = res["dfs"]
        L += ["## DFS", f"- Inicio: {r['inicio']}", f"- Orden de visita: {', '.join(r['orden'])}",
              f"- Alcanzables: {len(r['alcanzables'])} de {len(g.vertices)}",
              f"- Aristas que cierran ciclos: {len(r['aristas_ciclo'])}", ""]
    if "bfs" in res:
        r = res["bfs"]
        L += ["## BFS", f"- Inicio: {r['inicio']}", f"- Orden de visita: {', '.join(r['orden'])}"]
        for n, vs in r["niveles"].items():
            L.append(f"- Nivel {n}: {', '.join(vs)}")
        if r.get("camino"):
            L.append(f"- Camino a {r['destino']} ({r['num_aristas']} aristas): {_camino_txt(g, r['camino'])}")
        L.append("")
    if "dijkstra" in res:
        r = res["dijkstra"]
        L += ["## Dijkstra", f"- Origen: {r['origen']}"]
        if r.get("camino"):
            L += [f"- Destino: {r['destino']}", f"- Costo mínimo: {r['costo']:.2f} {unidad}",
                  f"- Camino: {_camino_txt(g, r['camino'])}"]
        L += ["", "| Nodo | Distancia | Predecesor |", "|---|---|---|"]
        for f in r["tabla"]:
            d = "∞" if f["distancia"] is None else f"{f['distancia']:.2f}"
            L.append(f"| {f['nodo']} | {d} | {f['predecesor'] or '-'} |")
        L.append("")
    for clave, nombre in (("kruskal", "Kruskal"), ("prim", "Prim")):
        if clave in res:
            r = res[clave]
            L += [f"## {nombre}", f"- Costo total: {r['costo']:.2f} {unidad}",
                  f"- Aristas del árbol ({len(r['aristas_arbol'])}): "
                  + ", ".join(f"{o}-{d} ({p:g})" for o, d, p in r["aristas_arbol"])]
            if clave == "kruskal" and r["rechazadas"]:
                L.append("- Rechazadas por ciclo: " + ", ".join(f"{o}-{d} ({p:g})" for o, d, p in r["rechazadas"]))
            L.append("")
    if "comparacion" in res:
        c = res["comparacion"]
        L += ["## Comparación Kruskal vs Prim", "", "| Criterio | Kruskal | Prim |", "|---|---|---|"]
        for f in c["filas"]:
            L.append(f"| {f['Criterio']} | {f['Kruskal']} | {f['Prim']} |")
        L += ["", f"**{c['mensaje']}**", ""]

    L += ["## Recomendaciones", ""]
    L += [f"{i}. {t}" for i, t in enumerate(recomendaciones(g, res), start=1)]
    return "\n".join(L) + "\n"
