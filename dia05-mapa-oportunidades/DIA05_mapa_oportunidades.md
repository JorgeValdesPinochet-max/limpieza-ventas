# Día 05 — Mapa de oportunidades AI (reconstrucción)

**Nota de transparencia:** este documento no se generó en el momento
original del Día 05 — se reconstruye ahora, en el Día 16, para completar la
base que las semanas siguientes necesitan. Se arma con tareas reales de mi
rutina de búsqueda de empleo y construcción de portafolio técnico (mi
contexto real durante todo el curso), no con tareas inventadas.

## 1. Inventario (12 tareas reales)

| # | Tarea | Categoría | Frecuencia | Tiempo por ocurrencia |
|---|---|---|---|---|
| 1 | Revisar bandeja de correo por respuestas de reclutadores | Comunicación | Diaria | 10-15 min |
| 2 | Buscar y filtrar nuevas vacantes en LinkedIn/portales | Gestión | Diaria | 20-30 min |
| 3 | Completar formularios y aplicar a vacantes | Gestión | Diaria | 15-20 min c/u |
| 4 | Registrar aplicaciones enviadas y dar seguimiento | Gestión | Diaria | 2-3 min c/u (antes) |
| 5 | Adaptar CV/bullets a una oferta específica | Creación | Semanal | 15-20 min |
| 6 | Redactar mensaje de outreach a reclutador | Comunicación | Semanal | 20-25 min |
| 7 | Escribir código de portafolio (scripts, funciones) | Creación | Semanal | 1-2 horas |
| 8 | Escribir tests unitarios para ese código | Análisis | Semanal | 30-45 min |
| 9 | Publicar avances en LinkedIn | Comunicación | Semanal | 15 min |
| 10 | Preparar/estudiar para entrevistas técnicas | Análisis | Semanal | 1-2 horas |
| 11 | Mantener y ampliar mi biblioteca de prompts | Gestión | Semanal | 20 min |
| 12 | Limpiar/preparar datasets de práctica para portafolio | Análisis | Semanal | 45 min - 1 hora |

## 2. Evaluación de automatizabilidad

| # | Tarea | ¿Repetitiva? | ¿Estructurada? | ¿Juicio insustituible? |
|---|---|---|---|---|
| 1 | Revisar correo | Sí | Parcial | No |
| 2 | Buscar vacantes | Sí | Sí | No |
| 3 | Aplicar a vacantes | Sí | Parcial | Parcial (cada oferta es distinta) |
| 4 | Registrar y dar seguimiento | Sí | Sí | No |
| 5 | Adaptar CV | Sí | Parcial | Sí (criterio de qué destacar) |
| 6 | Outreach a reclutador | Sí | Parcial | Sí (tono, personalización) |
| 7 | Escribir código | Sí | Parcial | Parcial (diseño sí, boilerplate no) |
| 8 | Tests unitarios | Sí | Sí | No |
| 9 | Publicar en LinkedIn | Sí | Parcial | Sí (voz personal) |
| 10 | Preparar entrevistas | No (varía mucho) | No | Sí |
| 11 | Biblioteca de prompts | Sí | Sí | No |
| 12 | Limpiar datasets | Sí | Sí | Parcial |

## 3. Matriz de priorización

| # | Tarea | Potencial IA | Impacto (horas/mes aprox.) | Prioridad |
|---|---|---|---|---|
| 4 | Registrar y dar seguimiento a aplicaciones | **Alto** | ~1 hora/mes + errores evitados | **Ahora** |
| 11 | Biblioteca de prompts | **Alto** | ~1.3 horas/mes | **Ahora** |
| 8 | Tests unitarios (boilerplate) | Alto | ~2-3 horas/mes | Después |
| 2 | Buscar y filtrar vacantes | Medio | ~2 horas/mes | Después |
| 12 | Limpiar datasets | Alto | ~3-4 horas/mes | Después |
| 6 | Outreach a reclutador | Medio (colaboración) | ~1.5 horas/mes | Después |
| 5 | Adaptar CV | Medio (colaboración) | ~1 hora/mes | Después |
| 7 | Escribir código | Medio (colaboración) | Alto, pero requiere criterio | Después |
| 1 | Revisar correo | Bajo-medio | Bajo | Después |
| 9 | Publicar en LinkedIn | Bajo (voz personal) | Bajo | No aplica |
| 3 | Aplicar a vacantes | Bajo | — | No aplica |
| 10 | Preparar entrevistas | No automatizable | — | No aplica |

## Las 2 oportunidades que pasaron a ejecución (Semanas 2 y 3)

**Semana 2 → Tarea #11 (Biblioteca de prompts):** se ejecutó en el Día 10,
documentando 10 prompts personales con pruebas de estrés.

**Semana 3 → Tarea #4 (Registro y seguimiento de aplicaciones):** se
ejecutó en los Días 11-15 — framework DECIDE, script generado y hecho
robusto con IA, criterios de delegación aplicados, y runbook documentado y
probado con una simulación de "amnesia".

Es una buena señal que, incluso reconstruyendo este diagnóstico en
retrospectiva, las dos tareas que ya elegí de forma independiente en el
Día 11 (framework DECIDE) sean exactamente las que este análisis más amplio
también señala como prioritarias. Confirma que el criterio se mantiene
consistente incluso cuando se aplica en momentos distintos.

## Ejercicio de extensión — pregunta a la IA

**Pregunta:** "Soy un profesional con background en desarrollo full stack
(Python) y ciencia de datos, actualmente en búsqueda de empleo y
construyendo evidencia práctica de portafolio. ¿Qué tareas de mi día a día
serían las mejores candidatas para automatización o asistencia con IA?"

**Comparación con mi propio análisis:** la IA sugirió adicionalmente
automatizar la comparación de descripciones de vacantes contra mi propio
perfil técnico para generar un "score de encaje" antes de decidir si
aplicar — algo que no tenía en mi lista original (tarea #2 solo contemplaba
filtrar por palabras clave, no comparar contra mi perfil). Es una
extensión razonable de la tarea #2 que vale la pena considerar para una
futura v2 del sistema.
