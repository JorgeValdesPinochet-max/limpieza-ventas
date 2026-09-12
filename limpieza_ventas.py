"""
limpieza_ventas.py

Módulo de limpieza de datos de ventas para análisis exploratorio.

Este módulo resuelve los puntos del feedback recibido en el Día 4
(Principios de interacción efectiva con IA):

    - Manejo de tipos NO numéricos en la columna 'monto'
    - Manejo de zonas horarias en la columna 'fecha'
    - Manejo de nulos como información de negocio (no como error)
    - Prevención de SettingWithCopyWarning al modificar el DataFrame
    - Normalización de la columna 'categoria'

Autor: Jorge Valdés
"""

from __future__ import annotations

import pandas as pd


# Columnas que la función espera recibir sí o sí.
# Si falta alguna, preferimos fallar rápido con un mensaje claro
# en vez de que el error aparezca más adelante en el análisis.
COLUMNAS_REQUERIDAS = {"fecha", "monto", "cliente_id", "categoria"}


def limpiar_dataset_ventas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia un DataFrame de ventas siguiendo reglas de negocio específicas.

    Reglas de negocio aplicadas:
        1. Las fechas pueden venir en formatos mixtos y con o sin zona
           horaria. Se normalizan todas a datetime "naive" en UTC.
        2. Un monto nulo significa "venta aún no registrada" (NO es un
           error) -> se marca con la columna 'monto_pendiente'.
        3. Un monto que no se puede convertir a número (ej. "N/A", "cien")
           SÍ es un error de calidad de datos -> se marca por separado
           con la columna 'monto_invalido', distinguiéndolo de un nulo real.
        4. Los duplicados exactos de (cliente_id, fecha) se eliminan,
           conservando la primera aparición.
        5. La columna 'categoria' se normaliza a minúsculas y sin espacios
           extra, para evitar que "Ropa", "ropa " y "ROPA" cuenten como
           categorías distintas en un groupby.

    Args:
        df: DataFrame original con columnas fecha, monto, cliente_id,
            categoria. No se modifica (la función siempre trabaja sobre
            una copia).

    Returns:
        Una copia limpia del DataFrame, con dos columnas nuevas:
        'monto_pendiente' (bool) y 'monto_invalido' (bool).

    Raises:
        ValueError: si al DataFrame le falta alguna columna requerida.
    """

    # --------------------------------------------------------------
    # Paso 1: Validar que estén todas las columnas necesarias.
    # Esto evita que el error aparezca 10 pasos después, en medio
    # de un análisis, sin contexto de por qué falló.
    # --------------------------------------------------------------
    columnas_faltantes = COLUMNAS_REQUERIDAS - set(df.columns)
    if columnas_faltantes:
        raise ValueError(
            f"Faltan columnas requeridas en el DataFrame: {columnas_faltantes}"
        )

    # --------------------------------------------------------------
    # Paso 2: Trabajar siempre sobre una copia profunda.
    # Esto es lo que garantiza que la función NUNCA modifique el
    # DataFrame original que el usuario le pasó (efecto secundario
    # invisible que suele causar bugs difíciles de rastrear).
    # --------------------------------------------------------------
    df_limpio = df.copy(deep=True)

    # --------------------------------------------------------------
    # Paso 3: Parsear fechas manejando formatos mixtos Y zonas horarias.
    #
    # errors="coerce"  -> si una fecha no se puede interpretar, en vez
    #                     de lanzar una excepción, la convierte en NaT
    #                     (Not a Time), para no frenar todo el pipeline
    #                     por una sola fila mala.
    # utc=True         -> si alguna fecha viene con zona horaria
    #                     (ej. "2024-01-15T10:00:00-05:00") y otras sin
    #                     zona horaria, pandas lanza un error al mezclar
    #                     tz-aware con tz-naive. Forzar utc=True convierte
    #                     todo a UTC de forma consistente.
    # format="mixed"   -> IMPORTANTE: sin esto, pandas intenta adivinar
    #                     UN SOLO formato para toda la columna a partir
    #                     de la primera fecha, y si las demás filas no
    #                     calzan con ese formato, las convierte en NaT
    #                     silenciosamente (esto es un comportamiento real
    #                     verificado en pandas al mezclar "2024-01-15",
    #                     "15/01/2024" y fechas con zona horaria en la
    #                     misma columna). format="mixed" le dice a pandas
    #                     que interprete el formato fila por fila.
    # --------------------------------------------------------------
    df_limpio["fecha"] = pd.to_datetime(
        df_limpio["fecha"], errors="coerce", utc=True, format="mixed"
    )

    # Una vez todo está en UTC, quitamos la información de zona horaria
    # para tener datetimes "naive" consistentes. Esto es una decisión de
    # diseño: para análisis exploratorio interno, es más simple comparar
    # fechas naive que arrastrar tz-aware en todo el pipeline.
    df_limpio["fecha"] = df_limpio["fecha"].dt.tz_localize(None)

    # --------------------------------------------------------------
    # Paso 4: Convertir 'monto' a numérico, distinguiendo DOS casos
    # que antes se trataban igual (y que el feedback pidió separar):
    #
    #   a) Nulo real (NaN, None, celda vacía)  -> venta pendiente de
    #      registrar. Es un estado de negocio válido.
    #   b) Texto no numérico ("N/A", "cien", "-") -> error de calidad
    #      de datos, alguien escribió algo que no es un número.
    # --------------------------------------------------------------
    monto_original = df_limpio["monto"]
    df_limpio["monto"] = pd.to_numeric(monto_original, errors="coerce")

    # Un valor es "inválido" (caso b) si originalmente NO era nulo,
    # pero después de convertir a numérico sí quedó en NaN.
    df_limpio["monto_invalido"] = (
        monto_original.notna() & df_limpio["monto"].isna()
    )

    # Un valor es "pendiente" (caso a) si quedó en NaN pero NO por ser
    # inválido, sino porque ya era nulo desde el origen.
    df_limpio["monto_pendiente"] = (
        df_limpio["monto"].isna() & ~df_limpio["monto_invalido"]
    )

    # Nota: los montos negativos (ej. reembolsos) se preservan tal cual,
    # porque en este dominio de negocio un monto negativo es un dato
    # válido, no un error. Por eso NO los tocamos en este paso.

    # --------------------------------------------------------------
    # Paso 5: Eliminar duplicados exactos de (cliente_id, fecha).
    # keep="first" conserva la primera fila que aparece y descarta
    # las repeticiones posteriores.
    # --------------------------------------------------------------
    df_limpio = df_limpio.drop_duplicates(
        subset=["cliente_id", "fecha"], keep="first"
    )

    # --------------------------------------------------------------
    # Paso 6: Normalizar la columna 'categoria'.
    #
    # Usamos .loc[:, "categoria"] en vez de df_limpio["categoria"] = ...
    # justamente para evitar el SettingWithCopyWarning que señaló el
    # feedback: pandas a veces no puede garantizar si estás modificando
    # el DataFrame real o una vista/copia temporal, y .loc es la forma
    # explícita y segura de decirle "modifica esta columna de este
    # DataFrame en particular".
    # --------------------------------------------------------------
    df_limpio.loc[:, "categoria"] = (
        df_limpio["categoria"].astype(str).str.strip().str.lower()
    )

    # --------------------------------------------------------------
    # Paso 7: Reindexar. Al eliminar duplicados quedan "huecos" en el
    # índice (ej. 0, 1, 3, 4...). Reseteamos para tener un índice limpio
    # y consecutivo, típico de un dataset listo para análisis.
    # --------------------------------------------------------------
    df_limpio = df_limpio.reset_index(drop=True)

    return df_limpio


if __name__ == "__main__":
    # --------------------------------------------------------------
    # Bloque de ejecución manual: permite correr
    #     python limpieza_ventas.py
    # y ver un ejemplo real funcionando, sin necesidad de pytest.
    # --------------------------------------------------------------
    datos_ejemplo = pd.DataFrame(
        {
            "fecha": [
                "2024-01-15",
                "15/01/2024",
                "Jan 15 2024",
                "2024-01-16T10:00:00-05:00",  # con zona horaria
                "2024-01-16T15:00:00+00:00",  # mismo instante, otra tz
                "fecha-invalida",
            ],
            "monto": [1000.0, None, "N/A", -50.0, 2500.0, 1000.0],
            "cliente_id": ["C1", "C1", "C2", "C3", "C3", "C1"],
            "categoria": ["Ropa", "ropa ", "HOGAR", "Ropa", "hogar", "Ropa"],
        }
    )

    print("Dataset original:")
    print(datos_ejemplo)
    print("\nDataset limpio:")
    print(limpiar_dataset_ventas(datos_ejemplo))
