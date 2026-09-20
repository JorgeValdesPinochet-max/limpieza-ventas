# Día 14 — RAG: comparación sin documento vs con documento real

## Comparación express

- **Documento usado:** `tracker_v2.py` (el script robusto del Día 12, ya
  existente en mi repositorio real).

- **Sin RAG (pregunta genérica, sin adjuntar el archivo):**
  Pregunté "¿cómo puedo hacer que mi script de registro de datos en CSV sea
  más robusto?" sin dar el código. La respuesta fue una lista de buenas
  prácticas de manual: usar try/except, validar campos, usar logging,
  especificar encoding, evitar rutas hardcodeadas, agregar tests. Todo
  correcto, pero **genérico** — es la misma respuesta que le darían a
  cualquier persona con cualquier script de CSV. No dice qué de MI código
  específicamente falla.

- **Con RAG (mismo tipo de pregunta, con el archivo real cargado):**
  Con `tracker_v2.py` como contexto, la respuesta identificó 4 problemas
  concretos y verificables en el código real:
  1. `CSV_DEFECTO = Path("aplicaciones.csv")` es una ruta relativa — se
     rompe si el script se ejecuta desde otra carpeta (ej: una tarea
     programada).
  2. No se especifica `encoding="utf-8"` al leer/escribir el CSV — riesgo
     real si el campo `notas` contiene tildes o "ñ".
  3. Todo el output usa `print()`, incluidos los errores — no hay
     trazabilidad histórica si algún día se automatiza con un cron job.
  4. No hay manejo de `PermissionError` si el CSV está abierto en Excel al
     momento de escribir.

- **Diferencia más visible:** la respuesta sin RAG fue *correcta pero
  intercambiable* — serviría para cualquier script. La respuesta con RAG fue
  *específica y verificable* — cada punto señala una línea concreta de mi
  código y un escenario real de mi flujo de trabajo (aplicar a trabajos,
  escribir notas con tildes, correr el script en el futuro de forma
  automatizada). Esa es la diferencia entre "consejo genérico de manual" y
  "revisión de código real".

- **Otros 2 usos posibles en mi trabajo:**
  1. Cargar mi CV actual + una oferta de trabajo específica, y pedirle a la
     IA que identifique qué bullets de mi CV coinciden literalmente con los
     requisitos de la oferta y cuáles me faltan — en vez de pedirle
     "mejora mi CV" en abstracto.
  2. Cargar mi `biblioteca-prompts.md` (mis 10 prompts documentados) junto
     con un prompt nuevo que esté escribiendo, y pedirle a la IA que
     verifique si ya tengo un prompt similar documentado antes de crear uno
     redundante.

## Ejercicio de extensión — 3 áreas donde RAG mejoraría mis prompts actuales

1. **Revisión de código de mis propios scripts (`tracker.py`, `tracker_v2.py`,
   `limpieza_ventas.py`).**
   Documentos a cargar: los archivos `.py` completos del repo.
   Pregunta actual (genérica): "¿cómo mejoro el manejo de errores en Python?"
   Pregunta con RAG: "revisa este archivo específico y dime, línea por línea,
   qué falla dado que lo uso para [caso de uso real]."

2. **Adaptación de CV y outreach a ofertas específicas (conecta con el Día 13,
   Zona Amarilla).**
   Documentos a cargar: mi CV actual + el texto completo de la oferta de
   trabajo.
   Pregunta actual (genérica): "escribe un mensaje de outreach para un
   reclutador de tecnología."
   Pregunta con RAG: "compara mi CV con esta oferta específica y dime qué
   tres logros míos debería destacar en el outreach, citando los requisitos
   exactos de la oferta."

3. **Consistencia de mi biblioteca de prompts (Día 10).**
   Documentos a cargar: `biblioteca-prompts.md`.
   Pregunta actual (genérica): "dame un buen prompt para generar tests
   unitarios."
   Pregunta con RAG: "revisa mi biblioteca de prompts existente y dime si ya
   tengo uno para esto, o ayúdame a extender el más parecido en vez de crear
   uno nuevo desde cero."
