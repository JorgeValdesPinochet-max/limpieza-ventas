# Limpieza de dataset de ventas

Módulo de limpieza de datos de ventas para análisis exploratorio, desarrollado
como práctica de la ruta de IA (Día 4 — Principios de interacción efectiva con IA).

## Por qué existe este proyecto

Esta segunda versión corrige los puntos exactos que señaló el feedback de evaluación
sobre la primera entrega:

| Punto del feedback | Cómo se resolvió |
|---|---|
| Manejo de tipos no numéricos | La columna `monto` se convierte con `pd.to_numeric(errors="coerce")` y se distingue entre nulo real (`monto_pendiente`) y texto inválido (`monto_invalido`) |
| Zonas horarias | Fechas parseadas con `utc=True` y normalizadas a datetime naive; instantes iguales en distinta tz se reconocen como duplicados |
| Nulos | Se preservan como información de negocio, no se eliminan filas |
| Advertencias de asignación (`SettingWithCopyWarning`) | Se usa `.copy(deep=True)` al inicio y `.loc[:, col]` para toda escritura |
| Pruebas de fechas, categorías y registros | Ver `test_limpieza_ventas.py`, 10 casos de prueba específicos |

## Requisitos

- Python 3.9+
- pandas
- pytest (solo para correr los tests)

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```python
import pandas as pd
from limpieza_ventas import limpiar_dataset_ventas

df = pd.read_csv("mis_ventas.csv")
df_limpio = limpiar_dataset_ventas(df)
```

También podés ejecutar el archivo directamente para ver un ejemplo funcionando:

```bash
python3 limpieza_ventas.py
```

## Correr los tests

```bash
pytest test_limpieza_ventas.py -v
```

## Estructura del proyecto

```
limpieza-ventas/
├── limpieza_ventas.py       # Módulo principal
├── test_limpieza_ventas.py  # Suite de pruebas (10 casos)
├── requirements.txt         # Dependencias
├── .gitignore
└── README.md
```
