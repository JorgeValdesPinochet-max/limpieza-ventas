"""
tracker_v2.py
Día 12 - Ejercicio de extensión: versión robusta de tracker.py (Día 11).

Mejoras sobre la v1:
  1. Manejo de errores: CSV corrupto, fechas inválidas, aplicaciones
     duplicadas (misma empresa + mismo cargo + misma fecha de envío).
  2. Resumen al terminar cada operación (qué se hizo, qué se rechazó y por qué).
  3. Parámetros configurables por línea de comandos en vez de hardcodear:
     --csv (ruta del archivo) y --dias-seguimiento (antes fijo en 7).

Uso:
    python tracker_v2.py agregar --empresa "Acme" --cargo "Data Analyst" \
        --fecha 2026-09-01 --canal LinkedIn --dias-seguimiento 5

    python tracker_v2.py resumen --csv otra_carpeta/mis_aplicaciones.csv
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

COLUMNAS = [
    "empresa",
    "cargo",
    "fecha_envio",
    "canal",
    "estado",
    "fecha_seguimiento",
    "notas",
]

DIAS_SEGUIMIENTO_DEFECTO = 7
CSV_DEFECTO = Path("aplicaciones.csv")


class ErrorTracker(Exception):
    """Errores de validación específicos del tracker (no bugs, sino datos inválidos)."""


def _dataframe_vacio() -> pd.DataFrame:
    df = pd.DataFrame(columns=COLUMNAS)
    df["fecha_envio"] = pd.to_datetime(df["fecha_envio"])
    df["fecha_seguimiento"] = pd.to_datetime(df["fecha_seguimiento"])
    return df


def cargar_aplicaciones(csv_path: Path) -> pd.DataFrame:
    """
    Carga el CSV. Si no existe, retorna vacío. Si existe pero está corrupto
    o le faltan columnas, lanza ErrorTracker con un mensaje claro en vez de
    fallar con un traceback críptico de pandas.
    """
    if not csv_path.exists():
        return _dataframe_vacio()

    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        return _dataframe_vacio()
    except pd.errors.ParserError as e:
        raise ErrorTracker(
            f"El archivo '{csv_path}' existe pero no se pudo leer como CSV "
            f"válido. ¿Se editó manualmente y se corrompió? Detalle: {e}"
        )

    columnas_faltantes = set(COLUMNAS) - set(df.columns)
    if columnas_faltantes:
        raise ErrorTracker(
            f"El archivo '{csv_path}' le faltan columnas requeridas: "
            f"{columnas_faltantes}. ¿Es el archivo correcto?"
        )

    try:
        df["fecha_envio"] = pd.to_datetime(df["fecha_envio"], format="mixed")
        df["fecha_seguimiento"] = pd.to_datetime(
            df["fecha_seguimiento"], format="mixed"
        )
    except (ValueError, TypeError) as e:
        raise ErrorTracker(
            f"El archivo '{csv_path}' tiene fechas en un formato que no se "
            f"pudo interpretar. Detalle: {e}"
        )

    return df


def guardar_aplicaciones(df: pd.DataFrame, csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df_a_guardar = df.copy()
    df_a_guardar["fecha_envio"] = df_a_guardar["fecha_envio"].dt.strftime("%Y-%m-%d")
    df_a_guardar["fecha_seguimiento"] = df_a_guardar["fecha_seguimiento"].dt.strftime(
        "%Y-%m-%d"
    )
    df_a_guardar.to_csv(csv_path, index=False)


def calcular_fecha_seguimiento(
    fecha_envio: pd.Timestamp, dias: int
) -> pd.Timestamp:
    return fecha_envio + timedelta(days=dias)


def _es_duplicada(df: pd.DataFrame, empresa: str, cargo: str, fecha_envio: pd.Timestamp) -> bool:
    if df.empty:
        return False
    filtro = (
        (df["empresa"].str.lower() == empresa.lower())
        & (df["cargo"].str.lower() == cargo.lower())
        & (df["fecha_envio"] == fecha_envio)
    )
    return filtro.any()


def agregar_aplicacion(
    empresa: str,
    cargo: str,
    fecha_envio: str,
    canal: str,
    csv_path: Path,
    dias_seguimiento: int = DIAS_SEGUIMIENTO_DEFECTO,
    estado: str = "enviada",
    notas: str = "",
    permitir_duplicados: bool = False,
) -> tuple[pd.DataFrame, str]:
    """
    Agrega una aplicación. Retorna (dataframe_actualizado, mensaje_resumen).
    Lanza ErrorTracker si la fecha es inválida o si es un duplicado no permitido.
    """
    if not empresa.strip() or not cargo.strip():
        raise ErrorTracker("El nombre de la empresa y el cargo no pueden estar vacíos.")

    try:
        fecha_envio_ts = pd.to_datetime(fecha_envio, format="mixed")
    except (ValueError, TypeError):
        raise ErrorTracker(
            f"La fecha '{fecha_envio}' no es válida. Usa formato YYYY-MM-DD "
            f"(ejemplo: 2026-09-01)."
        )

    if dias_seguimiento < 0:
        raise ErrorTracker("Los días de seguimiento no pueden ser negativos.")

    df = cargar_aplicaciones(csv_path)

    if not permitir_duplicados and _es_duplicada(df, empresa, cargo, fecha_envio_ts):
        raise ErrorTracker(
            f"Ya existe una aplicación a '{empresa}' para el cargo '{cargo}' "
            f"con fecha {fecha_envio_ts.date()}. Si es intencional (dos "
            f"procesos distintos), usa --permitir-duplicados."
        )

    fecha_seguimiento_ts = calcular_fecha_seguimiento(fecha_envio_ts, dias_seguimiento)

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

    mensaje = (
        f"Aplicación agregada: {empresa} ({cargo}). "
        f"Seguimiento programado para {fecha_seguimiento_ts.date()} "
        f"({dias_seguimiento} días después del envío). "
        f"Total de aplicaciones en el registro: {len(df)}."
    )
    return df, mensaje


def aplicaciones_pendientes_seguimiento(
    df: pd.DataFrame, hoy: pd.Timestamp | None = None
) -> pd.DataFrame:
    if hoy is None:
        hoy = pd.Timestamp(datetime.now().date())
    filtro = (df["fecha_seguimiento"] <= hoy) & (df["estado"] == "enviada")
    return df.loc[filtro].copy()


def resumen(csv_path: Path) -> str:
    df = cargar_aplicaciones(csv_path)

    if df.empty:
        return f"No hay aplicaciones registradas en '{csv_path}'."

    total = len(df)
    por_estado = df["estado"].value_counts().to_dict()
    pendientes = aplicaciones_pendientes_seguimiento(df)

    lineas = [
        f"Archivo: {csv_path}",
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
    parser = argparse.ArgumentParser(description="Tracker de aplicaciones de trabajo (v2, robusto)")
    parser.add_argument(
        "--csv",
        type=Path,
        default=CSV_DEFECTO,
        help=f"Ruta del archivo CSV (por defecto: {CSV_DEFECTO})",
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    agregar_parser = subparsers.add_parser("agregar", help="Agregar una aplicación")
    agregar_parser.add_argument("--empresa", required=True)
    agregar_parser.add_argument("--cargo", required=True)
    agregar_parser.add_argument("--fecha", required=True, help="YYYY-MM-DD")
    agregar_parser.add_argument("--canal", required=True)
    agregar_parser.add_argument("--estado", default="enviada")
    agregar_parser.add_argument("--notas", default="")
    agregar_parser.add_argument(
        "--dias-seguimiento",
        type=int,
        default=DIAS_SEGUIMIENTO_DEFECTO,
        help=f"Días hasta el seguimiento (por defecto: {DIAS_SEGUIMIENTO_DEFECTO})",
    )
    agregar_parser.add_argument(
        "--permitir-duplicados", action="store_true",
        help="Permite registrar una aplicación aunque parezca duplicada",
    )

    subparsers.add_parser("resumen", help="Mostrar resumen general")
    subparsers.add_parser("pendientes", help="Mostrar seguimientos pendientes")

    return parser.parse_args()


def main() -> None:
    args = _parsear_argumentos()

    try:
        if args.comando == "agregar":
            _, mensaje = agregar_aplicacion(
                empresa=args.empresa,
                cargo=args.cargo,
                fecha_envio=args.fecha,
                canal=args.canal,
                csv_path=args.csv,
                dias_seguimiento=args.dias_seguimiento,
                estado=args.estado,
                notas=args.notas,
                permitir_duplicados=args.permitir_duplicados,
            )
            print(mensaje)
        elif args.comando == "resumen":
            print(resumen(args.csv))
        elif args.comando == "pendientes":
            df = cargar_aplicaciones(args.csv)
            pendientes = aplicaciones_pendientes_seguimiento(df)
            if pendientes.empty:
                print("No hay seguimientos pendientes hoy.")
            else:
                print(pendientes.to_string(index=False))
    except ErrorTracker as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()