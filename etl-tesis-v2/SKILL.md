---
name: etl-tesis-v2
description: "Ejecuta el pipeline ETL oficial del proyecto para integrar nueva data (ej. 2026) al parquet final, alineado al notebook eda_denuncias.ipynb."
---

# ETL-Tesis v2

Este skill aplica el mismo flujo de limpieza y transformacion definido en el EDA del proyecto.

## Que hace

- Normaliza nombres de columnas.
- Limpia nulos fantasma.
- Estandariza `nivel_riesgo_victima`.
- Construye `ubigeo_codigo` y `ubigeo_nombre` con `dpto_domicilio`, `prov_domicilio`, `dist_domicilio`.
- Crea variables temporales (`anio`, `mes`, `anio_mes`) si existe `fecha_ingreso`.
- Elimina columnas con >99% nulos.
- Imputa por tipo semantico.
- Elimina variables binarias de baja varianza.
- Excluye registros `tipo_violencia == 0` y columnas relacionadas a violencia economica.
- Alinea esquema con parquet base y concatena nuevos registros.

## Script principal

`scripts/update_parquet_pipeline.py`

## Invocacion recomendada

```bash
python scripts/update_parquet_pipeline.py   --new-csv /ruta/nueva_data_2026.csv   --ubigeo-csv /home/munasqa/MAESTRIA/opencode/ubigeo_trabajar.csv   --base-parquet /home/munasqa/MAESTRIA/opencode/base_modelado.parquet   --out-parquet /home/munasqa/MAESTRIA/opencode/base_modelado.parquet
```

## Nota

Este skill actualiza el parquet de salida indicado por `--out-parquet`. Usa una ruta distinta si deseas ejecutar pruebas sin sobreescribir el archivo final.
