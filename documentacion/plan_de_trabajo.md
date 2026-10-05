# Plan de trabajo (4 avances)

Ajusta las fechas con tu docente. Si trabajas en equipo, reparte por módulo y que **cada uno pueda explicar todo**.

## Avance 1 — Diagnóstico (problema, usuarios, datos, evidencias)
- [ ] Escribir el planteamiento: el problema, quién usa el Teleférico, cómo se decide hoy qué ruta tomar
- [ ] Recorrido real: fotos propias de estaciones, croquis, notas (fecha, lugar, responsable)
- [ ] Entrevista breve a un usuario (guion en `guia_trabajo_de_campo.md`) o acta de observación
- [ ] Cronometrar los 27 tramos (`evidencias/hoja_cronometraje.csv`)
- [ ] Primer boceto del grafo a mano (foto)

## Avance 2 — Modelado
- [ ] `python -m app.actualizar_pesos ...` y revisar que no queden `ESTIMADO`
- [ ] Verificar vértices/aristas/pesos contra el mapa oficial
- [ ] Capturas de matriz de pesos, lista de adyacencia y grafo dibujado
- [ ] Justificar los pesos y los supuestos (sección 9 del informe)
- [ ] Boceto de la interfaz (a mano o en cualquier herramienta)

## Avance 3 — Algoritmos
- [ ] Leer `app/algoritmos.py` hasta poder explicar cada función
- [ ] Resolver a mano el grafo A–F (`documentacion/validacion_manual.md`) y comparar con el sistema
- [ ] Ejecutar `pytest -v` y capturar la salida
- [ ] Registrar errores que encuentres y cómo los corregiste (parte de las evidencias)

## Avance 4 — Sistema final
- [ ] Capturas de los 10 casos de prueba (`casos_de_prueba.md`)
- [ ] Informe PDF (`informe_plantilla.md`) y manual de usuario
- [ ] Video de 5–8 min: problema → datos → demo de los 5 algoritmos → cierre de estación → conclusiones
- [ ] Repositorio Git con commits tuyos (`git init`, commits por avance)
- [ ] Declaración de uso de IA (`declaracion_ia.md`)
- [ ] Ensayo de defensa con `guia_defensa.md`
