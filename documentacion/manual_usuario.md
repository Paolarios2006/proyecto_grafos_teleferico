# Manual de usuario

## Iniciar
```bash
pip install -r requirements.txt
streamlit run app/main.py
```
Se abre en el navegador con el grafo del Teleférico ya cargado.

## Barra lateral
- **Origen de los datos:** grafo del proyecto, un caso de prueba, subir CSV (vértices + aristas), subir JSON o grafo vacío. Pulsa **Cargar este grafo** para aplicarlo.
- **Grafo dirigido:** marca si las conexiones tienen sentido único (el Teleférico es no dirigido).
- **Reiniciar análisis:** borra los resultados mostrados.
- **Peso a utilizar:** tiempo (`peso`) o `distancia_km`.

## Pestañas
1. **Datos:** registrar, modificar y eliminar vértices y aristas; cambiar pesos; ver y descargar tablas (CSV/JSON). Muestra advertencias de validación.
2. **Grafo:** métricas (|V|, |E|, componentes, conexo) y dibujo de la red; opción de mostrar pesos y etiquetas.
3. **Representación:** lista de vértices y aristas, matriz de pesos, matriz de adyacencia, lista de adyacencia y grados.
4. **DFS:** elige nodo inicial → orden, árbol, alcanzables, componentes, ciclos y paso a paso.
5. **BFS:** nodo inicial y destino → niveles, cola paso a paso, camino con menos aristas.
6. **Dijkstra:** origen y destino → costo mínimo, camino, tabla de distancias/predecesores. Con pesos negativos avisa que no es aplicable. Incluye **escenario de cierre** de estaciones o tramos.
7. **Kruskal:** árbol de expansión mínima con aristas aceptadas y rechazadas. Exige grafo no dirigido y conexo.
8. **Prim:** igual, con nodo inicial elegible.
9. **Comparación:** corre ambos y muestra la tabla comparativa con tiempos y el veredicto sobre los costos.
10. **Reporte:** genera un reporte con resultados y recomendaciones y permite descargarlo (.md).

## Formato de archivos
`vertices.csv`: `id,nombre,descripcion` (opcionales `x,y` para posicionar el dibujo).
`aristas.csv`: `origen,destino,peso,unidad` (opcionales `linea`, `distancia_km`, `estado`, `fuente`).
JSON: `{"dirigido": false, "vertices": [{...}], "aristas": [{...}]}`.

## Errores comunes
- *«arista duplicada»*: ya existe una conexión entre esos vértices (en no dirigido A-B y B-A son la misma).
- *«NO es conexo»*: Kruskal y Prim necesitan una sola componente; revisa nodos aislados.
- *«Dijkstra no es aplicable»*: hay pesos negativos.
