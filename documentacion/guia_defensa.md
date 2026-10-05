# Guía para la defensa individual

El docente puede pedirte, en vivo (sección 22 del enunciado): modificar un vértice o peso, cambiar origen/destino, repetir un algoritmo,
**explicar una parte del código**, **predecir el resultado antes de ejecutar**, comparar BFS con Dijkstra, explicar por qué Kruskal rechazó una arista,
cambiar el nodo inicial de Prim o corregir un error sencillo.

## Qué debes poder explicar (en orden de lectura del código)
1. `grafo.py`: cómo se guarda el grafo (diccionario de vértices + lista de aristas), por qué `vecinos()` devuelve los vecinos ordenados (resultados reproducibles), cómo se detectan aristas duplicadas en no dirigido (`_clave`).
2. `algoritmos.py → dfs`: recursión, conjunto `visitado`, por qué una arista a un nodo ya visitado que no es el padre indica un ciclo.
3. `bfs`: la cola (`deque`), el nivel de cada nodo = número mínimo de aristas.
4. `dijkstra`: la cola de prioridad (`heapq`), la relajación `d + peso < dist[w]`, por qué falla con pesos negativos (un nodo ya fijado podría mejorar después).
5. `kruskal` + `UnionFind`: ordenar aristas, `buscar`/`unir`, rechazo = ya están en el mismo conjunto = ciclo.
6. `prim`: crece desde un nodo, siempre toma la arista más barata que sale del árbol.

## Preguntas típicas (practica respondiendo en voz alta)
- ¿Por qué BFS y Dijkstra dieron rutas distintas? (BFS cuenta aristas, Dijkstra suma pesos; ver `caso05_varios_caminos`.)
- ¿Cuándo BFS sí da el camino de menor costo? (Cuando todos los pesos son iguales.)
- ¿Por qué Kruskal y Prim pueden dar árboles distintos con el mismo costo? (Empates de peso; ver `caso06_pesos_repetidos`.)
- ¿Por qué Kruskal rechazó la arista X? (Sus extremos ya estaban conectados: cerraría un ciclo.)
- ¿Qué pasa si cierro Libertador? (Pestaña Dijkstra → escenario de cierre; la línea Verde queda aislada porque Libertador es estación crítica.)
- ¿Qué cambia al modificar una arista? (Caso 10.)
- ¿Qué limitaciones tiene el modelo? (Sin tiempos de espera/transbordo, pesos promedio de pocas mediciones, sin Bs como peso.)
- Predice: «si subo el peso de este tramo a 20, ¿cambia la ruta de A a B?» Razónalo mirando el grafo antes de ejecutar.

## Truco de preparación
Ejecuta cada algoritmo sobre el grafo A–F con tu resolución manual al lado. Si puedes narrar las iteraciones sin mirar el código, estás listo.
