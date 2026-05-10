# Resumen Ejecutivo - Proyecto de Analisis de Denuncias (2020-2025)

## Proposito

Preparar una base analitica robusta y reproducible de denuncias de violencia contra la mujer para analisis estadistico y modelado predictivo.

## Targets definidos

1. `tipo_violencia`
   - 0: Economica
   - 1: Psicologica
   - 2: Fisica
   - 3: Sexual

2. `nivel_riesgo_victima`
   - 1: Bajo
   - 2: Medio
   - 3: Alto

## Entregables principales

- Notebook de preparacion y EDA: `eda_denuncias.ipynb`
- Notebook de analisis estadistico y features: `analisis_estadistico_y_features.ipynb`
- Base final: `base_modelado.parquet`
- Reportes de variables: `.csv` y `.md`
- Tablas de crosstab, top geografico, serie temporal y top features por target

## Metodologia aplicada

- Normalizacion de nombres de columnas (formato estandar).
- Limpieza e imputacion con trazabilidad por variable.
- Enriquecimiento geografico con UBIGEO (`ubigeo_trabajar.csv`).
- Eliminacion de variables con alta ausencia y baja varianza.
- Exclusion de violencia economica para este escenario de modelado por baja representatividad en la muestra.
- Analisis estadistico con crosstab y distribuciones clave.
- Priorizacion inicial de predictores con estadistica de asociacion y Mutual Information (MI).

## Hallazgos operativos

- El flujo EDA y analitico ya corre de extremo a extremo.
- Se cuenta con base en Parquet y salidas reproducibles para iterar modelos.
- Se definio una primera lista de predictores priorizados por target.

## Proximos pasos

1. Validar leakage y ajustar set final de features.
2. Definir estrategia de particion (temporal/geografica).
3. Entrenar y evaluar modelos baseline por target.
4. Documentar resultados comparativos y versionar mejoras.
