import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import pandas as pd
import streamlit as st

from app.algoritmos import (PesoNegativoError, bfs, comparar_kruskal_prim, componentes_conexos,
                            dfs, dijkstra, dijkstra_con_cierre, es_conexo, kruskal, medir_tiempo, prim)
from app.grafo import Grafo
from app.reportes import generar_reporte, recomendaciones
from app.validaciones import construir_grafo, leer_csv, leer_json
from app.visual import dibujar

DATOS = RAIZ / "datos"

st.set_page_config(page_title="Análisis de Red — Teleférico", page_icon="🚡", layout="wide")
# ==========================================================
# TEMA VISUAL - TELEFÉRICO
# ==========================================================
st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 3px solid #009FE3;
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #FFFFFF !important;
    }

    /* Texto */
    p, label, span {
        color: #E2E8F0;
    }

    /* Botones */
    .stButton > button {
        background-color: #009FE3;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #0077B6;
        color: white;
    }

    /* Pestañas */
    button[data-baseweb="tab"] {
        color: #CBD5E1;
        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FACC15;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
    }

    /* Cajas de información */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

</style>
""")

# ----------------------------------------------------------------- estado
for clave, valor in (("g", None), ("res", {}), ("adv", []), ("err", []), ("flash", [])):
    if clave not in st.session_state:
        st.session_state[clave] = valor


def cargar(vdf, adf, dirigido, nombre):
    g, err, adv = construir_grafo(vdf, adf, dirigido, nombre)
    st.session_state.err, st.session_state.adv = err, adv
    if g is not None:
        st.session_state.g = g
        st.session_state.res = {}
        return True
    return False


def avisar(tipo, msg):
    st.session_state.flash.append((tipo, msg))
    st.session_state.res = {}      # los resultados anteriores ya no son válidos
    st.rerun()


# ---------------------------------------------------------------- barra lateral
st.sidebar.title("🚡 Análisis de Red")
st.sidebar.caption("Teoría de Grafos · DFS · BFS · Dijkstra · Kruskal · Prim")
fuente = st.sidebar.radio("Origen de los datos",
                          ["Teleférico (datos del proyecto)", "Caso de prueba", "Subir CSV", "Subir JSON", "Grafo vacío"])
dirigido = st.sidebar.checkbox("Grafo dirigido", value=False,
                               help="El Teleférico es no dirigido (se viaja en ambos sentidos).")
vdf_n = adf_n = None
nombre_n = "Grafo"
if fuente.startswith("Teleférico"):
    vdf_n, adf_n, nombre_n = leer_csv(DATOS / "vertices.csv"), leer_csv(DATOS / "aristas.csv"), "Teleférico La Paz–El Alto"
elif fuente == "Caso de prueba":
    casos = sorted(p.name.replace("_vertices.csv", "") for p in (DATOS / "casos_prueba").glob("*_vertices.csv"))
    caso = st.sidebar.selectbox("Caso", casos) if casos else None
    if caso:
        vdf_n = leer_csv(DATOS / "casos_prueba" / f"{caso}_vertices.csv")
        adf_n = leer_csv(DATOS / "casos_prueba" / f"{caso}_aristas.csv")
        nombre_n = caso
elif fuente == "Subir CSV":
    fv = st.sidebar.file_uploader("vertices.csv (id,nombre,descripcion)", type="csv")
    fa = st.sidebar.file_uploader("aristas.csv (origen,destino,peso,unidad)", type="csv")
    if fv and fa:
        vdf_n, adf_n, nombre_n = leer_csv(fv), leer_csv(fa), "Grafo CSV"
elif fuente == "Subir JSON":
    fj = st.sidebar.file_uploader("grafo.json", type="json")
    if fj:
        vdf_n, adf_n, d_json = leer_json(fj)
        nombre_n = "Grafo JSON"
        if d_json is not None:
            dirigido = bool(d_json)
else:
    vdf_n = pd.DataFrame(columns=["id", "nombre", "descripcion"])
    adf_n = pd.DataFrame(columns=["origen", "destino", "peso", "unidad"])
    nombre_n = "Grafo nuevo"

if st.sidebar.button("📂 Cargar este grafo", key="btn_cargar", disabled=vdf_n is None):
    if cargar(vdf_n, adf_n, dirigido, nombre_n):
        st.sidebar.success("Grafo cargado.")
if st.sidebar.button("🔄 Reiniciar análisis", key="btn_reset"):
    st.session_state.res = {}
    st.sidebar.info("Resultados borrados.")

if st.session_state.g is None:            # primera ejecución: cargar el grafo del proyecto
    cargar(leer_csv(DATOS / "vertices.csv"), leer_csv(DATOS / "aristas.csv"), False, "Teleférico La Paz–El Alto")

if st.session_state.err:
    st.sidebar.error("No se pudo cargar el grafo:")
    for e in st.session_state.err:
        st.sidebar.write("• " + e)

g = st.session_state.g
res = st.session_state.res
extras = g.columnas_numericas_extra()
opciones_peso = ["peso"] + extras
col_peso = st.sidebar.selectbox(
    "Peso a utilizar", opciones_peso,
    format_func=lambda c: f"peso ({', '.join(g.unidades()) or 'sin unidad'})" if c == "peso" else c)
ga = g if col_peso == "peso" else g.con_peso(col_peso, "km" if "km" in col_peso else "")
unidad = (ga.unidades() or [""])[0]
ids = sorted(ga.vertices)


def fmt(v):
    return f"{v} · {ga.vertices[v].get('nombre', v)}"


def nom(v):
    return ga.vertices[v].get("nombre", v)


def camino_txt(camino):
    return " → ".join(nom(v) for v in camino)


def hay_datos(minimo=1):
    if len(ids) < minimo:
        st.info("Primero registra o carga vértices y aristas en la pestaña «Datos».")
        return False
    return True


# ------------------------------------------------------------------- encabezado
st.title("Sistema de Análisis y Optimización de Redes")
st.caption(f"Grafo actual: **{g.nombre}** · |V| = {len(g.vertices)} · |E| = {len(g.aristas)} · "
           f"{'dirigido' if g.dirigido else 'no dirigido'} · ponderado ({unidad or 'sin unidad'})")
for tipo, msg in st.session_state.flash:
    getattr(st, tipo)(msg)
st.session_state.flash = []

tabs = st.tabs(["1 · Datos", "2 · Grafo", "3 · Representación", "4 · DFS", "5 · BFS", "6 · Dijkstra",
                "7 · Kruskal", "8 · Prim", "9 · Comparación", "10 · Reporte"])

# =============================================================== 1 · DATOS
with tabs[0]:
    if st.session_state.adv:
        with st.expander(f"⚠️ {len(st.session_state.adv)} advertencia(s) de validación", expanded=False):
            for a in st.session_state.adv:
                st.write("• " + a)
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Vértices")
        with st.expander("➕ Registrar vértice"):
            with st.form("f_add_v", clear_on_submit=True):
                nid = st.text_input("Código (ej. V27)")
                nnom = st.text_input("Nombre")
                ndes = st.text_input("Descripción")
                if st.form_submit_button("Registrar"):
                    try:
                        g.agregar_vertice(nid, nnom, ndes)
                        avisar("success", f"Vértice {nid} registrado.")
                    except ValueError as e:
                        st.error(str(e))
        with st.expander("✏️ Modificar vértice"):
            if ids:
                with st.form("f_mod_v"):
                    mid = st.selectbox("Vértice", ids, format_func=fmt)
                    mnom = st.text_input("Nuevo nombre (vacío = no cambiar)")
                    mdes = st.text_input("Nueva descripción (vacío = no cambiar)")
                    if st.form_submit_button("Modificar"):
                        campos = {k: v for k, v in (("nombre", mnom), ("descripcion", mdes)) if v.strip()}
                        try:
                            g.modificar_vertice(mid, **campos)
                            avisar("success", f"Vértice {mid} modificado.")
                        except ValueError as e:
                            st.error(str(e))
        with st.expander("🗑️ Eliminar vértice"):
            if ids:
                with st.form("f_del_v"):
                    did = st.selectbox("Vértice a eliminar", ids, format_func=fmt)
                    if st.form_submit_button("Eliminar"):
                        try:
                            n = g.eliminar_vertice(did)
                            avisar("warning", f"Vértice {did} eliminado junto con {n} arista(s).")
                        except ValueError as e:
                            st.error(str(e))

    with c2:
        st.subheader("Aristas")
        claves_ar = [f"{a['origen']} - {a['destino']}" for a in g.aristas]
        with st.expander("➕ Registrar arista"):
            if len(ids) >= 2:
                with st.form("f_add_a", clear_on_submit=True):
                    ao = st.selectbox("Origen", ids, format_func=fmt)
                    ad = st.selectbox("Destino", ids, index=1, format_func=fmt)
                    ap = st.number_input("Peso", value=1.0, step=0.1, format="%.2f")
                    au = st.text_input("Unidad", value=(g.unidades() or ["minutos"])[0])
                    al = st.text_input("Línea / etiqueta (opcional)")
                    if st.form_submit_button("Registrar"):
                        extra = {"linea": al} if al.strip() else {}
                        try:
                            g.agregar_arista(ao, ad, ap, au, **extra)
                            avisar("success", f"Arista {ao} - {ad} registrada.")
                        except ValueError as e:
                            st.error(str(e))
            else:
                st.caption("Necesitas al menos 2 vértices.")
        with st.expander("✏️ Modificar arista / peso"):
            if claves_ar:
                with st.form("f_mod_a"):
                    sel = st.selectbox("Arista", claves_ar)
                    np_ = st.number_input("Nuevo peso", value=1.0, step=0.1, format="%.2f")
                    est = st.selectbox("Estado del dato", ["(sin cambio)", "MEDIDO", "ESTIMADO"])
                    if st.form_submit_button("Modificar"):
                        o, d = sel.split(" - ")
                        campos = {"peso": np_}
                        if est != "(sin cambio)":
                            campos["estado"] = est
                        try:
                            g.modificar_arista(o, d, **campos)
                            avisar("success", f"Arista {sel}: nuevo peso {np_:g}.")
                        except ValueError as e:
                            st.error(str(e))
        with st.expander("🗑️ Eliminar arista"):
            if claves_ar:
                with st.form("f_del_a"):
                    sel = st.selectbox("Arista a eliminar", claves_ar)
                    if st.form_submit_button("Eliminar"):
                        o, d = sel.split(" - ")
                        try:
                            g.eliminar_arista(o, d)
                            avisar("warning", f"Arista {sel} eliminada.")
                        except ValueError as e:
                            st.error(str(e))

    vdf, adf = g.a_dataframes()
    st.markdown("**Tabla de vértices**")
    st.dataframe(vdf)
    st.markdown("**Tabla de aristas**")
    st.dataframe(adf)
    d1, d2, d3 = st.columns(3)
    d1.download_button("⬇️ vertices.csv", vdf.to_csv(index=False).encode("utf-8"), "vertices.csv", "text/csv")
    d2.download_button("⬇️ aristas.csv", adf.to_csv(index=False).encode("utf-8"), "aristas.csv", "text/csv")
    d3.download_button("⬇️ grafo.json", g.a_json().encode("utf-8"), "grafo.json", "application/json")

# =============================================================== 2 · GRAFO
with tabs[1]:
    if hay_datos():
        comps = componentes_conexos(ga)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Vértices |V|", len(ga.vertices))
        m2.metric("Aristas |E|", len(ga.aristas))
        m3.metric("Componentes conexos", len(comps))
        m4.metric("¿Conexo?", "Sí" if es_conexo(ga) else "No")
        if len(ga.vertices) < 10 or len(ga.aristas) < 15:
            st.warning("La práctica pide |V| ≥ 10 y |E| ≥ 15 para el grafo real (salvo justificación).")
        o1, o2 = st.columns(2)
        pesos_on = o1.checkbox("Mostrar pesos", value=True)
        etiq = o2.radio("Etiquetas", ["nombre", "código"], horizontal=True)
        st.pyplot(dibujar(ga, titulo=ga.nombre, mostrar_pesos=pesos_on,
                          etiquetas="nombre" if etiq == "nombre" else "codigo"))

# ========================================================= 3 · REPRESENTACIÓN
with tabs[2]:
    if hay_datos():
        vdf, adf = ga.a_dataframes()
        st.markdown("**Lista de vértices**")
        st.dataframe(vdf[[c for c in ("id", "nombre", "descripcion") if c in vdf.columns]])
        st.markdown("**Lista de aristas**")
        st.dataframe(adf)
        ids_m, mat = ga.matriz_pesos()
        dfm = pd.DataFrame([["–" if x is None else f"{x:g}" for x in fila] for fila in mat],
                           index=ids_m, columns=ids_m)
        st.markdown(f"**Matriz de pesos** ({unidad or 'sin unidad'}; «–» = no hay arista)")
        st.dataframe(dfm)
        ids_a, mad = ga.matriz_adyacencia()
        st.markdown("**Matriz de adyacencia**")
        st.dataframe(pd.DataFrame(mad, index=ids_a, columns=ids_a))
        st.markdown("**Lista de adyacencia** (generada por el sistema)")
        lineas = [f"{v}: " + (", ".join(f"{w}({p:g})" for w, p in vec) or "—")
                  for v, vec in ga.lista_adyacencia().items()]
        st.code("\n".join(lineas))
        st.markdown("**Grado de cada vértice**" + (" (entrada, salida)" if ga.dirigido else ""))
        gr = ga.grados()
        st.dataframe(pd.DataFrame({"vértice": [fmt(v) for v in gr],
                                   "grado": [str(x) if ga.dirigido else x for x in gr.values()]}))

# =================================================================== 4 · DFS
with tabs[3]:
    if hay_datos():
        st.caption("Utilidad en esta red: saber qué estaciones se pueden alcanzar desde un punto, "
                   "detectar si la red está partida en partes desconectadas y encontrar ciclos "
                   "(rutas alternativas).")
        ini = st.selectbox("Nodo inicial", ids, format_func=fmt, key="dfs_ini")
        if st.button("▶️ Ejecutar DFS", key="btn_dfs"):
            try:
                res["dfs"] = dfs(ga, ini)
            except ValueError as e:
                st.error(str(e))
        r = res.get("dfs")
        if r:
            st.success("Orden de visita: " + " → ".join(r["orden"]))
            st.write("**Recorrido con nombres:** " + camino_txt(r["orden"]))
            st.write(f"**Alcanzables:** {len(r['alcanzables'])} de {len(ids)}"
                     + (f" · **No alcanzables:** {', '.join(r['no_alcanzables'])}" if r["no_alcanzables"] else ""))
            comps = componentes_conexos(ga)
            st.write(f"**Componentes conexos:** {len(comps)}")
            for i, c in enumerate(comps, start=1):
                st.write(f"  Componente {i}: {', '.join(c)}")
            a1, a2 = st.columns(2)
            a1.markdown("**Aristas usadas (árbol DFS)**")
            a1.dataframe(pd.DataFrame(r["aristas_arbol"], columns=["desde", "hasta", "peso"]))
            a2.markdown("**Aristas que cierran ciclo / camino alternativo**")
            a2.dataframe(pd.DataFrame(r["aristas_ciclo"], columns=["desde", "hasta", "peso"]))
            with st.expander("Ver paso a paso"):
                st.code("\n".join(r["pasos"]))
            st.pyplot(dibujar(ga, aristas_resaltadas=r["aristas_arbol"], nodos_resaltados=r["alcanzables"],
                              titulo=f"DFS desde {nom(r['inicio'])}"))

# =================================================================== 5 · BFS
with tabs[4]:
    if hay_datos():
        st.caption("BFS encuentra el camino con MENOS ARISTAS (menos paradas). Es camino mínimo en costo "
                   "solo si todas las conexiones cuestan lo mismo.")
        b1, b2 = st.columns(2)
        ini = b1.selectbox("Nodo inicial", ids, format_func=fmt, key="bfs_ini")
        dst = b2.selectbox("Nodo destino", ids, index=len(ids) - 1, format_func=fmt, key="bfs_dst")
        if st.button("▶️ Ejecutar BFS", key="btn_bfs"):
            try:
                res["bfs"] = bfs(ga, ini, dst)
            except ValueError as e:
                st.error(str(e))
        r = res.get("bfs")
        if r:
            st.success("Orden de visita: " + " → ".join(r["orden"]))
            st.markdown("**Recorrido por niveles**")
            st.dataframe(pd.DataFrame({"nivel": list(r["niveles"]),
                                       "nodos": [", ".join(v) for v in r["niveles"].values()]}))
            if r.get("camino"):
                st.info(f"Camino mínimo en aristas: **{r['num_aristas']}** → " + camino_txt(r["camino"]))
            else:
                st.warning(f"No existe camino de {r['inicio']} a {r['destino']}.")
            st.markdown("**Estructura de la cola (paso a paso)**")
            st.dataframe(pd.DataFrame([{"paso": p["paso"], "extraído": p["extraido"],
                                        "encolados": ", ".join(p["encolados"]),
                                        "cola": ", ".join(p["cola"]),
                                        "visitados": ", ".join(p["visitados"])} for p in r["pasos"]]))
            st.pyplot(dibujar(ga, camino=r.get("camino"), nodos_resaltados=r["alcanzables"] if not r.get("camino") else (),
                              titulo=f"BFS: {nom(r['inicio'])} → {nom(r['destino'])}"))

# ============================================================== 6 · DIJKSTRA
with tabs[5]:
    if hay_datos():
        if ga.tiene_pesos_negativos():
            st.warning("⚠️ Hay pesos negativos: Dijkstra NO es aplicable (puede dar resultados incorrectos).")
        d1, d2 = st.columns(2)
        ori = d1.selectbox("Origen", ids, format_func=fmt, key="dij_ori")
        dst = d2.selectbox("Destino", ids, index=len(ids) - 1, format_func=fmt, key="dij_dst")
        if st.button("▶️ Ejecutar Dijkstra", key="btn_dij"):
            try:
                res["dijkstra"] = dijkstra(ga, ori, dst)
            except PesoNegativoError as e:
                res.pop("dijkstra", None)
                st.error(str(e))
            except ValueError as e:
                st.error(str(e))
        r = res.get("dijkstra")
        if r:
            if r.get("camino"):
                st.success(f"Costo mínimo: **{r['costo']:.2f} {unidad}**")
                st.write("**Camino:** " + " → ".join(r["camino"]))
                st.write(camino_txt(r["camino"]))
            else:
                st.warning(f"No hay camino de {r['origen']} a {r['destino']}.")
            st.markdown("**Tabla de distancias y predecesores**")
            st.dataframe(pd.DataFrame([{"nodo": fmt(f["nodo"]),
                                        "distancia": "∞" if f["distancia"] is None else round(f["distancia"], 2),
                                        "predecesor": f["predecesor"] or "—"} for f in r["tabla"]]))
            with st.expander("Ver paso a paso (nodo fijado y relajaciones)"):
                st.dataframe(pd.DataFrame([{"paso": p["paso"], "nodo fijado": p["nodo_fijado"],
                                            "distancia": round(p["distancia"], 2),
                                            "relajaciones": ", ".join(p["relajaciones"]) or "—"}
                                           for p in r["pasos"]]))
            st.pyplot(dibujar(ga, camino=r.get("camino"),
                              titulo=f"Dijkstra: {nom(r['origen'])} → {nom(r['destino'])}"
                                     + (f" ({r['costo']:.2f} {unidad})" if r.get("camino") else "")))
        with st.expander("🚧 Escenario: cierre de estaciones o tramos (rutas alternativas)"):
            cv = st.multiselect("Estaciones cerradas", ids, format_func=fmt, key="cierre_v")
            ca = st.multiselect("Tramos cerrados", [f"{a['origen']} - {a['destino']}" for a in ga.aristas],
                                key="cierre_a")
            if st.button("Simular cierre", key="btn_cierre"):
                try:
                    out = dijkstra_con_cierre(ga, ori, dst, cv, [tuple(x.split(" - ")) for x in ca])
                    o, c = out["original"], out["con_cierre"]
                    st.write(f"**Ruta original:** {camino_txt(o['camino']) if o.get('camino') else 'sin camino'}"
                             + (f" — {o['costo']:.2f} {unidad}" if o.get("camino") else ""))
                    if c is None or not c.get("camino"):
                        st.error("Con ese cierre NO existe ruta entre el origen y el destino.")
                    else:
                        st.write(f"**Ruta con cierre:** {camino_txt(c['camino'])} — {c['costo']:.2f} {unidad}")
                        if o.get("camino"):
                            dif = c["costo"] - o["costo"]
                            st.info(f"Diferencia: {dif:+.2f} {unidad}")
                except (PesoNegativoError, ValueError) as e:
                    st.error(str(e))

# ============================================================== 7 · KRUSKAL
with tabs[6]:
    if hay_datos():
        if st.button("▶️ Ejecutar Kruskal", key="btn_kr"):
            try:
                res["kruskal"] = kruskal(ga)
            except ValueError as e:
                res.pop("kruskal", None)
                st.error(str(e))
        r = res.get("kruskal")
        if r:
            st.success(f"Costo total del árbol de expansión mínima: **{r['costo']:.2f} {unidad}** "
                       f"({len(r['aristas_arbol'])} aristas)")
            k1, k2 = st.columns(2)
            k1.markdown("**Aristas ordenadas de menor a mayor peso**")
            k1.dataframe(pd.DataFrame(r["aristas_ordenadas"], columns=["desde", "hasta", "peso"]))
            k2.markdown("**Decisión por arista**")
            k2.dataframe(pd.DataFrame(r["pasos"]))
            st.write("**Aceptadas:** " + (", ".join(f"{o}-{d}" for o, d, _ in r["aceptadas"]) or "—"))
            st.write("**Rechazadas por formar ciclo:** " + (", ".join(f"{o}-{d}" for o, d, _ in r["rechazadas"]) or "—"))
            st.pyplot(dibujar(ga, aristas_resaltadas=r["aristas_arbol"],
                              titulo=f"Kruskal — costo {r['costo']:.2f} {unidad}"))

# ================================================================== 8 · PRIM
with tabs[7]:
    if hay_datos():
        ini = st.selectbox("Nodo inicial", ids, format_func=fmt, key="prim_ini")
        if st.button("▶️ Ejecutar Prim", key="btn_pr"):
            try:
                res["prim"] = prim(ga, ini)
            except ValueError as e:
                res.pop("prim", None)
                st.error(str(e))
        r = res.get("prim")
        if r:
            st.success(f"Nodo inicial: {r['inicio']} · Costo total: **{r['costo']:.2f} {unidad}**")
            st.markdown("**Arista elegida en cada iteración**")
            st.dataframe(pd.DataFrame([{"iteración": p["iteracion"], "arista": p["arista"], "peso": p["peso"],
                                        "nodos incorporados": ", ".join(p["incorporados"])} for p in r["pasos"]]))
            st.pyplot(dibujar(ga, aristas_resaltadas=r["aristas_arbol"],
                              titulo=f"Prim desde {nom(r['inicio'])} — costo {r['costo']:.2f} {unidad}"))

# ========================================================== 9 · COMPARACIÓN
with tabs[8]:
    if hay_datos():
        ini = st.selectbox("Nodo inicial de Prim", ids, format_func=fmt, key="cmp_ini")
        if st.button("⚖️ Comparar Kruskal y Prim", key="btn_cmp"):
            try:
                kr, pr = kruskal(ga), prim(ga, ini)
                tk, tp = medir_tiempo(kruskal, ga), medir_tiempo(prim, ga, ini)
                res.update({"kruskal": kr, "prim": pr, "comparacion": comparar_kruskal_prim(kr, pr, tk, tp)})
            except ValueError as e:
                res.pop("comparacion", None)
                st.error(str(e))
        c = res.get("comparacion")
        if c:
            (st.success if c["mismo_costo"] else st.error)(c["mensaje"])
            tabla = pd.DataFrame(c["filas"]).astype(str)
            tabla.loc[len(tabla)] = ["Ventajas observadas", "Ordena aristas; simple con datos como lista de aristas",
                                     "Crece desde un nodo; eficiente con matriz/lista de adyacencia"]
            tabla.loc[len(tabla)] = ["Limitaciones observadas", "Necesita ordenar todas las aristas y Union-Find",
                                     "Depende del nodo inicial para el orden (no para el costo)"]
            st.dataframe(tabla)
            p1, p2 = st.columns(2)
            p1.pyplot(dibujar(ga, aristas_resaltadas=res["kruskal"]["aristas_arbol"], titulo="Kruskal", tam=(8, 5)))
            p2.pyplot(dibujar(ga, aristas_resaltadas=res["prim"]["aristas_arbol"], titulo="Prim", tam=(8, 5)))

# ============================================================== 10 · REPORTE
with tabs[9]:
    if hay_datos():
        autor = st.text_input("Responsable del análisis")
        st.caption("Ejecuta antes los algoritmos que quieras incluir; el reporte usa lo que haya en pantalla.")
        if st.button("📝 Generar reporte", key="btn_rep"):
            st.session_state["reporte"] = generar_reporte(ga, res, autor)
        if st.session_state.get("reporte"):
            st.download_button("⬇️ Descargar reporte (.md)", st.session_state["reporte"].encode("utf-8"),
                               "reporte_red.md", "text/markdown")
            st.markdown(st.session_state["reporte"])
