# Día 9 — Ciclo de refinamiento aplicado

Ejercicio práctico: transformar un prompt/output funcional en un activo más
fino y reusable, documentando el ciclo de evaluación → feedback → resultado
refinado → aprendizaje reusable.

Caso real usado: la función `limpiar_dataset_ventas()` de este mismo
repositorio (ver `limpieza_ventas.py`).

---

## Ficha de refinamiento

**Output original:**
Le pedí a la IA una función de limpieza de datos con el prompt que armé en
el Día 06 (contexto e instrucción, sin ejemplos — zero-shot):

> "Eres un ingeniero de datos senior... Escribe una función que: (1) parsee
> la columna fecha... (2) NO elimine filas con monto nulo... (3) elimine
> duplicados... (4) normalice categoria..."

El código que obtuve usaba `pd.to_datetime(df["fecha"], errors="coerce",
utc=True)` para parsear las fechas — sin el parámetro `format="mixed"`.

**Dimensión a corregir:** Precisión (no profundidad ni tono — el código se
veía bien escrito, pero producía un resultado incorrecto sin avisar).

**Feedback exacto que di:**
No lo detecté leyendo el código, lo detecté **ejecutándolo**. Al correrlo
con mi dataset de prueba (fechas en formato ISO, día/mes/año, texto en
inglés, y con zona horaria), vi que varias fechas se convertían en `NaT`
sin razón aparente. Mi feedback fue:

> "Esta columna 'fecha' tiene formatos mixtos: '2024-01-15', '15/01/2024',
> 'Jan 15 2024', y fechas con zona horaria. Al ejecutar tu función, las
> fechas después de la primera se están perdiendo (quedan como NaT).
> Corrígelo sin cambiar la lógica de negocio, solo el parseo de fechas."

**Resultado refinado:**
Se agregó `format="mixed"` a la llamada de `pd.to_datetime()`. Con ese
cambio, las seis fechas de prueba se parsearon correctamente, incluidas
las de distinto formato y con zona horaria. Ver el commit correspondiente
en el historial de este repositorio.

**Aprendizaje reusable (para mi biblioteca de prompts):**
Cuando le pido a una IA una función que procese fechas en formato texto
con formatos mixtos, debo especificar explícitamente en el prompt: *"la
columna puede tener más de un formato de fecha en la misma columna, usa
parseo por fila y no por inferencia global"* — porque el comportamiento
por defecto de pandas asume un solo formato para toda la columna y falla
silenciosamente en el resto. Esto queda anotado como restricción fija en
mi plantilla de prompts para limpieza de datos, no como algo que reviso
caso por caso.

---

## Ejercicio de extensión — Iteración de técnica

Mi prompt original era **zero-shot**: contexto e instrucción, sin ningún
ejemplo de entrada/salida.

Para probar la iteración de técnica, tomé el mismo prompt base y le agregué
un ejemplo concreto (**few-shot**):

> "Ejemplo: si recibo la fila `fecha='15/01/2024', monto='N/A'`, el
> resultado esperado es `fecha=2024-01-15, monto=NaN, monto_invalido=True,
> monto_pendiente=False`. Ahora escribe la función completa."

**¿Cambiar de técnica produjo una mejora mayor que refinar las palabras?**

Sí, con una diferencia importante: cuando solo describí la regla en
palabras (zero-shot), la IA entendió el *qué* pero no anticipó el caso
límite de formatos mixtos en la misma columna — ese bug se encontró recién
al ejecutar el código. Cuando se agregó el ejemplo concreto de fila
(few-shot), el ejemplo mismo obliga a pensar en un caso específico y
verificable antes de que la IA genere nada — lo cual habría facilitado
detectar el problema de formatos mixtos desde el diseño del prompt, no
después de la ejecución.

**Conclusión para mi biblioteca:** para tareas de transformación de datos
con reglas de negocio específicas (como distinguir "nulo" de "inválido"),
few-shot con un ejemplo de fila real vale más que una descripción larga en
palabras — porque el ejemplo actúa como test implícito desde el momento en
que se escribe el prompt, no solo desde que se ejecuta el código.
