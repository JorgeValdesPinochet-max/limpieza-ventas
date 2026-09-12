# Mi biblioteca de prompts — Jorge Valdés

Sistema vivo de prompts optimizados para mis tareas reales como profesional
full stack + Python + ciencia de datos, en proceso de búsqueda de empleo.

Cada entrada sigue la plantilla del Día 10: Nombre, Propósito, Categoría,
Prompt, Notas de uso, Historial de refinamiento.

---

## 1. Limpieza de datasets con reglas de negocio explícitas

**PROPÓSITO:** Generar funciones de limpieza de datos en pandas que
distingan errores de calidad de datos vs. información de negocio válida
(nulos intencionales), y que manejen formatos mixtos sin fallar en
silencio.

**CATEGORÍA:** Análisis

**PROMPT:**
```
ROL: Eres un ingeniero de datos senior especializado en pandas y pipelines
de limpieza de datos para análisis exploratorio.

CONTEXTO: Tengo un dataset con la columna [NOMBRE_COLUMNA_FECHA] que puede
venir en MÚLTIPLES formatos dentro de la misma columna (ISO, día/mes/año,
texto, con o sin zona horaria), y la columna [NOMBRE_COLUMNA_MONTO] donde
un valor nulo significa [DEFINIR: ej. "pendiente de registrar", NO un error].

INSTRUCCIÓN: Escribe una función que: (1) parsee fechas de formatos mixtos
usando pd.to_datetime con format="mixed" y utc=True (NUNCA asumas un solo
formato para toda la columna), (2) distinga entre nulo real y texto no
numérico usando pd.to_numeric(errors="coerce") comparado contra el valor
original, (3) [otras reglas específicas del dataset].

FORMATO: Código Python con type hints, docstring explicando cada paso, y
comentarios inline solo donde la lógica no sea obvia.

RESTRICCIÓN: Usa .copy(deep=True) al inicio y .loc[:, col] para cualquier
asignación, para evitar SettingWithCopyWarning. La función nunca debe
modificar el DataFrame original.
```

**NOTAS DE USO:** Uso este prompt cada vez que empiezo un EDA con datos
nuevos. Antes de pedir el código, ejecuto `df.dtypes` y `df["fecha"].head(10)`
para identificar los formatos reales presentes y así completar el CONTEXTO
con ejemplos concretos, no genéricos.

**HISTORIAL DE REFINAMIENTO:**
- v1: No especificaba `format="mixed"`. Pandas asumía un solo formato de
  fecha para toda la columna a partir de la primera fila, y convertía en
  NaT silenciosamente todas las fechas con formato distinto — un bug real
  que encontré ejecutando el código, no leyéndolo.
- v2: Se agregó la restricción explícita de `format="mixed"` y la
  distinción nulo vs. inválido en INSTRUCCIÓN. Verificado con 10 tests
  pytest, incluyendo fechas con zona horaria mixta.

---

## 2. Comentarios de revisión de código para desarrolladores junior

**PROPÓSITO:** Generar feedback técnico de code review que sea preciso y
accionable, pero que no desmotive a un desarrollador con poca experiencia.

**CATEGORÍA:** Comunicación

**PROMPT:**
```
ROL: Eres un ingeniero de software senior especializado en [LENGUAJE/STACK],
con experiencia mentoreando desarrolladores junior en un equipo ágil.

CONTEXTO: Estoy revisando el PR de un compañero junior. El código tiene
estos problemas específicos: [LISTAR PROBLEMAS REALES DEL CÓDIGO, ej.
"no maneja nulos", "loop donde vectorizado sería mejor", "sin type hints"].
Es su [N]-avo PR y quiero que mejore sin sentirse desmotivado.

INSTRUCCIÓN: Redacta un comentario por cada problema detectado. Cada uno
debe explicar el problema técnico, por qué importa (impacto real, no
genérico), y sugerir la corrección con código de ejemplo.

FORMATO: "🔍 Problema: ... / 💡 Por qué importa: ... / ✅ Sugerencia: [código]"

TONO Y RESTRICCIÓN: Constructivo, nunca condescendiente. No uses frases
como "esto está mal". Empieza reconociendo algo positivo del PR.
```

**NOTAS DE USO:** Funciona mejor cuando pego el código real del PR en el
CONTEXTO en vez de describir los problemas en abstracto — la IA detecta
matices que yo podría pasar por alto (ej. una variable mal nombrada que
además oculta un bug).

**HISTORIAL DE REFINAMIENTO:**
- v1: Sin el componente de CONTEXTO con problemas específicos, la IA
  generaba comentarios genéricos tipo "revisa el manejo de errores" — no
  accionables.
- v2: Al agregar los problemas reales y el nivel de experiencia del
  destinatario, los comentarios pasaron a ser directamente copiables al PR.

---

## 3. Generación de tests pytest con casos borde de negocio

**PROPÓSITO:** Generar suites de tests que cubran las reglas de negocio
reales de una función, no solo el camino feliz.

**CATEGORÍA:** Creación

**PROMPT:**
```
ROL: Eres un ingeniero de QA especializado en testing de [DOMINIO] con pytest.

CONTEXTO: Esta función hace [DESCRIPCIÓN]. Las reglas de negocio críticas
son: [LISTAR, ej. "un monto nulo es válido y no debe eliminarse", "fechas
con distinta zona horaria que representan el mismo instante son duplicados"].

INSTRUCCIÓN: Escribe tests con pytest que cubran cada regla de negocio
listada arriba, más: que la función no modifique el objeto/DataFrame
original, y al menos un caso de columna faltante o input inválido.

FORMATO: Un archivo test_[nombre].py con nombres de test descriptivos
(test_que_describe_el_comportamiento_esperado) y fixtures reutilizables.

RESTRICCIÓN: Si dos filas de prueba deben comparar el mismo resultado
esperado, usa identificadores DISTINTOS entre ellas para evitar que la
propia lógica de deduplicación de la función colapse los casos de prueba
antes de poder compararlos.
```

**NOTAS DE USO:** La restricción final la agregué después de un error real:
un test mío usaba el mismo `cliente_id` para dos filas que quería comparar,
y la deduplicación de mi propia función las colapsaba antes de que pudiera
verificar nada.

**HISTORIAL DE REFINAMIENTO:**
- v1: Sin la restricción de identificadores distintos, generé un test que
  fallaba con `KeyError` por una razón no relacionada con el bug que
  quería probar (falso positivo de fallo).
- v2: Con la restricción explícita, el test aisla correctamente lo que
  se quiere verificar.

---

## 4. Explicar un modelo o resultado de análisis a un stakeholder no técnico

**PROPÓSITO:** Traducir hallazgos técnicos de un modelo de ML o análisis
de datos a lenguaje comprensible para alguien sin background técnico,
sin perder precisión.

**CATEGORÍA:** Comunicación

**PROMPT:**
```
ROL: Eres un data scientist senior que se especializa en comunicar
resultados técnicos a audiencias de negocio.

CONTEXTO: Construí un modelo de [TIPO] que predice [QUÉ]. Los resultados
clave son: [MÉTRICAS REALES]. La audiencia es [ej. "el gerente comercial,
sin conocimiento técnico, que decide si el modelo se usa en producción"].

INSTRUCCIÓN: Explica: (1) qué hace el modelo en una analogía cotidiana,
(2) qué tan confiable es sin usar jerga estadística (traduce
precision/recall a impacto de negocio concreto), (3) qué limitaciones
tiene y en qué casos podría fallar, (4) una recomendación clara de
siguiente paso.

FORMATO: Máximo 4 párrafos cortos, sin fórmulas ni jerga técnica.

RESTRICCIÓN: No uses las palabras "modelo", "algoritmo" ni "precisión"
más de una vez cada una. No minimices las limitaciones para que suene
mejor de lo que es.
```

**NOTAS DE USO:** Uso esto antes de reuniones con stakeholders no técnicos.
Reviso siempre el resultado para no sobre-simplificar al punto de ser
engañoso — es una traducción, no una promesa de perfección.

**HISTORIAL DE REFINAMIENTO:**
- v1: Sin la restricción de no minimizar limitaciones, el output sonaba
  demasiado optimista sobre el modelo.
- v2: Agregar esa restricción produjo explicaciones más honestas y
  balanceadas.

---

## 5. Preparación para entrevista técnica de Data Science

**PROPÓSITO:** Generar preguntas de práctica y puntos de repaso
personalizados según la oferta de trabajo específica a la que postulo.

**CATEGORÍA:** Planificación

**PROMPT:**
```
ROL: Eres un entrevistador técnico senior de Data Science con experiencia
contratando para roles [JUNIOR/SEMI-SENIOR] en [TIPO DE EMPRESA].

CONTEXTO: Voy a entrevistarme para un puesto que requiere: [PEGAR REQUISITOS
DE LA OFERTA REAL]. Mi experiencia actual es: [RESUMEN BREVE DE TU PERFIL].

INSTRUCCIÓN: Identifica las 5 brechas más probables entre mi perfil y los
requisitos del puesto. Para cada una, genera 2 preguntas de entrevista
típicas que probarían esa brecha, y una guía de qué debería repasar para
responderlas bien.

FORMATO: Tabla con columnas: Brecha | Pregunta típica | Qué repasar.

RESTRICCIÓN: No inventes tecnologías que no aparecen en la oferta. Prioriza
brechas reales sobre preguntas genéricas de "cultura fit".
```

**NOTAS DE USO:** Repito este prompt para cada postulación distinta,
pegando la oferta real — es lo que hace que las preguntas generadas sean
específicas y no genéricas de "preguntas de entrevista de Data Science".

**HISTORIAL DE REFINAMIENTO:**
- v1 (pendiente de probar en una entrevista real — actualizaré con
  resultado).

---

## 6. Priorización de backlog cuando compiten features y deuda técnica

**PROPÓSITO:** Tomar una lista desordenada de tareas pendientes (features,
bugs, refactors) y priorizarla con un criterio explícito, no solo por
urgencia percibida.

**CATEGORÍA:** Planificación

**PROMPT:**
```
ROL: Eres un tech lead con experiencia balanceando entrega de features
contra deuda técnica en equipos pequeños.

CONTEXTO: Este es mi backlog actual: [LISTAR TAREAS]. El objetivo del
trimestre es [OBJETIVO DE NEGOCIO]. El equipo tiene [N] desarrolladores.

INSTRUCCIÓN: Prioriza las tareas usando un criterio de impacto en el
objetivo del trimestre vs. esfuerzo estimado. Marca cualquier tarea de
deuda técnica que, si no se hace ahora, probablemente bloquee una feature
futura.

FORMATO: Tabla: Tarea | Impacto (Alto/Medio/Bajo) | Esfuerzo (Alto/Medio/Bajo)
| Prioridad | Justificación en una frase.

RESTRICCIÓN: No pongas más de 2 tareas en "Prioridad Alta" — fuerza una
decisión real, no una lista donde todo es urgente.
```

**NOTAS DE USO:** La restricción de "máximo 2 en Alta" es la parte más
útil — sin eso, la IA (como yo mismo bajo presión) tiende a marcar casi
todo como urgente, lo cual no ayuda a decidir.

**HISTORIAL DE REFINAMIENTO:**
- v1: Sin el límite de tareas en prioridad Alta, el resultado no era
  accionable (8 de 10 tareas "urgentes").
- v2: Con el límite explícito, la priorización fuerza trade-offs reales.

---

## 7. Mensaje de networking en LinkedIn para búsqueda de empleo

**PROPÓSITO:** Redactar mensajes de contacto en frío que generen respuesta,
personalizados según el rol y la persona, sin sonar genérico ni
desesperado.

**CATEGORÍA:** Comunicación

**PROMPT:**
```
ROL: Eres un profesional de reclutamiento tech que sabe qué mensajes de
LinkedIn generan respuesta y cuáles se ignoran.

DESTINATARIO: [Rol de la persona, ej. "Data Science Lead en una fintech"].
No lo conozco personalmente.

SITUACIÓN: Estoy buscando trabajo como [TU PERFIL]. Vi que la empresa
[NOMBRE] tiene una posición abierta de [ROL] / o vi que esta persona
publicó sobre [TEMA ESPECÍFICO].

OBJETIVO: Generar una respuesta o una llamada de 15 minutos, no pedir
trabajo directamente en el primer mensaje.

TONO: Directo, breve, sin lenguaje de venta ("me encantaría formar parte
de su equipo") ni jerga corporativa vacía.

RESTRICCIÓN: Máximo 500 caracteres (límite real de LinkedIn para mensajes
de conexión). No uses signos de exclamación. No menciones "apasionado"
ni "motivado".
```

**NOTAS DE USO:** Cambio siempre el SITUACIÓN con algo específico y
verificable de la persona o empresa (un post reciente, un proyecto
público) — mensajes genéricos tienen tasa de respuesta mucho más baja.

**HISTORIAL DE REFINAMIENTO:**
- v1: Sin la restricción de caracteres y palabras prohibidas, los mensajes
  sonaban a plantilla de LinkedIn genérica.
- v2: Con las restricciones, el tono se volvió más humano y específico.

---

## 8. Análisis exploratorio de datos (EDA) con narrativa para no técnicos

**PROPÓSITO:** Generar un EDA que no sea solo código y gráficos, sino que
incluya una narrativa de negocio interpretando los hallazgos.

**CATEGORÍA:** Análisis

**PROMPT:**
```
ROL: Eres un data scientist senior haciendo un análisis exploratorio para
presentar a un equipo de negocio.

CONTEXTO: Tengo un dataset de [DESCRIPCIÓN]. Las preguntas de negocio que
me interesa responder son: [LISTAR 2-3 PREGUNTAS REALES].

INSTRUCCIÓN: Para cada pregunta, indica qué análisis estadístico o
visualización usarías (piensa paso a paso: primero qué variable(s)
involucra, luego qué tipo de relación buscas, luego qué gráfico o test
es apropiado), y qué patrón esperarías ver si la hipótesis de negocio es
cierta vs. si no lo es.

FORMATO: Una sección por pregunta, con el análisis técnico y luego 2-3
frases de "qué significaría esto para el negocio".

RESTRICCIÓN: No asumas causalidad de correlaciones. Señala explícitamente
cuándo un hallazgo es solo correlacional.
```

**NOTAS DE USO:** El "piensa paso a paso" (chain-of-thought) es clave acá
— sin eso, la IA salta directo a sugerir gráficos sin justificar por qué
esa visualización responde la pregunta de negocio.

**HISTORIAL DE REFINAMIENTO:**
- v1 (zero-shot, sin "piensa paso a paso"): sugerencias de gráficos
  genéricas, no conectadas a las preguntas de negocio específicas.
- v2 (con chain-of-thought explícito): el razonamiento intermedio mejoró
  la relevancia de las sugerencias — cambiar la técnica funcionó mejor
  que solo agregar más contexto.

---

## 9. Documentación técnica de una función o módulo para el equipo

**PROPÓSITO:** Generar documentación técnica (docstrings + README de
módulo) a partir de código ya escrito, consistente con el resto del
proyecto.

**CATEGORÍA:** Creación

**PROMPT:**
```
ROL: Eres un ingeniero de software que documenta código para que otros
desarrolladores del equipo lo entiendan sin preguntarte directamente.

CONTEXTO: Este es el código: [PEGAR CÓDIGO REAL]. El equipo usa el
formato de docstring [Google/NumPy/reST — especificar cuál].

INSTRUCCIÓN: Genera: (1) un docstring completo para cada función pública,
(2) una sección de README explicando el propósito del módulo, cómo
instalarlo/usarlo, y un ejemplo ejecutable, (3) advertencias sobre
efectos secundarios o supuestos no obvios del código.

FORMATO: Docstrings en el mismo archivo de código; README en Markdown
separado.

RESTRICCIÓN: No documentes lo obvio (ej. no digas "esta función suma dos
números" si el nombre y los parámetros ya lo dicen). Enfócate en el
"por qué" de decisiones no evidentes en el código.
```

**NOTAS DE USO:** Pego siempre el código real, nunca describo la función
de memoria — la IA detecta comportamientos (como manejo de excepciones)
que yo olvido mencionar.

**HISTORIAL DE REFINAMIENTO:**
- v1 (pendiente de refinar con un caso real).

---

## 10. Email de seguimiento post-entrevista técnica

**PROPÓSITO:** Redactar un email de agradecimiento/seguimiento después de
una entrevista técnica que refuerce puntos específicos sin sonar
desesperado.

**CATEGORÍA:** Comunicación

**PROMPT:**
```
ROL: Eres un profesional de carrera tech que ayuda a candidatos a redactar
comunicación post-entrevista efectiva.

DESTINATARIO: [Nombre/rol del entrevistador]. La entrevista fue [técnica /
cultural / con el hiring manager].

SITUACIÓN: En la entrevista discutimos [1-2 TEMAS ESPECÍFICOS REALES,
ej. "el manejo de datos faltantes en un pipeline de ML", "mi experiencia
con FastAPI"]. Sentí que [algo que quiero reforzar o aclarar, si aplica].

OBJETIVO: Agradecer, reforzar un punto específico de la conversación
(no genérico), y reiterar interés sin sonar ansioso.

TONO: Profesional, breve, cálido pero no informal.

RESTRICCIÓN: Máximo 150 palabras. No repitas el currículum. No uses
"espero tener noticias pronto" ni frases de relleno similares.
```

**NOTAS DE USO:** Lo envío siempre dentro de las 24 horas posteriores a
la entrevista. El componente de SITUACIÓN con un tema específico discutido
es lo que distingue esto de un email genérico de agradecimiento.

**HISTORIAL DE REFINAMIENTO:**
- v1 (pendiente de refinar con resultado real de una entrevista).
