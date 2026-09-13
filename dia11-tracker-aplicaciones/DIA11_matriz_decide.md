# Día 11 — Framework DECIDE: elegir con criterio, no por entusiasmo

**Contexto:** Estoy en proceso de búsqueda de empleo mientras construyo evidencia
práctica de este curso. Apliqué DECIDE a mis tareas reales de las últimas dos
semanas (búsqueda de empleo + trabajo en el repo) para elegir UNA tarea Tipo A
y automatizarla esta semana.

## Matriz DECIDE

| # | Tarea | Frecuencia (1-5) | Estructura (1-5) | Juicio (1-5) | Score (F×E÷J) | Tipo |
|---|-------|:-:|:-:|:-:|:-:|:-:|
| 1 | Registrar y dar seguimiento a aplicaciones enviadas (empresa, fecha, estado, próxima acción) | 5 | 5 | 1 | 25 | **A** |
| 2 | Commit + push de cada entrega nueva al repo con mensaje descriptivo | 5 | 5 | 1 | 25 | **A** |
| 3 | Buscar y filtrar vacantes por palabras clave (Python, data, junior) | 5 | 4 | 2 | 10 | B |
| 4 | Ejecutar pytest y guardar el resultado como evidencia | 3 | 5 | 1 | 15 | B (límite) |
| 5 | Adaptar el CV/bullets a cada oferta específica | 4 | 3 | 4 | 3 | C |
| 6 | Redactar mensaje de outreach personalizado a reclutador | 3 | 2 | 4 | 1.5 | C |
| 7 | Aplicar mi función de limpieza a un dataset nuevo para portafolio | 3 | 4 | 2 | 6 | C |
| 8 | Redactar post de LinkedIn mostrando avance del día | 2 | 3 | 4 | 1.5 | C |
| 9 | Preparar brief antes de una entrevista | 1 | 2 | 5 | 0.4 | C |

**Criterio de clasificación:** Score > 15 → Tipo A (automatizar ya). Score 8-15
→ Tipo B (asistir con IA). Score < 8 → Tipo C (mantener manual, requiere
criterio humano).

## Tarea Tipo A elegida: Registro y seguimiento de aplicaciones enviadas

Entre las dos tareas empatadas en score (25), elegí esta por sobre "commits al
repo" porque:

- Es la que **hoy hago peor**: llevo el registro mentalmente y se me pierden
  datos (cuándo apliqué, cuándo toca hacer seguimiento).
- El flujo de git ya lo tengo internalizado y funcionando bien desde días
  anteriores; automatizarlo no me ahorraría tanto tiempo real.
- Tiene **estructura clara (5)**: siempre son los mismos campos (empresa,
  cargo, fecha, canal, estado).
- Tiene **juicio mínimo (1)**: son reglas fijas, no criterio situacional
  ("si pasaron 7 días sin respuesta → marcar seguimiento pendiente").
- Tiene **frecuencia alta (5)**: aplico casi a diario mientras busco empleo.

Las tareas Tipo C (CV, outreach, posts de LinkedIn, briefs de entrevista) las
mantengo manuales a propósito: automatizarlas de raíz arriesga perder
autenticidad o cometer errores tipo "Estimado [EMPRESA]".

## Ejercicio de extensión — Pregunta a Claude

**Pregunta:** "Estas son mis tareas recurrentes Tipo A: (1) registro y
seguimiento de aplicaciones de trabajo, (2) commit + push de cada entrega al
repo. ¿Cuál recomendarías automatizar primero y por qué? ¿Qué enfoque técnico
sugerirías?"

**Respuesta (resumen):** Automatizar primero el tracker de aplicaciones,
porque es la de mayor ROI (más tiempo ahorrado, hoy peor resuelta) y la más
simple de construir con mi stack actual. Enfoque técnico sugerido: un CSV
local + script Python con pandas que calcule automáticamente la fecha de
seguimiento (fecha de envío + 7 días) y genere un resumen de pendientes,
validado con pytest. No requiere IA generativa porque es 100% reglas y datos
estructurados — usar un flujo con prompts aquí sería innecesariamente frágil
y caro de mantener.

## Implementación

Construí `tracker.py`: agrega aplicaciones a un registro CSV, calcula
automáticamente la fecha de seguimiento (envío + 7 días) y genera un resumen
de qué aplicaciones necesitan seguimiento hoy. Validado con 12 tests pytest
(`test_tracker.py`), todos pasando.

```bash
# Agregar una aplicación
python tracker.py agregar --empresa "Acme Corp" --cargo "Data Analyst" --fecha 2026-09-01 --canal LinkedIn

# Ver resumen general
python tracker.py resumen

# Ver solo las que necesitan seguimiento hoy
python tracker.py pendientes
```

Próximo paso (Escalar, no esta semana): conectar con Gmail API para detectar
automáticamente correos de confirmación y auto-poblar el CSV. Queda fuera del
alcance de esta entrega porque pasaría a ser Tipo B (requiere más juicio y
manejo de excepciones).