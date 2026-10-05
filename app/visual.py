"""Dibujo del grafo con matplotlib (usa las coordenadas x,y de los vértices si existen).

Estilo: mapa nocturno estilo Teleférico, con líneas de colores brillantes sobre fondo oscuro.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORES_LINEA = {
    "Roja": "#ff4d4f", "Amarilla": "#ffc933", "Verde": "#3ddc84", "Azul": "#4d7cff",
    "Naranja": "#ff9a3c", "Blanca": "#f1f3f8", "Celeste": "#35c8ff", "Morada": "#b46bff",
    "Café": "#c98a4b", "Plateada": "#c5d0e0", "Peatonal": "#8ea0c0",
}
FONDO = "#0e1527"
COLOR_RESALTE = "#ffffff"       # contorno brillante de lo resaltado
COLOR_NODO = "#1b2748"
BORDE_NODO = "#8fa6e8"
COLOR_NODO_RES = "#ffd54f"
COLOR_TEXTO = "#eef2ff"


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
    fig.patch.set_facecolor(FONDO)
    ax.set_facecolor(FONDO)

    for a in g.aristas:
        o, d = a["origen"], a["destino"]
        x = [pos[o][0], pos[d][0]]
        y = [pos[o][1], pos[d][1]]
        es_res = _par(o, d, g.dirigido) in resaltar
        color = COLORES_LINEA.get(a.get("linea", ""), "#6b7a99")
        if es_res:
            ax.plot(x, y, color=color, lw=14, alpha=0.18, solid_capstyle="round", zorder=2)   # brillo
            ax.plot(x, y, color=COLOR_RESALTE, lw=7, solid_capstyle="round", zorder=3)         # contorno
            ax.plot(x, y, color=color, lw=4, solid_capstyle="round", zorder=4)
        else:
            ax.plot(x, y, color=color, lw=2.6, alpha=0.18 if hay_resalte else 0.95,
                    ls="--" if a.get("linea") == "Peatonal" else "-", solid_capstyle="round", zorder=1)
        if g.dirigido:
            ax.annotate("", xy=(x[1], y[1]), xytext=(x[0], y[0]),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.8), zorder=2)
        if mostrar_pesos:
            ax.text((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, f"{a['peso']:g}", fontsize=7,
                    ha="center", va="center", zorder=6, color=color if es_res or not hay_resalte else "#7d8bb0",
                    fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.22", fc=FONDO, ec=color, lw=0.8, alpha=0.95))

    for v, (px, py) in pos.items():
        res = v in nodos_resaltados
        tenue = nodos_resaltados and not res
        if res:   # halo
            ax.scatter([px], [py], s=620, c=COLOR_NODO_RES, alpha=0.18, zorder=5, linewidths=0)
        ax.scatter([px], [py], s=250 if res else 160,
                   c=COLOR_NODO_RES if res else COLOR_NODO,
                   edgecolors=COLOR_RESALTE if res else BORDE_NODO,
                   linewidths=2.4 if res else 1.5, zorder=7, alpha=0.45 if tenue else 1)
        txt = g.vertices[v].get("nombre", v) if etiquetas == "nombre" else v
        ax.text(px, py + 0.34, txt, fontsize=7.8, ha="center", va="bottom", zorder=8,
                color=COLOR_TEXTO if not tenue else "#7d8bb0",
                fontweight="bold" if res else "normal")

    ax.set_title(titulo, fontsize=14, fontweight="bold", color=COLOR_TEXTO, pad=14)
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")

    lineas = sorted({a.get("linea", "") for a in g.aristas if a.get("linea", "") in COLORES_LINEA})
    if lineas:
        handles = [plt.Line2D([0], [0], color=COLORES_LINEA[l], lw=4, label=l) for l in lineas]
        leg = ax.legend(handles=handles, loc="lower left", fontsize=8, ncol=2, frameon=True,
                        title="Líneas", facecolor="#141c33", edgecolor="#263154", labelcolor=COLOR_TEXTO)
        leg.get_title().set_color(COLOR_TEXTO)
    fig.tight_layout()
    return fig
