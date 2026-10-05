import io
import json
import math

import pandas as pd

from .grafo import Grafo

COLS_VERTICES = ["id", "nombre"]
COLS_ARISTAS = ["origen", "destino", "peso"]


def leer_csv(fuente):
    
    if isinstance(fuente, str) and "\n" in fuente:
        fuente = io.StringIO(fuente)
    df = pd.read_csv(fuente, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    return df.apply(lambda col: col.str.strip())


def leer_json(fuente):
    
    texto = fuente if isinstance(fuente, str) else fuente.read()
    if isinstance(texto, bytes):
        texto = texto.decode("utf-8-sig")
    datos = json.loads(texto)
    vdf = pd.DataFrame(datos.get("vertices", [])).astype(str)
    adf = pd.DataFrame(datos.get("aristas", [])).astype(str)
    return vdf, adf, datos.get("dirigido")


def validar_tablas(vdf, adf, dirigido=False):
    
    err, adv = [], []

    for c in COLS_VERTICES:
        if c not in vdf.columns:
            err.append(f"Vértices: falta la columna obligatoria '{c}'.")
    for c in COLS_ARISTAS:
        if c not in adf.columns:
            err.append(f"Aristas: falta la columna obligatoria '{c}'.")
    if err:
        return err, adv

    # ---- vértices
    ids = vdf["id"].tolist()
    for i, v in enumerate(ids, start=2):
        if v == "":
            err.append(f"Vértices, fila {i}: el código está vacío (dato incompleto).")
    vistos = set()
    for v in ids:
        if v and v in vistos:
            err.append(f"Vértices: el código '{v}' está duplicado.")
        vistos.add(v)
    for i, n in enumerate(vdf["nombre"].tolist(), start=2):
        if n == "":
            adv.append(f"Vértices, fila {i}: nombre vacío (se usará el código).")
    validos = {v for v in ids if v}

    # ---- aristas
    vistas = {}
    for i, fila in enumerate(adf.to_dict("records"), start=2):
        o, d, p = fila["origen"], fila["destino"], fila["peso"]
        if o == "" or d == "" or p == "":
            err.append(f"Aristas, fila {i}: hay campos vacíos (origen, destino o peso).")
            continue
        for v in (o, d):
            if v not in validos:
                err.append(f"Aristas, fila {i}: el vértice '{v}' no existe en la lista de vértices.")
        if o == d:
            err.append(f"Aristas, fila {i}: lazo {o}-{d} no permitido.")
        try:
            pv = float(p)
            if math.isnan(pv) or math.isinf(pv):
                raise ValueError
            if pv < 0:
                adv.append(f"Aristas, fila {i}: peso negativo ({pv}) en {o}-{d}. "
                           "Dijkstra no será aplicable.")
            if pv == 0:
                adv.append(f"Aristas, fila {i}: peso 0 en {o}-{d}; revisa si es correcto.")
        except ValueError:
            err.append(f"Aristas, fila {i}: el peso '{p}' no es numérico.")
        clave = (o, d) if dirigido else tuple(sorted((o, d)))
        if clave in vistas:
            err.append(f"Aristas, fila {i}: la arista {o}-{d} está duplicada "
                       f"(ya aparece en la fila {vistas[clave]}).")
        else:
            vistas[clave] = i

    # ---- advertencias generales
    if "unidad" in adf.columns:
        unidades = {u for u in adf["unidad"].tolist() if u}
        if len(unidades) > 1:
            adv.append(f"Hay unidades mezcladas en los pesos: {sorted(unidades)}.")
    if "estado" in adf.columns and (adf["estado"].str.upper() == "ESTIMADO").any():
        n = int((adf["estado"].str.upper() == "ESTIMADO").sum())
        adv.append(f"{n} arista(s) tienen peso ESTIMADO. Reemplázalos por mediciones propias "
                   "(columna 'estado' = MEDIDO) antes de entregar.")
    conectados = set(adf["origen"]) | set(adf["destino"])
    for v in sorted(validos - conectados):
        adv.append(f"El vértice '{v}' está aislado (sin aristas).")
    return err, adv


def construir_grafo(vdf, adf, dirigido=False, nombre="Grafo"):
    """Valida y construye el Grafo. Devuelve (grafo | None, errores, advertencias)."""
    err, adv = validar_tablas(vdf, adf, dirigido)
    if err:
        return None, err, adv
    g = Grafo(dirigido=dirigido, nombre=nombre)
    extras_v = [c for c in vdf.columns if c not in ("id", "nombre", "descripcion")]
    for fila in vdf.to_dict("records"):
        extra = {c: _numero_o_texto(fila[c]) for c in extras_v if fila[c] != ""}
        g.agregar_vertice(fila["id"], fila.get("nombre", ""), fila.get("descripcion", ""), **extra)
    extras_a = [c for c in adf.columns if c not in ("origen", "destino", "peso", "unidad")]
    for fila in adf.to_dict("records"):
        extra = {c: fila[c] for c in extras_a}
        g.agregar_arista(fila["origen"], fila["destino"], fila["peso"], fila.get("unidad", ""), **extra)
    return g, err, adv


def _numero_o_texto(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return s


def cargar_csv(ruta_vertices, ruta_aristas, dirigido=False, nombre="Grafo"):
    return construir_grafo(leer_csv(ruta_vertices), leer_csv(ruta_aristas), dirigido, nombre)
