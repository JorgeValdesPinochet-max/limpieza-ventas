"""
tracker.py
Tarea Tipo A (Framework DECIDE - Día 11): Registro y seguimiento de
aplicaciones de trabajo enviadas.

Automatiza el registro de aplicaciones a empleos y el cálculo de cuándo
corresponde hacer seguimiento (por defecto, 7 días después del envío).

Uso desde consola:
    python tracker.py agregar --empresa "Acme" --cargo "Data Analyst" \
        --fecha 2026-09-10 --canal LinkedIn

    python tracker.py resumen

    python tracker.py pendientes
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

CSV_PATH = Path(__file__).parent / "aplicaciones.csv"

COLUMNAS = [
    "empresa",
    "cargo",
    "fecha_envio",
    "canal",
    "estado",
    "fecha_seguimiento",
    "notas",
]

DIAS_PARA_SEGUIMIENTO = 7


def _dataframe_vacio() -> pd.DataFrame:
    """Crea un DataFrame vacío con las columnas correctas y tipos de fecha."""
    df = pd.DataFrame(columns=COLUMNAS)
    df["fecha_envio"] = pd.to_datetime(df["fecha_envio"])
    df["fecha_seguimiento"] = pd.to_datetime(df["fecha_seguimiento"])
    return df


def cargar_aplicaciones(csv_path: Path = CSV_PATH) -> pd.DataFrame:
    """Carga el CSV de aplicaciones. Si no existe, retorna un DataFrame vacío."""
    if not csv_path.exists():
        return _dataframe_vacio()

    df = pd.read_csv(csv_path)
    # format="mixed" por si hay fechas guardadas en formatos distintos
    df["fecha_envio"] = pd.to_datetime(df["fecha_envio"], format="mixed")
    df["fecha_seguimiento"] = pd.to_datetime(df["fecha_seguimiento"], format="mixed")
    return df


def guardar_aplicaciones(df: pd.DataFrame, csv_path: Path = CSV_PATH) -> None:
    """Guarda el DataFrame en el CSV, con fechas en formato ISO (YYYY-MM-DD)."""
    df_a_guardar = df.copy()
    df_a_guardar["fecha_envio"] = df_a_guardar["fecha_envio"].dt.strftime("%Y-%m-%d")
    df_a_guardar["fecha_seguimiento"] = df_a_guardar["fecha_seguimiento"].dt.strftime(
        "%Y-%m-%d"
    )
    df_a_guardar.to_csv(csv_path, index=False)


def calcular_fecha_seguimiento(
    fecha_envio: pd.Timestamp, dias: int = DIAS_PARA_SEGUIMIENTO
) -> pd.Timestamp:
    """Calcula la fecha de seguimiento sumando `dias` a la fecha de envío."""
    return fecha_envio + timedelta(days=dias)


def agregar_aplicacion(
    empresa: str,
    cargo: str,
    fecha_envio: str,
    canal: str,
    estado: str = "enviada",
    notas: str = "",
    csv_path: Path = CSV_PATH,
) -> pd.DataFrame:
    """
    Agrega una nueva aplicación al registro y recalcula su fecha de
    seguimiento automáticamente. Retorna el DataFrame actualizado.
    """
    df = cargar_aplicaciones(csv_path)

    fecha_envio_ts = pd.to_datetime(fecha_envio, format="mixed")
    fecha_seguimiento_ts = calcular_fecha_seguimiento(fecha_envio_ts)

    nueva_fila = pd.DataFrame(
        [
            {
                "empresa": empresa,
                "cargo": cargo,
                "fecha_envio": fecha_envio_ts,
                "canal": canal,
                "estado": estado,
                "fecha_seguimiento": fecha_seguimiento_ts,
                "notas": notas,
            }
        ]
    )

    df = pd.concat([df, nueva_fila], ignore_index=True)
    guardar_aplicaciones(df, csv_path)
    return df


def aplicaciones_pendientes_seguimiento(
    df: pd.DataFrame, hoy: pd.Timestamp | None = None
) -> pd.DataFrame:
    """
    Retorna las aplicaciones cuya fecha_seguimiento ya llegó (<= hoy) y que
    siguen en estado 'enviada' (no han sido marcadas como respondidas,
    rechazadas, etc.).
    """
    if hoy is None:
        hoy = pd.Timestamp(datetime.now().date())

    filtro = (df["fecha_seguimiento"] <= hoy) & (df["estado"] == "enviada")
    return df.loc[filtro].copy()


def resumen(csv_path: Path = CSV_PATH) -> str:
    """Genera un resumen legible del estado del tracker."""
    df = cargar_aplicaciones(csv_path)

    if df.empty:
        return "No hay aplicaciones registradas todavía."

    total = len(df)
    por_estado = df["estado"].value_counts().to_dict()
    pendientes = aplicaciones_pendientes_seguimiento(df)

    lineas = [
        f"Total de aplicaciones registradas: {total}",
        f"Por estado: {por_estado}",
        f"Aplicaciones que necesitan seguimiento HOY: {len(pendientes)}",
    ]

    if not pendientes.empty:
        lineas.append("Detalle de seguimientos pendientes:")
        for _, fila in pendientes.iterrows():
            lineas.append(
                f"  - {fila['empresa']} ({fila['cargo']}), "
                f"enviada el {fila['fecha_envio'].date()}"
            )

    return "\n".join(lineas)


def _parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tracker de aplicaciones de trabajo")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    agregar_parser = subparsers.add_parser("agregar", help="Agregar una aplicación")
    agregar_parser.add_argument("--empresa", required=True)
    agregar_parser.add_argument("--cargo", required=True)
    agregar_parser.add_argument("--fecha", required=True, help="YYYY-MM-DD")
    agregar_parser.add_argument("--canal", required=True)
    agregar_parser.add_argument("--estado", default="enviada")
    agregar_parser.add_argument("--notas", default="")

    subparsers.add_parser("resumen", help="Mostrar resumen general")
    subparsers.add_parser("pendientes", help="Mostrar seguimientos pendientes")

    return parser.parse_args()


def main() -> None:
    args = _parsear_argumentos()

    if args.comando == "agregar":
        agregar_aplicacion(
            empresa=args.empresa,
            cargo=args.cargo,
            fecha_envio=args.fecha,
            canal=args.canal,
            estado=args.estado,
            notas=args.notas,
        )
        print(f"Aplicación a '{args.empresa}' registrada correctamente.")
    elif args.comando == "resumen":
        print(resumen())
    elif args.comando == "pendientes":
        df = cargar_aplicaciones()
        pendientes = aplicaciones_pendientes_seguimiento(df)
        if pendientes.empty:
            print("No hay seguimientos pendientes hoy.")
        else:
            print(pendientes.to_string(index=False))


if __name__ == "__main__":
    main()
