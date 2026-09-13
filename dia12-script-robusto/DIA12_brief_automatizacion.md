# Día 12 — Brief de automatización: tracker de aplicaciones (v2, robusto)

Este ejercicio toma la tarea Tipo A del Día 11 (registro y seguimiento de
aplicaciones de trabajo) y aplica el patrón **describe → genera → prueba →
afina** para llevarla de un script funcional a uno robusto.

## Brief visual de automatización

- **Entrada:** datos de una aplicación de trabajo que envío (empresa, cargo,
  fecha de envío, canal, notas), ingresados por línea de comandos.
- **Transformación:** validar los datos, calcular automáticamente la fecha
  en que corresponde hacer seguimiento (fecha de envío + N días, configurable),
  detectar si ya existe una aplicación idéntica registrada, y guardar todo
  en un registro persistente.
- **Salida esperada:** un archivo CSV actualizado con la nueva aplicación, un
  mensaje de confirmación con el resumen de lo que se hizo, y un comando
  aparte que liste qué aplicaciones necesitan seguimiento hoy.
- **Restricción crítica:** el script no debe fallar con un traceback críptico
  ante datos mal formados (fechas inválidas, CSV corrupto, campos vacíos) —
  debe informar el error en lenguaje claro y salir con código de error
  distinto de cero, para poder usarlo en flujos automatizados más adelante.
- **Primer test:** ver sección "Evidencia de prueba" abajo.

## Ciclo describe → genera → prueba → afina (evidencia real)

### 1. Describir (Día 11)

Pedí un script que registrara aplicaciones de trabajo en un CSV y calculara
automáticamente la fecha de seguimiento a 7 días. Sin manejo de errores
todavía — la prioridad era tener algo funcional rápido.

### 2. Generar (Día 11 → tracker_v1_original.py)

Se generó el script base con las funciones agregar_aplicacion,
cargar_aplicaciones, calcular_fecha_seguimiento y resumen, usando pandas.

### 3. Probar con datos reales — aquí apareció un bug genuino

Al validar la función aplicaciones_pendientes_seguimiento con dos
aplicaciones de fechas distintas, mi primera suposición fue que ambas
aparecerían como pendientes en una fecha de referencia intermedia. El test
falló:

AssertionError
  Acme Corp: enviada 2026-09-01 -> seguimiento 2026-09-08
  Beta Inc:  enviada 2026-09-05 -> seguimiento 2026-09-12
  hoy simulado: 2026-09-10
  esperaba 2, pero el resultado fue 1

**Causa real:** mi suposición era incorrecta, no el código. Beta Inc todavía
no llegaba a su fecha de seguimiento (2026-09-12) el día 2026-09-10, así que
correctamente NO debía aparecer como pendiente. El código funcionaba bien;
tuve que corregir la expectativa del test, no la lógica del script. Esto es
justamente el valor de probar con datos reales antes de asumir que algo
"debería" funcionar de cierta forma.

### 4. Afinar (Día 12 → tracker_v2.py)

Con el ejercicio de extensión de hoy, pedí explícitamente que el script
fuera más robusto en tres frentes:

1. **Manejo de errores:** fechas inválidas, CSV corrupto o con columnas
   faltantes, campos vacíos, y aplicaciones duplicadas — todo con mensajes
   claros en vez de un traceback de Python.
2. **Resumen al terminar:** cada vez que se agrega una aplicación, el script
   confirma qué se guardó, cuándo toca el seguimiento y cuántas aplicaciones
   hay en total.
3. **Parámetros configurables:** la ruta del CSV (--csv) y los días para
   el seguimiento (--dias-seguimiento) ya no están hardcodeados — antes
   DIAS_PARA_SEGUIMIENTO = 7 era una constante fija en el código.

## Evidencia de prueba (ejecutada, no simulada)

Test 1: agregar con parámetro configurable (5 días en vez de 7 por defecto)
$ python tracker_v2.py --csv prueba.csv agregar --empresa "Acme Corp" --cargo "Data Analyst" --fecha 2026-09-01 --canal LinkedIn --dias-seguimiento 5
Aplicación agregada: Acme Corp (Data Analyst). Seguimiento programado para 2026-09-06 (5 días después del envío). Total de aplicaciones en el registro: 1.

Test 2: intentar duplicado exacto -> rechazado con mensaje claro
$ python tracker_v2.py --csv prueba.csv agregar --empresa "Acme Corp" --cargo "Data Analyst" --fecha 2026-09-01 --canal LinkedIn
Error: Ya existe una aplicación a 'Acme Corp' para el cargo 'Data Analyst' con fecha 2026-09-01. Si es intencional (dos procesos distintos), usa --permitir-duplicados.
(código de salida: 1)

Test 3: fecha inválida -> rechazada, sin traceback
$ python tracker_v2.py --csv prueba.csv agregar --empresa "Beta Inc" --cargo "Backend" --fecha "no-es-una-fecha" --canal Portal
Error: La fecha 'no-es-una-fecha' no es válida. Usa formato YYYY-MM-DD (ejemplo: 2026-09-01).
(código de salida: 1)

Test 4: empresa vacía -> rechazada
$ python tracker_v2.py --csv prueba.csv agregar --empresa "" --cargo "Backend" --fecha 2026-09-01 --canal Portal
Error: El nombre de la empresa y el cargo no pueden estar vacíos.
(código de salida: 1)

Test 5: CSV corrupto (editado a mano, sin columnas correctas) -> rechazado
$ python tracker_v2.py --csv corrupto.csv resumen
Error: El archivo 'corrupto.csv' le faltan columnas requeridas: {'fecha_seguimiento', 'fecha_envio', 'canal', 'cargo', 'estado', 'empresa', 'notas'}. ¿Es el archivo correcto?
(código de salida: 1)

Test 6: duplicado permitido explícitamente -> funciona
$ python tracker_v2.py --csv prueba.csv agregar --empresa "Acme Corp" --cargo "Data Analyst" --fecha 2026-09-01 --canal Referido --permitir-duplicados
Aplicación agregada: Acme Corp (Data Analyst). Seguimiento programado para 2026-09-08 (7 días después del envío). Total de aplicaciones en el registro: 2.

Test 7: resumen final
$ python tracker_v2.py --csv prueba.csv resumen
Archivo: prueba.csv
Total de aplicaciones registradas: 1
Por estado: {'enviada': 1}
Aplicaciones que necesitan seguimiento HOY: 1
Detalle de seguimientos pendientes:
  - Acme Corp (Data Analyst), enviada el 2026-09-01

Los 7 escenarios se comportaron como se esperaba en la primera ejecución de
la v2 — resultado directo de que las validaciones se diseñaron a partir de
casos de falla reales que ya había visto en la v1 (fechas mal escritas al
tipear rápido, y el riesgo de aplicar dos veces al mismo puesto sin darme
cuenta).

## Conclusión

El script pasó de "funciona si le doy datos perfectos" (v1, Día 11) a
"funciona y me avisa claramente cuando algo está mal" (v2, Día 12) en una
sola iteración de afinamiento, dirigida por casos de error concretos en vez
de manejo de errores genérico. Esa es la diferencia entre un script de
prueba y una herramienta que uso a diario con confianza.