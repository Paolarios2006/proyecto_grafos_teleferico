import math
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app.actualizar_pesos import actualizar
from app.algoritmos import (PesoNegativoError, bfs, comparar_kruskal_prim, componentes_conexos, dfs,
                            dijkstra, dijkstra_con_cierre, es_conexo, estaciones_criticas, kruskal, prim)
from app.grafo import Grafo
from app.validaciones import cargar_csv, construir_grafo, leer_csv

DATOS = RAIZ / "datos"


def caso(nombre):
    p = DATOS / "casos_prueba"
    return cargar_csv(p / f"{nombre}_vertices.csv", p / f"{nombre}_aristas.csv", nombre=nombre)


@pytest.fixture(scope="module")
def real():
    g, err, _ = cargar_csv(DATOS / "vertices.csv", DATOS / "aristas.csv", nombre="Teleférico")
    assert err == []
    return g


@pytest.fixture(scope="module")
def manual():
    g, err, _ = cargar_csv(DATOS / "validacion_manual" / "vertices.csv",
                           DATOS / "validacion_manual" / "aristas.csv", nombre="Manual A-F")
    assert err == []
    return g


# ---------------------------------------------------------------- caso 1: grafo real
def test_caso01_grafo_real_cumple_requisitos(real):
    assert len(real.vertices) >= 10 and len(real.aristas) >= 15
    assert not real.dirigido and es_conexo(real) and not real.tiene_pesos_negativos()


def test_caso01_los_cinco_algoritmos_corren_en_el_grafo_real(real):
    assert len(dfs(real, "V06")["alcanzables"]) == len(real.vertices)
    assert bfs(real, "V06", "V14")["camino"][0] == "V06"
    assert dijkstra(real, "V06", "V14")["costo"] > 0
    assert len(kruskal(real)["aristas_arbol"]) == len(real.vertices) - 1
    assert len(prim(real, "V01")["aristas_arbol"]) == len(real.vertices) - 1


# ---------------------------------------------------------------- caso 2: conexo, pesos distintos
def test_caso02_conexo_pesos_distintos():
    g, err, _ = caso("caso02_conexo_pesos_distintos")
    assert err == [] and es_conexo(g)
    k, p = kruskal(g), prim(g, "V01")
    assert math.isclose(k["costo"], p["costo"])
    assert len(k["aristas_arbol"]) == 6


# ---------------------------------------------------------------- caso 3: nodo aislado
def test_caso03_nodo_aislado():
    g, err, adv = caso("caso03_nodo_aislado")
    assert err == [] and any("aislado" in a for a in adv)
    assert not es_conexo(g)
    assert "V06" in dfs(g, "V01")["no_alcanzables"]
    assert ["V06"] in componentes_conexos(g)
    with pytest.raises(ValueError, match="NO es conexo"):
        kruskal(g)
    assert dijkstra(g, "V01", "V06")["camino"] is None      # destino inalcanzable


# ---------------------------------------------------------------- caso 4: no conexo
def test_caso04_no_conexo():
    g, err, _ = caso("caso04_no_conexo")
    assert err == [] and len(componentes_conexos(g)) == 2
    with pytest.raises(ValueError):
        prim(g, "V01")
    assert set(bfs(g, "V01")["no_alcanzables"]) == {"V04", "V05", "V06"}


# ---------------------------------------------------------------- caso 5: varios caminos
def test_caso05_bfs_y_dijkstra_pueden_diferir():
    g, _, _ = caso("caso05_varios_caminos")
    b, d = bfs(g, "V01", "V06"), dijkstra(g, "V01", "V06")
    assert b["camino"] == ["V01", "V02", "V06"] and b["num_aristas"] == 2      # menos aristas
    assert d["camino"] == ["V01", "V03", "V04", "V05", "V06"] and d["costo"] == 8  # menor costo (11 por BFS)


# ---------------------------------------------------------------- caso 6: pesos repetidos
def test_caso06_pesos_repetidos_mismo_costo():
    g, _, _ = caso("caso06_pesos_repetidos")
    k = kruskal(g)
    assert k["costo"] == 25 and len(k["aristas_arbol"]) == 5
    for inicio in sorted(g.vertices):                 # Prim da el mismo costo desde cualquier nodo
        assert prim(g, inicio)["costo"] == 25


# ---------------------------------------------------------------- caso 7: arista duplicada
def test_caso07_arista_duplicada_en_archivo():
    g, err, _ = caso("caso07_arista_duplicada")
    assert g is None and any("duplicada" in e for e in err)


def test_caso07_arista_duplicada_al_registrar():
    g = Grafo()
    g.agregar_vertice("A"); g.agregar_vertice("B")
    g.agregar_arista("A", "B", 3, "min")
    with pytest.raises(ValueError, match="duplicada"):
        g.agregar_arista("A", "B", 5, "min")
    with pytest.raises(ValueError, match="duplicada"):
        g.agregar_arista("B", "A", 5, "min")          # en no dirigido A-B y B-A son la misma
    gd = Grafo(dirigido=True)
    gd.agregar_vertice("A"); gd.agregar_vertice("B")
    gd.agregar_arista("A", "B", 3); gd.agregar_arista("B", "A", 4)   # en dirigido sí son distintas


# ---------------------------------------------------------------- caso 8: peso negativo
def test_caso08_dijkstra_rechaza_pesos_negativos():
    g, err, adv = caso("caso08_peso_negativo")
    assert err == [] and any("negativo" in a for a in adv)
    with pytest.raises(PesoNegativoError, match="no es aplicable"):
        dijkstra(g, "V01", "V05")


# ---------------------------------------------------------------- caso 9: Kruskal vs Prim
def test_caso09_kruskal_igual_prim_en_real_y_manual(real, manual):
    for g in (real, manual):
        k = kruskal(g)
        for inicio in sorted(g.vertices):
            assert math.isclose(k["costo"], prim(g, inicio)["costo"])
    c = comparar_kruskal_prim(kruskal(manual), prim(manual, "V01"))
    assert c["mismo_costo"] and c["mismo_arbol"]


# ---------------------------------------------------------------- caso 10: modificar una arista
def test_caso10_modificar_arista_cambia_la_solucion():
    g, _, _ = caso("caso05_varios_caminos")
    assert dijkstra(g, "V01", "V06")["costo"] == 8
    g.modificar_arista("V02", "V06", peso=1)          # el atajo pasa a costar 1
    d = dijkstra(g, "V01", "V06")
    assert d["camino"] == ["V01", "V02", "V06"] and d["costo"] == 2


def test_cierre_de_estacion_cambia_o_corta_la_ruta(real):
    out = dijkstra_con_cierre(real, "V06", "V14", cerrar_vertices=["V11"])   # cerrar Libertador
    assert out["con_cierre"]["camino"] is None                                # Verde queda aislada


# ---------------------------------------------------------------- validación manual (grafo A-F)
def test_validacion_manual_resultados_esperados(manual):
    d = dijkstra(manual, "V01", "V06")
    assert d["camino"] == ["V01", "V03", "V02", "V04", "V05", "V06"] and d["costo"] == 13
    k = kruskal(manual)
    assert k["costo"] == 13
    assert {frozenset((o, x)) for o, x, _ in k["aristas_arbol"]} == {
        frozenset(p) for p in [("V02", "V03"), ("V01", "V03"), ("V04", "V05"), ("V05", "V06"), ("V02", "V04")]}
    assert [r[:2] for r in k["rechazadas"]] == [("V01", "V02"), ("V04", "V06"), ("V03", "V04"), ("V03", "V05")]
    assert dfs(manual, "V04")["orden"] == ["V04", "V02", "V01", "V03", "V05", "V06"]
    b = bfs(manual, "V04")
    assert b["orden"] == ["V04", "V02", "V03", "V05", "V06", "V01"]
    assert b["niveles"] == {0: ["V04"], 1: ["V02", "V03", "V05", "V06"], 2: ["V01"]}


# ---------------------------------------------------------------- extras
def test_dfs_detecta_ciclos(manual):
    assert len(dfs(manual, "V01")["aristas_ciclo"]) == 9 - 5     # |E| - (|V|-1) aristas fuera del árbol


def test_dirigido_dijkstra_respeta_el_sentido():
    g = Grafo(dirigido=True)
    for v in "ABC":
        g.agregar_vertice(v)
    g.agregar_arista("A", "B", 1); g.agregar_arista("B", "C", 1); g.agregar_arista("C", "A", 10)
    assert dijkstra(g, "A", "C")["costo"] == 2 and dijkstra(g, "C", "B")["costo"] == 11
    with pytest.raises(ValueError, match="dirigido"):
        kruskal(g)


def test_validaciones_de_datos_incompletos_y_peso_no_numerico():
    v = leer_csv("id,nombre\nA,Uno\nB,Dos\n,Tres\n")
    a = leer_csv("origen,destino,peso\nA,B,abc\nA,Z,3\nA,B,\n")
    g, err, _ = construir_grafo(v, a)
    assert g is None
    texto = " ".join(err)
    assert "vacío" in texto and "no es numérico" in texto and "no existe" in texto


def test_estaciones_criticas_real(real):
    crit = estaciones_criticas(real)
    assert "V11" in crit and "V24" in crit and "V07" not in crit    # Libertador y Faro Murillo cortan; Río Seco no


def test_actualizar_pesos_desde_cronometraje(tmp_path):
    hoja = tmp_path / "hoja.csv"
    hoja.write_text("origen,destino,fecha,responsable,t1_seg,t2_seg,t3_seg\n"
                    "V01,V02,2026-10-10,Jhon,300,330,310\nV02,V03,,,,,\n", encoding="utf-8")
    ar = tmp_path / "aristas.csv"
    ar.write_text("origen,destino,peso,unidad,estado,fuente\nV01,V02,5.5,minutos,ESTIMADO,x\n"
                  "V02,V03,5.5,minutos,ESTIMADO,x\n", encoding="utf-8")
    assert actualizar(hoja, ar) == 1
    df = leer_csv(ar)
    assert df.loc[0, "estado"] == "MEDIDO" and df.loc[0, "peso"] == "5.22"
    assert df.loc[1, "estado"] == "ESTIMADO"                         # sin mediciones, no se toca
