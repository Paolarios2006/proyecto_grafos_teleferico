"""Dibujo del grafo con matplotlib (usa las coordenadas x,y de los vértices si existen)."""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORES_LINEA = {
    "Roja": "#d62728", "Amarilla": "#e8b800", "Verde": "#2ca02c", "Azul": "#1f4fd8",
    "Naranja": "#ff7f0e", "Blanca": "#5f6368", "Celeste": "#35b6e8", "Morada": "#8e44ad",
    "Café": "#8b5a2b", "Plateada": "#a9b8c9", "Peatonal": "#555555",
}
COLOR_RESALTE = "#111111"
COLOR_NODO = "#ffffff"


def _posiciones(g):
    pos = {}
    sin_coord = []
    for v, datos in g.vertices.items():
        try:
            pos[v] = (float(datos["x"]), float(datos["y"]))
        except (KeyError, TypeError, ValueError):
            sin_coord.append(v)
    if sin_coord:                       # distribución circular para los que no tienen x,y
        n = len(sin_coord)
        for i, v in enumerate(sorted(sin_coord)):
            pos[v] = (5 + 4 * math.cos(2 * math.pi * i / n), 5 + 4 * math.sin(2 * math.pi * i / n))
    return pos


def _par(a, b, dirigido):
    return (a, b) if dirigido else frozenset((a, b))


def dibujar(g, aristas_resaltadas=(), nodos_resaltados=(), camino=None, titulo="",
            mostrar_pesos=True, etiquetas="nombre", tam=(13, 7.5)):
    """Devuelve una figura. `aristas_resaltadas`: iterable de (u, v[, peso])."""
    pos = _posiciones(g)
    resaltar = {_par(t[0], t[1], g.dirigido) for t in aristas_resaltadas}
    if camino:
        resaltar |= {_par(u, v, g.dirigido) for u, v in zip(camino, camino[1:])}
        nodos_resaltados = set(nodos_resaltados) | set(camino)
    hay_resalte = bool(resaltar) or bool(nodos_resaltados)

    fig, ax = plt.subplots(figsize=tam)
    for a in g.aristas:
        o, d = a["origen"], a["destino"]
        x = [pos[o][0], pos[d][0]]
        y = [pos[o][1], pos[d][1]]
        es_res = _par(o, d, g.dirigido) in resaltar
        color = COLORES_LINEA.get(a.get("linea", ""), "#888888")
        if es_res:
            ax.plot(x, y, color=COLOR_RESALTE, lw=6.5, solid_capstyle="round", zorder=2)
            ax.plot(x, y, color=color, lw=3, solid_capstyle="round", zorder=3)
        else:
            ax.plot(x, y, color=color, lw=2.2, alpha=0.25 if hay_resalte else 0.9,
                    ls="--" if a.get("linea") == "Peatonal" else "-", zorder=1)
        if g.dirigido:
            ax.annotate("", xy=(x[1], y[1]), xytext=(x[0], y[0]),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5), zorder=2)
        if mostrar_pesos:
            ax.text((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, f"{a['peso']:g}", fontsize=7,
                    ha="center", va="center", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    for v, (px, py) in pos.items():
        res = v in nodos_resaltados
        ax.scatter([px], [py], s=230 if res else 150, c="#ffd54f" if res else COLOR_NODO,
                   edgecolors=COLOR_RESALTE, linewidths=2.2 if res else 1.2, zorder=5,
                   alpha=1 if (res or not nodos_resaltados) else 0.5)
        txt = g.vertices[v].get("nombre", v) if etiquetas == "nombre" else v
        ax.text(px, py + 0.32, txt, fontsize=7.5, ha="center", va="bottom", zorder=6,
                fontweight="bold" if res else "normal")
    ax.set_title(titulo, fontsize=12, fontweight="bold")
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")
    # leyenda de líneas presentes
    lineas = sorted({a.get("linea", "") for a in g.aristas if a.get("linea", "") in COLORES_LINEA})
    if lineas:
        handles = [plt.Line2D([0], [0], color=COLORES_LINEA[l], lw=3, label=l) for l in lineas]
        ax.legend(handles=handles, loc="lower left", fontsize=7, ncol=2, frameon=True, title="Línea")
    fig.tight_layout()
    return fig
