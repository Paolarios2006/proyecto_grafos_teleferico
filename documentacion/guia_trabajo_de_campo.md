# Guía de trabajo de campo (lo que debes hacer tú)

La práctica **no acepta** datos, fotos ni entrevistas inventadas. Esto es lo que necesitas, con el mínimo esfuerzo.

## 1. Recorrido y cronometraje (medio día)
Lo más eficiente: recorrer línea por línea con el celular.
1. Abre `evidencias/hoja_cronometraje.csv` (27 tramos ya listados).
2. En cada estación, inicia el cronómetro cuando la cabina **sale** y párelo cuando **llega** a la siguiente. Repite 3 veces si puedes (`t1_seg`, `t2_seg`, `t3_seg`).
3. Llena `fecha`, `hora`, `lugar` y `responsable` en cada fila.
4. Tramo peatonal San José ↔ Prado: cronometra caminando (sale de una estación, llega a la otra).
5. Anota en `observaciones` cualquier cosa rara (fila larga, cabina detenida, línea cerrada).
6. Toma fotos propias: entrada de estaciones, mapa de la red, boletería, cabinas. Guárdalas en `evidencias/fotografias/`.
7. Si una línea está cerrada ese día, anótalo; no inventes el tiempo.

Si no puedes fotografiar por permisos, escribe un **acta de observación** (plantilla abajo).

Luego: `python -m app.actualizar_pesos evidencias/hoja_cronometraje.csv`

## 2. Entrevista breve (10 minutos)
A un usuario habitual (o a un encargado). Pide permiso, anota nombre (o iniciales si prefiere anonimato), fecha y lugar.
1. ¿Con qué frecuencia usa el Teleférico y para qué trayectos?
2. ¿Cómo decide hoy qué líneas tomar para llegar a su destino?
3. ¿Qué transbordos le resultan más largos o incómodos?
4. ¿Qué pasa cuando una línea está cerrada? ¿Qué alternativa usa?
5. ¿Qué información le gustaría tener antes de viajar (tiempo total, mejor ruta, alternativas)?
6. ¿Qué tramos o estaciones considera más importantes para la ciudad?

Guarda la entrevista (audio, foto de tus notas o transcripción) en `evidencias/entrevistas/`.

## 3. Acta de observación (plantilla)
```
ACTA DE OBSERVACIÓN
Fecha: __________  Hora inicio/fin: __________
Lugar (estación/línea): ____________________
Responsable(s): ____________________
Qué se observó (flujo de personas, tiempos de espera, transbordos, incidentes): __________
Procedimiento seguido para obtener los datos: __________
Firma o conformidad (encargado de estación, si aplica): __________
```

## 4. Datos del contexto que debes verificar tú
- Tarifa vigente por línea y por transbordo (se citó Bs 3 por línea y Bs 2 por transbordo; **confirma el valor actual**).
- Horarios de operación (lunes a sábado y domingos/feriados).
- Que las 26 estaciones y su orden en cada línea coincidan con el mapa oficial (miteleferico.bo).
- Si alguna línea está en mantenimiento o cerrada el día del recorrido.
