# Resumen Ejecutivo - Proyecto de Analisis de Denuncias (2020-2025)

## Proposito

Preparar una base analitica robusta y reproducible de denuncias de violencia contra la mujer para analisis estadistico y modelado predictivo.

## Targets definidos

1. `tipo_violencia`
   - 0: Psicologica
   - 1: Fisica
   - 2: Sexual

2. `nivel_riesgo_victima`
   - 0: Bajo
   - 1: Medio
   - 2: Alto

## Entregables principales

- Notebook de preparacion y EDA: `eda_denuncias.ipynb`
- Notebook de analisis estadistico y features: `analisis_estadistico_y_features.ipynb`
- Notebook de seleccion de caracteristicas (flujo oficial): `seleccion_caracteristicas_multimetodo_FULL.ipynb`
- Base final: `base_modelado.parquet`
- Reportes de variables: `.csv` y `.md`
- Tablas de crosstab, top geografico, serie temporal y top features por target
- Resultados de comparacion hibrido vs MOES:
  - `resumen_comparativo_features.csv`
  - `detalle_interseccion_hibrido_moes.csv`

## Metodologia aplicada

- Normalizacion de nombres de columnas (formato estandar).
- Limpieza e imputacion con trazabilidad por variable.
- Enriquecimiento geografico con UBIGEO (`ubigeo_trabajar.csv`).
- Eliminacion de variables con alta ausencia y baja varianza.
- Exclusion de violencia economica para este escenario de modelado por baja representatividad en la muestra.
- Analisis estadistico con crosstab y distribuciones clave.
- Seleccion hibrida de variables (Cramer's V, MI, RF, Permutation, RFECV) con score de consenso.
- Seleccion evolutiva multiobjetivo MOES-RF para comparar error vs numero de variables.
- Auditoria automatizada de leakage antes de modelado.
- Entrenamiento final por target (ejecucion separada para estabilidad): RF, RL, MCP/MLP, XGB, CatBoost.

## Hallazgos operativos

- El flujo EDA, seleccion y comparacion hibrido-vs-MOES corre de extremo a extremo.
- `tipo_violencia` muestra alta convergencia entre metodos (interseccion 21/30, Jaccard 0.6774).
- `nivel_riesgo_victima` muestra convergencia menor (interseccion 12/30, Jaccard 0.3529), indicando mayor complejidad del target.
- No se detecto leakage_flag=1 en la verificacion automatizada vigente.

## Proximos pasos

1. Ampliar benchmark con metricas adicionales por modelo (ademas de F1-macro).
2. Evaluar escenarios de remuestreo (SMOTE/SMOTETomek) por target.
3. Consolidar subset final de variables con estabilidad por semillas (42/52/62).
4. Cerrar comparacion final de modelos y documentar decision metodologica.
