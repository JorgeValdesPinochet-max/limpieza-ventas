"""
test_limpieza_ventas.py

Suite de pruebas para limpieza_ventas.py.

Cada test está diseñado para cubrir un punto específico del feedback:

    - test_columna_faltante_lanza_error         -> validación de columnas
    - test_fechas_formatos_mixtos               -> parseo de fechas
    - test_fechas_con_zona_horaria_mixta        -> manejo de timezones
    - test_monto_nulo_se_marca_como_pendiente   -> nulos como negocio
    - test_monto_no_numerico_se_marca_invalido  -> tipos no numéricos
    - test_monto_negativo_se_preserva           -> valores negativos válidos
    - test_duplicados_por_cliente_y_fecha       -> deduplicación
    - test_categoria_se_normaliza               -> normalización de texto
    - test_no_modifica_dataframe_original       -> ausencia de efectos secundarios
    - test_no_genera_warnings_de_asignacion     -> SettingWithCopyWarning
"""

import warnings

import pandas as pd
import pytest

from limpieza_ventas import limpiar_dataset_ventas


@pytest.fixture
def dataset_base() -> pd.DataFrame:
    """
    Fixture reutilizable: un DataFrame de ventas "crudo" con todos los
    problemas típicos que la función debe resolver.
    """
    return pd.DataFrame(
        {
            "fecha": [
                "2024-01-15",               # formato ISO
                "15/01/2024",               # formato día/mes/año
                "Jan 15 2024",              # formato texto en inglés
                "2024-01-16T10:00:00-05:00",  # con zona horaria (UTC-5)
                "2024-01-16T15:00:00+00:00",  # mismo instante, en UTC
            ],
            "monto": [1000.0, None, "N/A", -50.0, 2500.0],
            "cliente_id": ["C1", "C2", "C3", "C4", "C4"],
            "categoria": ["Ropa", "ropa ", "HOGAR", "Hogar", "hogar"],
        }
    )


def test_columna_faltante_lanza_error():
    """Si falta una columna requerida, debe fallar rápido y con mensaje claro."""
    df_incompleto = pd.DataFrame({"fecha": ["2024-01-15"], "monto": [100]})

    with pytest.raises(ValueError, match="Faltan columnas requeridas"):
        limpiar_dataset_ventas(df_incompleto)


def test_fechas_formatos_mixtos(dataset_base):
    """Las fechas en distintos formatos deben parsearse todas correctamente."""
    resultado = limpiar_dataset_ventas(dataset_base)

    # Las primeras tres filas deben quedar como datetime válido, no NaT.
    assert resultado.loc[0, "fecha"] == pd.Timestamp("2024-01-15")
    assert resultado.loc[1, "fecha"] == pd.Timestamp("2024-01-15")
    assert resultado.loc[2, "fecha"] == pd.Timestamp("2024-01-15")


def test_fechas_con_zona_horaria_mixta():
    """
    Dos fechas que representan el MISMO instante en distinta zona horaria
    deben terminar siendo iguales una vez normalizadas.

    Nota: usamos cliente_id DISTINTOS a propósito. Si usáramos el mismo
    cliente_id para ambas filas, drop_duplicates() las colapsaría en una
    sola ANTES de que pudiéramos comparar las dos fechas normalizadas
    (justamente el bug que este test tenía en su primera versión).
    """
    df = pd.DataFrame(
        {
            "fecha": [
                "2024-01-16T10:00:00-05:00",  # UTC-5
                "2024-01-16T15:00:00+00:00",  # mismo instante, en UTC
            ],
            "monto": [100.0, 200.0],
            "cliente_id": ["C_A", "C_B"],  # distintos, para que no se deduplique
            "categoria": ["ropa", "ropa"],
        }
    )
    resultado = limpiar_dataset_ventas(df)

    fecha_utc_menos_5 = resultado.loc[resultado["cliente_id"] == "C_A", "fecha"].iloc[0]
    fecha_utc = resultado.loc[resultado["cliente_id"] == "C_B", "fecha"].iloc[0]

    # "2024-01-16T10:00:00-05:00" es exactamente "2024-01-16T15:00:00+00:00"
    assert fecha_utc_menos_5 == fecha_utc

    # Además, el resultado no debe tener información de tz adjunta
    # (deben ser datetimes "naive").
    assert resultado["fecha"].dt.tz is None


def test_monto_nulo_se_marca_como_pendiente(dataset_base):
    """Un monto nulo es una venta pendiente de registrar, no un error."""
    resultado = limpiar_dataset_ventas(dataset_base)

    fila_nula = resultado[resultado["cliente_id"] == "C2"].iloc[0]
    assert fila_nula["monto_pendiente"] is True or fila_nula["monto_pendiente"] == True
    assert fila_nula["monto_invalido"] == False


def test_monto_no_numerico_se_marca_invalido(dataset_base):
    """Un monto tipo texto ('N/A') es un error de calidad, distinto de un nulo."""
    resultado = limpiar_dataset_ventas(dataset_base)

    fila_invalida = resultado[resultado["cliente_id"] == "C3"].iloc[0]
    assert fila_invalida["monto_invalido"] == True
    assert fila_invalida["monto_pendiente"] == False


def test_monto_negativo_se_preserva(dataset_base):
    """Un monto negativo (ej. reembolso) es un dato válido y debe conservarse."""
    resultado = limpiar_dataset_ventas(dataset_base)

    fila_negativa = resultado[resultado["cliente_id"] == "C4"].iloc[0]
    assert fila_negativa["monto"] == -50.0
    assert fila_negativa["monto_invalido"] == False
    assert fila_negativa["monto_pendiente"] == False


def test_duplicados_por_cliente_y_fecha():
    """Debe eliminar solo duplicados EXACTOS de (cliente_id, fecha)."""
    df = pd.DataFrame(
        {
            "fecha": ["2024-01-15", "2024-01-15", "2024-01-16"],
            "monto": [100.0, 999.0, 200.0],  # misma fecha+cliente, distinto monto
            "cliente_id": ["C1", "C1", "C1"],
            "categoria": ["ropa", "ropa", "ropa"],
        }
    )
    resultado = limpiar_dataset_ventas(df)

    # Debe quedar solo 2 filas: la duplicada se elimina conservando la primera.
    assert len(resultado) == 2
    assert resultado.loc[0, "monto"] == 100.0  # se conservó la primera aparición


def test_categoria_se_normaliza(dataset_base):
    """Todas las variantes de 'Hogar' deben terminar como 'hogar'."""
    resultado = limpiar_dataset_ventas(dataset_base)

    categorias_hogar = resultado[resultado["cliente_id"].isin(["C3", "C4"])]
    assert (categorias_hogar["categoria"] == "hogar").all()


def test_no_modifica_dataframe_original(dataset_base):
    """La función nunca debe mutar el DataFrame que recibió como argumento."""
    columnas_antes = list(dataset_base.columns)
    valores_antes = dataset_base.copy()

    limpiar_dataset_ventas(dataset_base)

    # El DataFrame original debe seguir intacto: mismas columnas, mismos valores.
    assert list(dataset_base.columns) == columnas_antes
    pd.testing.assert_frame_equal(dataset_base, valores_antes)


def test_no_genera_warnings_de_asignacion(dataset_base):
    """
    La función no debe generar SettingWithCopyWarning, que es el warning
    clásico de pandas cuando no queda claro si se está modificando una
    copia o el DataFrame real.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", pd.errors.SettingWithCopyWarning)
        # Si aparece el warning, este simplefilter lo convierte en excepción
        # y el test fallará, dejando en evidencia el problema.
        limpiar_dataset_ventas(dataset_base)
