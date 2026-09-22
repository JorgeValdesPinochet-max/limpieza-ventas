# Día 17 — Ficha de decisión: próxima automatización (v3 del sistema)

- **Contexto:** en el Día 15 identifiqué dos posibles siguientes pasos para
  evolucionar mi tracker de aplicaciones: (A) integrar Gmail API para
  auto-detectar correos de confirmación, o (B) construir un generador de
  mensajes de outreach usando RAG (CV + oferta como documentos de
  contexto). Con tiempo limitado, tocaba decidir cuál construir primero.

- **Opciones:**
  1. **Integración con Gmail:** automatizar la detección de correos de
     confirmación para auto-poblar el CSV del tracker, eliminando el
     registro manual.
  2. **Generador de outreach con RAG:** cargar mi CV + el texto de una
     oferta específica, y que la IA genere un borrador de outreach
     fundamentado en ambos documentos (siguiendo el criterio de calidad
     ya definido en el Día 13).

- **Aporte de la IA (exploración + interpretación):**
  Al procesar los datos reales de mi mapa de oportunidades (Día 05) y mi
  plan de evolución (Día 15), la IA identificó que el ahorro de tiempo de
  la Opción A es marginal — el registro manual actual ya toma ~15 segundos
  gracias al tracker existente, así que integrar Gmail optimizaría algo
  que ya está casi resuelto. En cambio, la Opción B ataca una tarea que
  hoy me toma ~1.5 horas al mes con calidad variable, y reutiliza una
  competencia (RAG) que ya demostré dominar en el Día 14, con menor riesgo
  técnico que manejar autenticación OAuth sobre mi correo real.

- **Decisión final:** construir primero el **generador de outreach con
  RAG** (Opción B).

- **Razón principal:** mejor relación esfuerzo/impacto dado mi situación
  actual — la Opción A resuelve un problema que ya está en gran parte
  resuelto (el ahorro marginal es bajo), mientras que la Opción B mejora
  una tarea de mayor fricción real (outreach, calidad inconsistente) sin
  introducir la complejidad y el riesgo de seguridad de conectar una API
  externa a mi correo personal. La integración con Gmail queda como v4,
  para cuando tenga más experiencia acumulada con integraciones de APIs.

## Ejercicio de extensión — medición de tiempo por fase

Pendiente de cronometrar en la próxima decisión profesional real que
enfrente: cuánto tiempo paso explorando/procesando vs. interpretando vs.
decidiendo, con y sin asistencia de IA. La expectativa según la lección de
hoy: sin IA, ~70% del tiempo se va en explorar/procesar y solo 30% en
decidir de verdad; con IA, la proporción debería invertirse hacia más
tiempo de interpretación real (mejor información) y decisión, y menos
tiempo perdido en procesar datos a mano.
