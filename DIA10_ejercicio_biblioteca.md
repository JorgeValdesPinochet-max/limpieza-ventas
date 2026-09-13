# Día 10 — Ejercicio práctico: primeras 3 entradas de mi biblioteca

Ejercicio de la Semana 2: dejar de improvisar prompts para tareas que se
repiten, documentando las primeras 3 entradas de mi biblioteca personal
(ver `biblioteca-prompts.md` para las 10 completas).

Estas 3 entradas están escritas desde mi punto de vista como quien
**produce y entrega** el trabajo (no desde el rol de quien revisa a otros).

---

## Ficha 1

**Nombre del prompt:** Limpieza de datasets con reglas de negocio explícitas
(nulo vs. inválido)

**Propósito:** Generar funciones de limpieza de datos en pandas que
distingan errores de calidad de datos (texto no numérico) de información
de negocio válida (nulos intencionales), y que parseen fechas de formatos
mixtos sin fallar en silencio.

**Cuándo usarlo:** Al inicio de cualquier análisis exploratorio con un
dataset nuevo, antes de tocar el análisis en sí.

**Ajuste más útil hasta ahora:** Agregar la restricción explícita de usar
`format="mixed"` en `pd.to_datetime()`. Sin esto, pandas asume un solo
formato de fecha para toda la columna a partir de la primera fila, y
convierte silenciosamente en `NaT` todas las fechas con formato distinto
— lo descubrí ejecutando el código, no leyéndolo.

**Próxima mejora:** Agregar una instrucción para que la función también
devuelva un resumen (% de filas con monto pendiente, % con monto
inválido), así el resultado es más fácil de auditar de un vistazo.

---

## Ficha 2

**Nombre del prompt:** Auto-revisión de mi código antes de entregarlo

**Propósito:** Obtener una crítica honesta de mi propio código, como si
un ingeniero senior lo evaluara, para corregir problemas ANTES de
entregarlo en una tarea, un PR real, o mostrarlo en una entrevista técnica.

**Cuándo usarlo:** Justo antes de dar por "terminado" cualquier código
que voy a entregar o compartir — es mi último filtro de calidad, no un
reemplazo de pensar el problema yo mismo.

**PROMPT:**
```
ROL: Eres un ingeniero de software senior evaluando código en una entrevista
técnica o revisión de PR, con altos estándares pero feedback constructivo.

CONTEXTO: Este es mi código: [PEGAR CÓDIGO REAL]. Lo voy a [entregar como
tarea / subir a un PR real / mostrar en una entrevista técnica]. Mi nivel
de experiencia es [junior / en transición a Data Science / autodidacta].

INSTRUCCIÓN: Evalúa el código como lo haría un revisor real: identifica
(1) errores de lógica o casos borde no manejados, (2) problemas de estilo
o legibilidad, (3) decisiones de diseño que un entrevistador cuestionaría,
y (4) qué es lo que SÍ está bien hecho (para no perderlo al refactorizar).

FORMATO: Lista priorizada de mayor a menor gravedad, con el problema, por
qué importa, y la corrección sugerida con código.

RESTRICCIÓN: No suavices los problemas reales solo para sonar amable —
quiero saber exactamente qué vería mal un evaluador real, aunque sea
incómodo de leer.
```

**Ajuste más útil hasta ahora:** Agregar la restricción de "no suavizar
los problemas reales solo para sonar amable". La primera vez que probé
"revisa mi código" sin esa restricción, el feedback fue demasiado gentil
conmigo mismo — justo lo opuesto de lo que necesito antes de una entrega
real.

**Próxima mejora:** Agregar la opción de pedir que compare mi solución
contra cómo la resolvería un candidato senior para el mismo problema,
así identifico no solo errores sino diferencias de nivel.

---

## Ficha 3

**Nombre del prompt:** Tests pytest con casos borde de reglas de negocio

**Propósito:** Generar suites de tests que cubran las reglas de negocio
reales de una función (no solo el camino feliz), evitando falsos
positivos causados por la propia lógica de la función bajo prueba.

**Cuándo usarlo:** Inmediatamente después de escribir o recibir una
función de procesamiento de datos, antes de darla por terminada.

**Ajuste más útil hasta ahora:** Agregar la restricción de usar
identificadores distintos entre filas de prueba que se van a comparar.
Sin eso, un test mío usaba el mismo `cliente_id` para dos filas que
quería comparar, y la deduplicación de mi propia función las colapsaba
antes de poder verificar nada — un `KeyError` que no tenía que ver con
el bug real que buscaba probar. (Ver el commit real de esta corrección
en el historial de este repositorio.)

**Próxima mejora:** Agregar una instrucción para que también genere un
test de "regresión" que reproduzca exactamente un bug ya corregido, para
asegurar que no vuelva a aparecer.

---

## Ejercicio de extensión — Prueba de estrés (Ficha 2)

Ejecuté el prompt de auto-revisión (Ficha 2) tres veces con contextos
distintos, para ver si es robusto o frágil.

**Variación A — Mi función `limpiar_dataset_ventas()`, para entregar
como tarea del curso:**
Señaló que la función no valida qué pasa si el DataFrame llega vacío
(0 filas) — un caso borde que mis propios tests no cubrían. Feedback
específico y útil.

**Variación B — Un script de API REST con Flask, para mostrar en
entrevista técnica:**
Al cambiar el contexto a "entrevista técnica", el tono se ajustó
apropiadamente: más exigente con manejo de errores HTTP y estructura
de respuestas.

**Variación C — Un test suite básico, para subir a un PR real de un
proyecto grupal:**
Acá mostró fragilidad: evaluó bien el código, pero no dijo nada sobre si
mis mensajes de commit o la descripción del PR eran adecuados, porque el
CONTEXTO que le di se enfocó solo en el código, no en el paquete
completo de la entrega.

**Conclusión:** El prompt es robusto para variar el **propósito de la
entrega** (tarea/entrevista/PR) — el tono se ajusta bien con solo
cambiar esa palabra en el CONTEXTO. Es frágil cuando la entrega real
incluye más que código (como un PR con historial de commits) —
necesitaría recibir también el mensaje de commit y la descripción del
PR como parte del CONTEXTO, no solo el código aislado.
