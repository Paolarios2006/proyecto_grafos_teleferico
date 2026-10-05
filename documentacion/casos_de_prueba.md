# Casos de prueba obligatorios

Cada caso se prueba **en la aplicación** (sidebar → «Caso de prueba» → «Cargar este grafo») y se registra:
datos de entrada, resultado esperado, resultado obtenido, estado y captura. Las columnas «obtenido», «estado» y «captura» las llenas tú
después de ejecutarlo. Las pruebas automáticas (`pytest -v`) cubren los mismos casos como respaldo.

| N.º | Caso | Datos de entrada | Resultado esperado | Obtenido | Estado | Captura |
|---|---|---|---|---|---|---|
| 1 | Grafo real investigado | «Teleférico (datos del proyecto)» con tus pesos medidos | Conexo, \|V\|=26, \|E\|=27, los 5 algoritmos corren, costo Kruskal = costo Prim | | | |
| 2 | Conexo, pesos distintos | `caso02_conexo_pesos_distintos` | Conexo. Kruskal = Prim = 21. Árbol de 6 aristas | | | |
| 3 | Nodo aislado | `caso03_nodo_aislado` | Advertencia de V06 aislado. DFS desde V01 no alcanza V06. Kruskal/Prim muestran error «NO es conexo» | | | |
| 4 | No conexo | `caso04_no_conexo` | 2 componentes: {V01,V02,V03} y {V04,V05,V06}. Kruskal/Prim rechazan por no ser conexo | | | |
| 5 | Más de un camino | `caso05_varios_caminos`, V01 → V06 | BFS: V01-V02-V06 (2 aristas). Dijkstra: V01-V03-V04-V05-V06 (costo 8) | | | |
| 6 | Pesos repetidos | `caso06_pesos_repetidos` | Kruskal = Prim = 25 desde cualquier nodo inicial; los árboles pueden diferir | | | |
| 7 | Arista duplicada | `caso07_arista_duplicada`; y registrar a mano una arista ya existente | La carga se rechaza con «arista duplicada»; el formulario también la rechaza | | | |
| 8 | Dijkstra con peso negativo | `caso08_peso_negativo`, V01 → V05 | Advertencia en pantalla y error «Dijkstra no es aplicable» | | | |
| 9 | Kruskal vs Prim, mismo grafo | Pestaña «Comparación» con el grafo real y con `validacion_manual` | Costos iguales; mensaje verde | | | |
| 10 | Modificar una arista | `caso05_varios_caminos`: poner V02-V06 en peso 1 (Datos → Modificar arista) | Dijkstra V01 → V06 pasa a V01-V02-V06 con costo 2 | | | |

## Pruebas extra recomendadas con el grafo real
- Pestaña Dijkstra → «Escenario de cierre»: cerrar Libertador y calcular UPEA → Irpavi (no debe haber ruta).
- Cerrar un tramo del ciclo (por ejemplo Faro Murillo - Mirador) y ver la ruta alternativa.
- Cambiar «Peso a utilizar» a `distancia_km` y comprobar que cambian los costos.
