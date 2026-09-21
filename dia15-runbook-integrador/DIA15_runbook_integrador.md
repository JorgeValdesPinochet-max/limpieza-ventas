# Día 15 — Proyecto integrador: Runbook del Tracker de Aplicaciones

Consolida el trabajo de toda la semana: la tarea Tipo A elegida con DECIDE
(Día 11), el script generado y hecho robusto con IA (Día 12), los criterios
de delegación aplicados durante su construcción (Día 13), y la decisión
informada sobre cuándo usar RAG (Día 14).

## Runbook breve

- **Propósito:** registrar cada aplicación de trabajo que envío (empresa,
  cargo, fecha, canal) y calcular automáticamente cuándo corresponde hacer
  seguimiento, para dejar de llevar esto en la cabeza y perder datos.
- **Insumos:** ninguno externo — solo los datos que yo mismo tipeo al momento
  de aplicar a un trabajo (empresa, cargo, fecha, canal). No requiere
  documentos ni Excel externos.
- **Paso 1-2-3:**
  1. Cada vez que envío una aplicación, corro
     `python tracker_v2.py --csv aplicaciones.csv agregar --empresa "X" --cargo "Y" --fecha YYYY-MM-DD --canal "Z"`.
  2. Una vez por semana (o cuando quiero revisar), corro
     `python tracker_v2.py --csv aplicaciones.csv resumen` para ver el
     estado general.
  3. Reviso `python tracker_v2.py --csv aplicaciones.csv pendientes` antes
     de empezar el día, para saber a quién debo escribirle seguimiento hoy.
- **Validación:** probado 2+ veces con datos reales (Días 11 y 12): 12 tests
  automatizados con pytest (todos en verde) más 7 pruebas manuales de casos
  de error (fecha inválida, duplicados, CSV corrupto, campos vacíos) — todas
  se comportaron como se esperaba.
- **Estado actual:** **listo para uso diario.** No es un prototipo — ya lo
  uso desde el Día 11 para mis propias aplicaciones reales.

## ¿Este proyecto necesita RAG?

**No, y esa es la decisión correcta según el criterio del Día 14.** RAG
tiene sentido cuando la respuesta depende de información que solo existe en
mis documentos (un Excel, un manual interno, un catálogo). El tracker no
consulta documentos — opera sobre datos estructurados que yo mismo ingreso
en el momento. Forzar RAG aquí sería "porque suena avanzado", no porque
agregue valor, que es exactamente el error que la lección de hoy advierte
evitar.

Donde SÍ aplicaría RAG es en la evolución natural de este sistema — ver
"Plan de evolución" más abajo.

## Documentación de uso (para mi "yo del futuro")

**Qué problema resuelve:** perder de vista a qué empresas apliqué, cuándo, y
cuándo me toca hacer seguimiento — antes lo llevaba mentalmente y se me
perdían datos.

**Cómo ejecutarlo:** (reemplaza TODO lo que está entre `< >` con tus datos
reales — no copies los ejemplos tal cual)
```bash
# Agregar una aplicación nueva
python tracker_v2.py --csv aplicaciones.csv agregar --empresa "<NOMBRE_EMPRESA>" --cargo "<NOMBRE_CARGO>" --fecha <YYYY-MM-DD> --canal <CANAL>

# Ejemplo real:
# python tracker_v2.py --csv aplicaciones.csv agregar --empresa "Acme Corp" --cargo "Data Analyst" --fecha 2026-09-20 --canal LinkedIn

# Ver resumen general
python tracker_v2.py --csv aplicaciones.csv resumen

# Ver qué necesita seguimiento hoy
python tracker_v2.py --csv aplicaciones.csv pendientes
```

**Dependencias:** Python 3.12 y la librería `pandas`. Si es la primera vez
que corres el script en una máquina nueva, instala pandas primero:
```bash
pip install pandas
```
Nada más — no requiere conexión a internet ni servicios externos para
funcionar (solo para instalar la dependencia la primera vez).

**Documentos que necesita cargar:** ninguno (no usa RAG, ver sección
anterior).

**Qué hacer si falla:**
- Si dice `Error: La fecha '...' no es válida` → revisar que la fecha esté
  en formato `YYYY-MM-DD`.
- Si dice `Ya existe una aplicación a...` → es el detector de duplicados
  funcionando; si es intencional, agregar `--permitir-duplicados`.
- Si dice `le faltan columnas requeridas` → el CSV se corrompió o se editó
  a mano incorrectamente; revisar en Excel/Notepad que tenga las 7 columnas
  originales.
- Si nada de lo anterior aplica → revisar que estoy parado en la carpeta
  correcta con `dir` antes de ejecutar el comando.

## Medición de impacto

| Métrica | Antes (manual) | Ahora (con tracker) |
|---|---|---|
| Tiempo por aplicación registrada | ~2-3 min (buscar dónde anoté, revisar si ya apliqué antes) | ~15 seg (un comando) |
| Errores de seguimiento perdido | Frecuente — sin sistema, dependía de mi memoria | Cero — el comando `pendientes` lo calcula solo |
| Frecuencia de uso | N/A (no existía) | Diaria mientras busco empleo (5-7 veces/semana) |
| Tiempo ahorrado estimado | — | ~2 min x 6 aplicaciones/semana ≈ 12 min/semana ≈ **~48 min/mes** |

El ahorro de tiempo puro es modesto, pero el valor real está en **los
errores evitados**: antes se me perdían seguimientos y probablemente perdí
oportunidades por no escribir a tiempo. Ese costo no está en la tabla porque
es difícil de cuantificar, pero es el motivo real por el que elegí esta
tarea en el Día 11 (Score 25, la más alta del framework DECIDE).

## Plan de evolución

**Para v3 (próxima mejora):**
1. **Integración con Gmail API** para detectar automáticamente correos de
   confirmación de aplicación y auto-poblar el CSV, en vez de tipear cada
   entrada manualmente. (Identificado ya desde el Día 11 como "fuera de
   alcance por ahora".)
2. **Generador de outreach con RAG:** esta es la automatización nueva donde
   SÍ aplicaría RAG. Cargaría mi CV actual + el texto de cada oferta
   específica, y le pediría a la IA que genere el mensaje de outreach
   citando coincidencias reales entre mi experiencia y los requisitos de la
   oferta (conecta directamente con el Día 13, Zona Amarilla, y el Día 14,
   caso de uso #2 que identifiqué).

**Otra tarea a automatizar:** aplicar el mismo patrón de tracker (registro +
cálculo automático de fechas) a mi seguimiento de contenido publicado en
LinkedIn — registrar qué publiqué, cuándo, y cuándo conviene volver a
publicar sobre un tema similar sin repetirme.

## Ejercicio de extensión — prueba de "amnesia" (sin colega disponible)

Sin un colega disponible esta semana, hice la prueba alternativa: en un
entorno completamente limpio, seguí mi propia documentación al pie de la
letra, como si nunca hubiera visto el código. Encontré 3 puntos ciegos
reales:

1. **Los ejemplos del comando usaban valores literales (`"Nombre"`,
   `"Puesto"`)** en vez de marcadores claros de reemplazo. Al copiar-pegar
   el comando tal cual (como haría alguien sin contexto), se registra un
   dato basura sin ningún aviso de error. **Corregido:** ahora los ejemplos
   usan `<MARCADORES>` explícitos más un ejemplo real aparte.
2. **La dependencia `pandas` se mencionaba pero nunca se explicaba cómo
   instalarla.** En un entorno realmente nuevo (sin pandas), el script
   falla con un traceback críptico (`ModuleNotFoundError`) en vez de un
   mensaje amigable. **Corregido:** se agregó el comando `pip install
   pandas` explícito en la documentación.
3. **Riesgo de encoding con tildes/ñ en Windows** (identificado desde el
   Día 14): no lo pude confirmar ni descartar en este entorno de prueba
   (Linux, que usa UTF-8 por defecto). Queda como pendiente real de
   verificar directamente en mi máquina Windows.

Esta prueba confirma exactamente lo que advierte la lección: uno no ve sus
propios puntos ciegos porque tiene el contexto completo en la cabeza. Los
dos primeros problemas eran invisibles para mí hasta que forcé la
perspectiva de "cero contexto previo".
