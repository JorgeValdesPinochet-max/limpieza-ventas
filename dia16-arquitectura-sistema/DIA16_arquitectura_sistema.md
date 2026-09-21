# Día 16 — Arquitectura de mi sistema personal potenciado por IA

## Mapa mínimo del sistema

**Capa 1 — Entrada:** lo que ya tengo es el mapa de oportunidades (Día 05,
reconstruido) que identifica de dónde entra la información a mi sistema:
correo de reclutadores, portales de vacantes, y datasets de práctica para
portafolio. **Lo que falta:** ningún procesamiento automático — hoy reviso
correo y vacantes 100% manualmente, sin resúmenes ni pre-filtrado por IA.
Esta es la capa menos desarrollada de las cuatro (ver "Eslabón más débil").

**Capa 2 — Procesamiento:** ya tengo dos componentes reales funcionando:
mis prompts documentados (Día 10) y mi automatización de tracking de
aplicaciones (`tracker_v2.py`, Días 11-12), con criterios explícitos de
qué delego a la IA y qué no (Día 13). **Lo que falta:** procesamiento
automático de las vacantes que encuentro (tarea #2 del Día 05) — hoy las
filtro manualmente por palabras clave.

**Capa 3 — Memoria:** ya tengo mi `biblioteca-prompts.md` con 10 prompts
documentados y probados, y todo mi repositorio de GitHub organizado por
día (`dia11-tracker-aplicaciones/`, `dia12-script-robusto/`, etc.), que
funciona como historial recuperable de todo lo que he construido.
**Lo que falta:** un índice o README central que conecte todas las piezas
— hoy cada carpeta es autónoma, pero no hay un solo lugar que diga "así se
conecta todo esto".

**Capa 4 — Ejecución:** ya tengo el hábito diario de "aplicar → registrar
en el tracker → revisar pendientes" que se volvió rutina desde el Día 11.
**Lo que falta:** un momento fijo del día dedicado a esto (hoy lo hago de
forma reactiva, cuando se me ocurre, no en un bloque protegido de tiempo).

## Eslabón más débil

**Capa 1 — Entrada y captura.** Es la única capa donde no existe ningún
componente de IA todavía — todo el procesamiento de correo y vacantes es
100% manual. Las otras tres capas ya tienen al menos una pieza real
funcionando y probada; esta capa está en cero.

**Cambio concreto esta semana:** aplicar la tarea Verde ya identificada en
el Día 13 ("resumir una vacante larga a los 3-4 puntos clave") de forma
sistemática — cada vez que encuentre una vacante candidata, antes de leerla
completa, pedirle a la IA el resumen de stack/seniority/modalidad. Es la
mejora más pequeña y más rápida de implementar de las cuatro capas, y
convierte la Capa 1 de "cero" a "algo real" sin necesidad de construir
ninguna herramienta nueva — solo un hábito de prompt.

## Constitución potenciada por IA (principios personales)

1. **No agrego una herramienta nueva a menos que reemplace o complemente
   una que ya uso activamente.** Evita acumular suscripciones o apps que
   uso una vez y abandono.

2. **Solo automatizo tareas que ya hago de forma manual y consistente al
   menos 3 veces** (principio del framework DECIDE, Día 11). La
   automatización resuelve un patrón comprobado, no una hipótesis.

3. **Toda automatización se prueba con datos reales antes de considerarla
   terminada** (Días 12 y 15) — un script sin evidencia de que funciona
   con mis propios datos no cuenta como "listo", cuenta como borrador.

4. **Nunca delego a la IA decisiones de Zona Roja** (Día 13): aceptar una
   oferta, negociar condiciones, o cualquier decisión con consecuencias
   reales irreversibles. La IA informa esas decisiones; no las toma por
   mí.

5. **Reviso mi sistema (prompts, scripts, documentación) al menos una vez
   por semana**, no solo cuando algo falla. El mantenimiento programado
   evita que las piezas sueltas se degraden sin que yo lo note — es el
   mismo principio de "muestreo semanal" que definí para supervisar tests
   generados por IA (Día 13).

## Por qué esto no es un ejercicio académico

Las cuatro capas ya no son teoría — cada una tiene al menos un componente
real y verificable en mi repositorio de GitHub, construido y probado
durante las Semanas 1 a 3 de este curso. El valor de este mapa es que ahora
sé exactamente dónde está el hueco real (Capa 1) y tengo un cambio concreto
y de bajo esfuerzo para cerrarlo esta semana, en vez de seguir acumulando
herramientas sueltas sin criterio.
