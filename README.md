# Proyecto: Analisis de denuncias de violencia (2020-2025)

Este repositorio contiene el flujo de trabajo para preparar, analizar y documentar una base de denuncias de violencia contra la mujer, con foco en dos targets de modelado:

- `tipo_violencia`
- `nivel_riesgo_victima`

## Objetivo

Construir una base analitica limpia en formato Parquet y un analisis estadistico reproducible que permita:

- entender la estructura y calidad de los datos,
- documentar decisiones de limpieza e imputacion,
- generar visualizaciones clave,
- iniciar una seleccion fundamentada de variables predictoras.

## Estructura principal

- `eda_denuncias.ipynb`  
  EDA de preparacion, trazabilidad de decisiones, estandarizacion de columnas, enriquecimiento ubigeo, imputacion y exportables.

- `analisis_estadistico_y_features.ipynb`  
  Analisis estadistico con graficos (crosstab, distribucion geografica, serie temporal) y ranking inicial de features por target.

- `ubigeo_trabajar.csv`  
  Maestro UBIGEO usado para construir `ubigeo_codigo` y `ubigeo_nombre`.

- `notas_targets_modelado.md`  
  Definiciones de targets y codificacion acordada para diccionario y visualizaciones.

## Definicion de targets

### 1) `tipo_violencia`

- `0`: Economica
- `1`: Psicologica
- `2`: Fisica
- `3`: Sexual

### 2) `nivel_riesgo_victima`

- `1`: Bajo
- `2`: Medio
- `3`: Alto

## Decisiones metodologicas clave

- Normalizacion de nombres de columnas (minusculas, sin acentos, con `_`).
- Enriquecimiento geografico con UBIGEO:
  - `ubigeo_codigo = dpto_domicilio + prov_domicilio + dist_domicilio`
  - cruce con `ubigeo_trabajar.csv` para `ubigeo_nombre`.
- Eliminacion de columnas con muy alta ausencia de datos (regla de `% nulos`).
- Imputacion trazable por tipo semantico de variable.
- Exclusión de registros y variables vinculadas a violencia economica para el escenario actual de modelado (muestra no representativa para esta etapa).
- Filtro de baja varianza optimizado para evitar sobrecarga de RAM.

## Salidas generadas

Dependiendo de la ejecucion de notebooks, se generan archivos como:

- `base_modelado.parquet`
- `base_modelado_particionado/`
- `reporte_variables_inicial.csv` y `.md`
- `reporte_variables_final.csv` y `.md`
- `crosstab_nivel_riesgo_x_tipo_violencia_count.csv`
- `crosstab_nivel_riesgo_x_tipo_violencia_rowpct.csv`
- `top20_departamentos_denuncias.csv`
- `top20_ubigeos_denuncias.csv`
- `serie_temporal_mensual_denuncias.csv`
- `top30_features_tipo_violencia.csv`
- `top30_features_nivel_riesgo_victima.csv`

## Requisitos

Python 3.10+ recomendado, con librerias:

```bash
pip install pandas pyarrow numpy seaborn matplotlib scipy scikit-learn
```

## Flujo recomendado

1. Ejecutar `eda_denuncias.ipynb` para preparar base y reportes.
2. Ejecutar `analisis_estadistico_y_features.ipynb` para graficos y seleccion inicial de features.
3. Revisar exportables CSV/Markdown para documentacion y ajustes.

## Siguientes pasos sugeridos

- validar leakage de variables antes de entrenar modelos,
- definir protocolo de split temporal/geografico,
- construir baseline de modelado por target,
- comparar metodos de seleccion de features con validacion cruzada.
