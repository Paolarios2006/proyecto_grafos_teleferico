# INFORME — Práctica Integradora de Teoría de Grafos

> Plantilla con los 22 puntos que pide la práctica. Lo marcado **[COMPLETAR]** depende de tus datos y evidencias reales.
> Pásalo a Word/PDF cuando esté lleno.

## 1. Portada
UPEA · Carrera de Ingeniería de Sistemas · Investigación Operativa II / Estructuras Discretas · Docente: M.Sc. Ing. Juan Carlos Catunta Choquecalle · Gestión 2026 · Título · Integrantes **[COMPLETAR]**

## 2. Índice
(Generar automáticamente.)

## 3. Introducción
**[COMPLETAR]** Qué es Mi Teleférico, por qué importa en La Paz y El Alto, qué se hizo en este trabajo (2–3 párrafos).

## 4. Descripción de la problemática
- Lugar y población: red de transporte por cable La Paz–El Alto (10 líneas, 26 estaciones) y sus usuarios.
- Usuarios beneficiados: pasajeros habituales, la empresa operadora, planificación municipal **[COMPLETAR]**
- Cómo se resuelve hoy: mapa oficial y decisión del usuario (**[COMPLETAR con la entrevista]**)
- Dificultades: no hay herramienta que calcule la ruta de menor tiempo, ni alternativas ante cierres **[COMPLETAR]**
- Decisiones que mejora el sistema: elegir ruta, prever alternativas si cierra una estación, identificar estaciones críticas.

## 5. Objetivos
Copiar los objetivos general y específicos del enunciado, adaptados a tu problema.

## 6. Metodología de recopilación de datos
**[COMPLETAR]** Fecha(s), lugar(es), responsable(s), procedimiento de cronometraje (3 mediciones por tramo, promedio), fuentes secundarias consultadas (mapa oficial, sitio de Mi Teleférico).

## 7. Evidencias del contexto real
**[COMPLETAR]** Entrevista o acta, fotos propias, tabla con datos originales (`hoja_cronometraje.csv`).

## 8. Fundamento teórico
Grafos dirigidos/no dirigidos, ponderados, grado, caminos, ciclos, conectividad, listas y matrices de adyacencia, DFS, BFS, Dijkstra, Kruskal, Prim, Union-Find. Citar Cormen, Rosen, Sedgewick, West. **[COMPLETAR con tus palabras]**

## 9. Construcción y representación del grafo
**Definición formal:** G = (V, E), V = {v1, …, v26}, E = {e1, …, e27}, w: E → R≥0.
- Vértice: una estación del Teleférico. Las estaciones de transbordo son un solo vértice.
- Arista: tramo de cable entre dos estaciones consecutivas de una línea (26) + 1 tramo peatonal San José–Prado.
- Peso: tiempo de viaje en **minutos** (alternativa: distancia en km).
- Tipo: **no dirigido** (se viaja en ambos sentidos) y **ponderado**.
- |V| = 26 ≥ 10 y |E| = 27 ≥ 15.
- Supuestos y restricciones: el tiempo de transbordo y de espera no se modela; el costo en Bs (pasaje por línea y por transbordo) no es un peso de arista; el tramo peatonal implica salir a la calle y pagar otro pasaje; los pesos son el promedio de **[COMPLETAR]** mediciones.
- Incluir: gráfico del grafo, lista de vértices, lista de aristas, matriz de pesos y lista de adyacencia (capturas de la pestaña «Representación»).

## 10. Aplicación de DFS
Nodo inicial, orden, aristas del árbol, alcanzables, componentes, ciclos. Utilidad en el problema. **[COMPLETAR con capturas y resultados]**

## 11. Aplicación de BFS
Niveles, cola, camino con menos aristas. Por qué BFS es mínimo solo con costos iguales. **[COMPLETAR]**

## 12. Aplicación de Dijkstra
Origen/destino elegidos, tabla de distancias y predecesores, camino, costo, ahorro frente a otra ruta. Por qué requiere w ≥ 0. **[COMPLETAR]**

## 13. Aplicación de Kruskal
Aristas ordenadas, aceptadas, rechazadas, árbol y costo. **[COMPLETAR]**

## 14. Aplicación de Prim
Nodo inicial, iteraciones, árbol y costo. **[COMPLETAR]**

## 15. Comparación de resultados
Tabla Kruskal vs Prim (costo, aristas, orden, tiempo, ventajas, limitaciones) y la validación manual A–F (`validacion_manual.md`) contra el sistema.

## 16. Descripción del sistema
Arquitectura por módulos (`grafo`, `algoritmos`, `validaciones`, `reportes`, `visual`, `main`), tecnologías (Python, Streamlit, pandas, matplotlib), funcionalidades y capturas de pantalla.

## 17. Casos de prueba
Tabla completa de `casos_de_prueba.md` con capturas.

## 18. Interpretación de resultados
Responder con tus resultados las 15 preguntas orientadoras del enunciado (sección 23 del PDF). **[COMPLETAR]**

## 19. Recomendaciones
Basadas en el reporte del sistema: estaciones de transbordo clave, estaciones críticas, rutas alternativas, tramos redundantes. **[COMPLETAR]**

## 20. Conclusiones
No basta decir «los algoritmos funcionaron»: qué se descubrió de la red, qué ruta/alternativa conviene, qué tiempos se podrían reducir, quiénes se benefician, qué limitaciones tienen los datos (por ejemplo, no se midió tiempo de espera ni de transbordo) y qué mejorar en una versión futura (tiempos por hora pico, costos en Bs, minibuses como capa adicional). **[COMPLETAR]**

## 21. Referencias bibliográficas
- Cormen, Leiserson, Rivest y Stein. *Introduction to Algorithms*. MIT Press.
- Rosen, K. H. *Discrete Mathematics and Its Applications*. McGraw-Hill.
- Sedgewick y Wayne. *Algorithms*. Addison-Wesley.
- West, D. B. *Introduction to Graph Theory*. Prentice Hall.
- Mi Teleférico, mapa de líneas y estaciones: https://www.miteleferico.bo **(fecha de consulta: [COMPLETAR])**
- Datos de líneas, tiempos y transbordos usados como punto de partida: https://lapazteleferico.com/mapa-mi-teleferico/ y https://es.wikipedia.org/wiki/Mi_Telef%C3%A9rico **(contrastar con el mapa oficial)**

## 22. Anexos
Hoja de cronometraje, entrevista/acta, fotografías, código fuente, manual de usuario, registro de errores, declaración de IA, enlace al repositorio.
