# Validación manual — grafo didáctico A–F (6 nodos, 9 aristas)

Archivos: `datos/validacion_manual/vertices.csv` y `aristas.csv`. **Resuélvelo a mano, en hoja, y fotografía el procedimiento.**
Después compáralo con lo que muestra el sistema (cárgalo en la app con «Subir CSV»).

Aristas (peso): A-B 4 · A-C 2 · B-C 1 · B-D 5 · C-D 8 · C-E 10 · D-E 2 · D-F 6 · E-F 3
Regla de desempate: si hay empate, elegir el vecino de código/letra menor.

| Ejercicio | Qué debes mostrar a mano | Resultado manual | Resultado del sistema | ¿Coinciden? |
|---|---|---|---|---|
| DFS desde D | Pila / orden de visita, aristas del árbol | | | |
| BFS desde D | Cola en cada paso, niveles | | | |
| Dijkstra A → F | Tabla de distancias y predecesores en cada iteración, camino | | | |
| Kruskal | Aristas ordenadas, aceptadas/rechazadas, costo | | | |
| Prim desde A | Arista elegida en cada iteración, costo | | | |

Si tu resultado manual y el del sistema no coinciden, no lo escondas: revisa cuál está mal y regístralo en el
registro de errores. Esa discusión suma en la defensa.
