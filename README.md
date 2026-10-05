# 🚡 Sistema de Análisis y Optimización de Redes — Teleférico La Paz–El Alto

Práctica Integradora de Teoría de Grafos · Investigación Operativa II / Estructuras Discretas · UPEA · Gestión 2026

**Problemática:** rutas y conexiones del Teleférico (Mi Teleférico) entre El Alto y La Paz.
**Modelo:** vértices = estaciones (26) · aristas = tramos de cable entre estaciones consecutivas + 1 tramo peatonal (27) ·
peso = tiempo de viaje en minutos (o distancia en km) · grafo **no dirigido y ponderado**.

## Ejecutar

```bash
pip install -r requirements.txt
streamlit run app/main.py        # abre la aplicación en el navegador
pytest -v                        # corre las 19 pruebas automáticas
```

## Estructura

```
app/
  main.py               interfaz Streamlit (10 pestañas)
  grafo.py              clase Grafo: vértices, aristas, CRUD, matrices, listas, grados
  algoritmos.py         DFS, BFS, Dijkstra, Kruskal, Prim (hechos a mano, sin NetworkX)
  validaciones.py       lectura CSV/JSON y validación (vacíos, duplicados, pesos inválidos)
  reportes.py           reporte automático + recomendaciones
  visual.py             dibujo del grafo con caminos/árboles resaltados
  actualizar_pesos.py   pasa tus cronometrajes de campo a datos/aristas.csv
datos/                  vertices.csv, aristas.csv, casos_prueba/, validacion_manual/
pruebas/                test_algoritmos.py
evidencias/             hoja_cronometraje.csv (plantilla) + carpetas para fotos, entrevistas, capturas
documentacion/          plan, guía de campo, plantilla de informe, casos de prueba, guía de defensa, declaración de IA
```

## ⚠️ Estado de los datos (leer antes de entregar)

Las **26 estaciones, las 10 líneas y los transbordos son reales**. Pero los **pesos de cada tramo son ESTIMADOS**:
se tomó el tiempo y la longitud total de cada línea (publicados) y se dividió entre sus tramos. Esa columna `estado`
dice `ESTIMADO` y la app te lo advierte.

La práctica exige datos propios y verificables. **Tienes que cronometrar los tramos en un recorrido real**
(ver `documentacion/guia_trabajo_de_campo.md`), llenar `evidencias/hoja_cronometraje.csv` y ejecutar:

```bash
python -m app.actualizar_pesos evidencias/hoja_cronometraje.csv
```

Eso reemplaza los pesos por tus mediciones y marca `MEDIDO`. Mientras haya `ESTIMADO`, los resultados son una demostración, no un resultado.

## Qué está hecho y qué falta (te toca a ti)

| Hecho en el sistema | Te toca a ti (no se puede delegar) |
|---|---|
| Los 5 algoritmos con pasos detallados | Recorrido real: cronometraje, fotos, fecha/lugar/responsable |
| CRUD de vértices y aristas, CSV/JSON, validaciones | Entrevista o acta de observación documentada |
| Matrices, lista de adyacencia, grados | Resolver a mano DFS, BFS, Dijkstra, Kruskal y Prim (grafo A–F) |
| Grafo dibujado con resaltado, comparación Kruskal/Prim | Capturas de los 10 casos de prueba |
| Simulación de cierre de estación/tramo | Informe PDF, manual de usuario, video de 5–8 min |
| Reporte con recomendaciones | Repositorio Git con tus commits, declaración de IA |
| 19 pruebas automáticas | Entender el código: la defensa es individual |
