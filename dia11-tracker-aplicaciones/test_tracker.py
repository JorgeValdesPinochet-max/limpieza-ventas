"""
test_tracker.py
Tests pytest para tracker.py (Día 11 - tarea Tipo A del framework DECIDE).

Ejecutar con:
    python -m pytest test_tracker.py -v
"""

import pandas as pd
import pytest

from tracker import (
    agregar_aplicacion,
    aplicaciones_pendientes_seguimiento,
    calcular_fecha_seguimiento,
    cargar_aplicaciones,
    resumen,
)


@pytest.fixture
def csv_temporal(tmp_path):
    """Crea una ruta de CSV temporal y aislada para cada test."""
    return tmp_path / "aplicaciones_test.csv"


def test_cargar_aplicaciones_sin_archivo_retorna_vacio(csv_temporal):
    df = cargar_aplicaciones(csv_temporal)
    assert df.empty
    assert list(df.columns) == [
        "empresa",
        "cargo",
        "fecha_envio",
        "canal",
        "estado",
        "fecha_seguimiento",
        "notas",
    ]


def test_calcular_fecha_seguimiento_suma_siete_dias():
    fecha_envio = pd.Timestamp("2026-09-01")
    resultado = calcular_fecha_seguimiento(fecha_envio)
    assert resultado == pd.Timestamp("2026-09-08")


def test_calcular_fecha_seguimiento_dias_personalizados():
    fecha_envio = pd.Timestamp("2026-09-01")
    resultado = calcular_fecha_seguimiento(fecha_envio, dias=3)
    assert resultado == pd.Timestamp("2026-09-04")


def test_agregar_aplicacion_crea_una_fila(csv_temporal):
    df = agregar_aplicacion(
        empresa="Acme Corp",
        cargo="Data Analyst",
        fecha_envio="2026-09-01",
        canal="LinkedIn",
        csv_path=csv_temporal,
    )
    assert len(df) == 1
    assert df.iloc[0]["empresa"] == "Acme Corp"


def test_agregar_aplicacion_calcula_fecha_seguimiento_automaticamente(csv_temporal):
    df = agregar_aplicacion(
        empresa="Acme Corp",
        cargo="Data Analyst",
        fecha_envio="2026-09-01",
        canal="LinkedIn",
        csv_path=csv_temporal,
    )
    assert df.iloc[0]["fecha_seguimiento"] == pd.Timestamp("2026-09-08")


def test_agregar_aplicacion_persiste_en_csv(csv_temporal):
    agregar_aplicacion(
        empresa="Acme Corp",
        cargo="Data Analyst",
        fecha_envio="2026-09-01",
        canal="LinkedIn",
        csv_path=csv_temporal,
    )
    assert csv_temporal.exists()
    df_recargado = cargar_aplicaciones(csv_temporal)
    assert len(df_recargado) == 1
    assert df_recargado.iloc[0]["empresa"] == "Acme Corp"


def test_agregar_dos_aplicaciones_acumula_filas(csv_temporal):
    agregar_aplicacion(
        empresa="Acme Corp",
        cargo="Data Analyst",
        fecha_envio="2026-09-01",
        canal="LinkedIn",
        csv_path=csv_temporal,
    )
    df = agregar_aplicacion(
        empresa="Beta Inc",
        cargo="Backend Engineer",
        fecha_envio="2026-09-05",
        canal="Portal empresa",
        csv_path=csv_temporal,
    )
    assert len(df) == 2


def test_pendientes_seguimiento_detecta_fecha_vencida(csv_temporal):
    agregar_aplicacion(
        empresa="Acme Corp",
        cargo="Data Analyst",
        fecha_envio="2026-09-01",  # seguimiento = 2026-09-08
        canal="LinkedIn",
        csv_path=csv_temporal,
    )
    df = cargar_aplicaciones(csv_temporal)
    hoy_simulado = pd.Timestamp("2026-09-10")
    pendientes = aplicaciones_pendientes_seguimiento(df, hoy=hoy_simulado)
    assert len(pendientes) == 1
    assert pendientes.iloc[0]["empresa"] == "Acme Corp"


def test_pendientes_seguimiento_ignora_fecha_futura(csv_temporal):
    agregar_aplicacion(
        empresa="Acme Corp",
        cargo="Data Analyst",
        fecha_envio="2026-09-10",  # seguimiento = 2026-09-17, aún no llega
        canal="LinkedIn",
        csv_path=csv_temporal,
    )
    df = cargar_aplicaciones(csv_temporal)
    hoy_simulado = pd.Timestamp("2026-09-11")
    pendientes = aplicaciones_pendientes_seguimiento(df, hoy=hoy_simulado)
    assert len(pendientes) == 0


def test_pendientes_seguimiento_ignora_estado_no_enviada(csv_temporal):
    agregar_aplicacion(
        empresa="Acme Corp",
        cargo="Data Analyst",
        fecha_envio="2026-09-01",
        canal="LinkedIn",
        estado="rechazada",
        csv_path=csv_temporal,
    )
    df = cargar_aplicaciones(csv_temporal)
    hoy_simulado = pd.Timestamp("2026-09-10")
    pendientes = aplicaciones_pendientes_seguimiento(df, hoy=hoy_simulado)
    assert len(pendientes) == 0


def test_resumen_sin_datos(csv_temporal):
    texto = resumen(csv_temporal)
    assert "No hay aplicaciones registradas" in texto


def test_resumen_con_datos_incluye_total(csv_temporal):
    agregar_aplicacion(
        empresa="Acme Corp",
        cargo="Data Analyst",
        fecha_envio="2026-09-01",
        canal="LinkedIn",
        csv_path=csv_temporal,
    )
    texto = resumen(csv_temporal)
    assert "Total de aplicaciones registradas: 1" in texto
