import copy
import json
import math


class Grafo:
    def __init__(self, dirigido=False, nombre="Grafo"):
        self.dirigido = dirigido
        self.nombre = nombre
        self.vertices = {}   # id -> {"nombre", "descripcion", ...extras}
        self.aristas = []    # lista de dicts

    # ------------------------------------------------------------------ util
    def _clave(self, o, d):
        
        return (o, d) if self.dirigido else tuple(sorted((o, d)))

    def _indice_arista(self, o, d):
        k = self._clave(o, d)
        for i, a in enumerate(self.aristas):
            if self._clave(a["origen"], a["destino"]) == k:
                return i
        return None

    def existe_arista(self, o, d):
        return self._indice_arista(o, d) is not None

    def obtener_arista(self, o, d):
        i = self._indice_arista(o, d)
        return None if i is None else self.aristas[i]

    # -------------------------------------------------------------- vértices
    def agregar_vertice(self, id_, nombre="", descripcion="", **extra):
        id_ = str(id_).strip()
        if not id_:
            raise ValueError("El código del vértice no puede estar vacío.")
        if id_ in self.vertices:
            raise ValueError(f"El vértice '{id_}' ya existe (duplicado).")
        self.vertices[id_] = {"nombre": str(nombre).strip() or id_,
                              "descripcion": str(descripcion).strip(), **extra}

    def modificar_vertice(self, id_, **campos):
        if id_ not in self.vertices:
            raise ValueError(f"El vértice '{id_}' no existe.")
        self.vertices[id_].update(campos)

    def eliminar_vertice(self, id_):
        """Elimina el vértice y sus aristas incidentes. Devuelve cuántas aristas se borraron."""
        if id_ not in self.vertices:
            raise ValueError(f"El vértice '{id_}' no existe.")
        antes = len(self.aristas)
        self.aristas = [a for a in self.aristas if id_ not in (a["origen"], a["destino"])]
        del self.vertices[id_]
        return antes - len(self.aristas)

    # --------------------------------------------------------------- aristas
    def agregar_arista(self, origen, destino, peso, unidad="", **extra):
        origen, destino = str(origen).strip(), str(destino).strip()
        for v in (origen, destino):
            if v not in self.vertices:
                raise ValueError(f"El vértice '{v}' no existe; créalo antes de conectarlo.")
        if origen == destino:
            raise ValueError("No se permiten lazos (arista de un vértice a sí mismo).")
        try:
            peso = float(peso)
        except (TypeError, ValueError):
            raise ValueError(f"El peso '{peso}' no es numérico.")
        if math.isnan(peso) or math.isinf(peso):
            raise ValueError("El peso debe ser un número finito.")
        if self.existe_arista(origen, destino):
            raise ValueError(f"La arista {origen} - {destino} ya existe (duplicada).")
        # Los pesos negativos se aceptan para poder probar la advertencia de Dijkstra.
        self.aristas.append({"origen": origen, "destino": destino, "peso": peso,
                             "unidad": str(unidad).strip(), **extra})

    def modificar_arista(self, origen, destino, **campos):
        i = self._indice_arista(origen, destino)
        if i is None:
            raise ValueError(f"La arista {origen} - {destino} no existe.")
        if "peso" in campos:
            try:
                campos["peso"] = float(campos["peso"])
            except (TypeError, ValueError):
                raise ValueError("El peso debe ser numérico.")
            if math.isnan(campos["peso"]) or math.isinf(campos["peso"]):
                raise ValueError("El peso debe ser un número finito.")
        self.aristas[i].update(campos)

    def eliminar_arista(self, origen, destino):
        i = self._indice_arista(origen, destino)
        if i is None:
            raise ValueError(f"La arista {origen} - {destino} no existe.")
        del self.aristas[i]

    # --------------------------------------------------------------- consulta
    def vecinos(self, v):
        
        res = []
        for a in self.aristas:
            if a["origen"] == v:
                res.append((a["destino"], a["peso"], a))
            elif not self.dirigido and a["destino"] == v:
                res.append((a["origen"], a["peso"], a))
        return sorted(res, key=lambda t: t[0])

    def lista_adyacencia(self):
        return {v: [(w, p) for w, p, _ in self.vecinos(v)] for v in sorted(self.vertices)}

    def matriz_pesos(self):
        
        ids = sorted(self.vertices)
        pos = {v: i for i, v in enumerate(ids)}
        m = [[None] * len(ids) for _ in ids]
        for a in self.aristas:
            i, j = pos[a["origen"]], pos[a["destino"]]
            m[i][j] = a["peso"]
            if not self.dirigido:
                m[j][i] = a["peso"]
        return ids, m

    def matriz_adyacencia(self):
        ids, m = self.matriz_pesos()
        return ids, [[0 if x is None else 1 for x in fila] for fila in m]

    def grados(self):
        
        if not self.dirigido:
            return {v: len(self.vecinos(v)) for v in sorted(self.vertices)}
        ent = {v: 0 for v in self.vertices}
        sal = {v: 0 for v in self.vertices}
        for a in self.aristas:
            sal[a["origen"]] += 1
            ent[a["destino"]] += 1
        return {v: (ent[v], sal[v]) for v in sorted(self.vertices)}

    def grado_total(self, v):
        g = self.grados()[v]
        return g if not self.dirigido else sum(g)

    def tiene_pesos_negativos(self):
        return any(a["peso"] < 0 for a in self.aristas)

    def aristas_negativas(self):
        return [a for a in self.aristas if a["peso"] < 0]

    def unidades(self):
        return sorted({a.get("unidad", "") for a in self.aristas if a.get("unidad", "")})

    # --------------------------------------------------------------- copias
    def copia(self):
        return copy.deepcopy(self)

    def sin(self, vertices=(), aristas=()):
        
        g = self.copia()
        for par in aristas:
            if g.existe_arista(*par):
                g.eliminar_arista(*par)
        for v in vertices:
            if v in g.vertices:
                g.eliminar_vertice(v)
        return g

    def con_peso(self, columna, unidad=""):
        
        g = self.copia()
        for a in g.aristas:
            a["peso"] = float(a[columna])
            a["unidad"] = unidad
        return g

    def columnas_numericas_extra(self):
        
        if not self.aristas:
            return []
        extras = set().union(*[set(a) for a in self.aristas]) - {"origen", "destino", "peso", "unidad"}
        validas = []
        for c in sorted(extras):
            try:
                [float(a[c]) for a in self.aristas]
                validas.append(c)
            except (KeyError, TypeError, ValueError):
                pass
        return validas

    # ------------------------------------------------------- import / export
    def a_dataframes(self):
        import pandas as pd
        vdf = pd.DataFrame([{"id": k, **v} for k, v in sorted(self.vertices.items())])
        adf = pd.DataFrame(self.aristas)
        return vdf, adf

    def a_json(self):
        return json.dumps({"nombre": self.nombre, "dirigido": self.dirigido,
                           "vertices": [{"id": k, **v} for k, v in sorted(self.vertices.items())],
                           "aristas": self.aristas}, ensure_ascii=False, indent=2)

    def resumen(self):
        return {"vertices": len(self.vertices), "aristas": len(self.aristas),
                "tipo": "dirigido" if self.dirigido else "no dirigido",
                "ponderado": True, "unidades": self.unidades()}
