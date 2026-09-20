# Día 13 — Semáforo de delegación a IA

**Contexto:** clasifico tareas reales de mi trabajo actual (búsqueda de
empleo + construcción de portafolio técnico), retomando la lista del Día 11
(framework DECIDE), pero ahora con el criterio de "¿se lo delego a la IA, lo
comparto con ella, o lo mantengo 100% humano?" — que es una pregunta distinta
a "¿se puede automatizar con un script?".

## Semáforo de delegación

**Zona Verde — delego casi completo:**
- Generar el andamiaje inicial de tests unitarios (pytest) para un script
  nuevo, a partir de la especificación de qué debe hacer la función.
- Resumir una vacante larga a los 3-4 puntos clave (stack, seniority,
  modalidad) para decidir rápido si aplico o no.
- Clasificar vacantes guardadas por palabras clave (Python, junior, remoto).

**Zona Amarilla — colaboración (IA borrador, yo reviso y completo):**
- Redactar el mensaje de outreach inicial a un reclutador o hiring manager.
- Adaptar los bullets del CV al lenguaje específico de una oferta puntual.
- Generar el código de un script de automatización (como `tracker.py`) a
  partir de mi descripción del problema.

**Zona Roja — no delego, decido yo:**
- Aceptar o rechazar una oferta de trabajo.
- Negociar directamente salario o condiciones con un reclutador (la IA puede
  ayudarme a *preparar* argumentos, pero la conversación y la decisión final
  de qué pedir son mías).
- Comunicar una renuncia a un empleador actual, si llegara a aplicar.

## Criterio de calidad — Zona Amarilla

**Tarea elegida:** redactar el mensaje de outreach a un reclutador.

Un buen borrador de outreach, en mi contexto, significa:
1. Menciona algo **específico y real** de la empresa o la vacante (un
   producto, un proyecto público, una tecnología del stack mencionada en la
   oferta) — nunca una frase genérica tipo "Estimado equipo de RRHH".
2. Incluye **un logro técnico concreto con métrica**, no una lista de
   habilidades sin contexto (ejemplo: "reduje el tiempo de limpieza de datos
   de X a Y" en vez de "tengo experiencia en pandas").
3. Longitud máxima de **150 palabras** — un reclutador no lee un párrafo largo.
4. Termina con una **pregunta o llamada a la acción clara** (pedir 15 minutos
   de llamada, no solo "quedo atento").

Si el borrador de la IA no cumple los 4 puntos, no lo envío tal cual — lo
ajusto yo antes de mandarlo. Esto convierte la revisión en una lista de
verificación de segundos, no en reescribir desde cero.

## Mecanismo de supervisión — Zona Verde

**Tarea elegida:** generar el andamiaje inicial de tests unitarios (pytest).

- **Primera vez con un patrón nuevo:** reviso el 100% de los tests generados
  línea por línea, para confirmar que las aserciones realmente prueban algo
  (no son tautológicas, tipo `assert True`) y que cubren casos límite reales.
- **Una vez validado el patrón:** confío en que la IA genera correctamente
  ese tipo de test, y mi supervisión pasa a ser automática: si `pytest`
  corre y pasa en verde, lo acepto.
- **Muestreo semanal:** una vez por semana, sin previo aviso (a mí mismo),
  elijo un test al azar de los generados esa semana y lo reviso a fondo,
  para detectar si la calidad se degradó con el tiempo.
- **Alerta:** si algún test generado por IA falla al correrlo contra el
  código real (no contra datos de ejemplo), lo trato como señal de que debo
  volver a revisar el 100% por un tiempo, no solo por muestreo.

## Ejercicio de extensión — aplicación real esta semana

Tarea Amarilla elegida: redactar el mensaje de outreach para la próxima
vacante interesante que encuentre.

**Plan de medición:**
1. Pedir a Claude/ChatGPT el borrador inicial usando los criterios de calidad
   de arriba como parte del prompt.
2. Revisar el borrador contra el checklist de 4 puntos.
3. Ajustar con mi criterio (tono personal, detalles que la IA no puede saber).
4. Medir el tiempo total (generar + revisar + ajustar) vs. el tiempo que me
   toma históricamente escribir uno desde cero manualmente (~20-25 minutos).

**Resultado esperado:** si el ciclo completo toma menos de 10 minutos y el
mensaje cumple los 4 criterios, la delegación de esta tarea a Zona Amarilla
queda validada con evidencia, no solo con la intuición de que "ahorra tiempo".
