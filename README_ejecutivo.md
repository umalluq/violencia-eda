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
- Entrenamiento final por target (ejecucion separada para estabilidad): RF, RL, MLP, XGB, CatBoost.

## Hallazgos operativos

- El flujo EDA, seleccion y comparacion hibrido-vs-MOES corre de extremo a extremo.
- `tipo_violencia` muestra alta convergencia entre metodos (interseccion 21/30, Jaccard 0.6774).
- `nivel_riesgo_victima` muestra convergencia menor (interseccion 12/30, Jaccard 0.3529), indicando mayor complejidad del target.
- No se detecto leakage_flag=1 en la verificacion automatizada vigente.

## Resultados: benchmark MOES vs Hibrido (mismo K y mismo protocolo)

Se realizo una comparacion directa y justa entre los subconjuntos de variables seleccionados por MOES y por el enfoque hibrido, manteniendo:
- mismo numero de variables por target (`K=22` en `tipo_violencia`, `K=16` en `nivel_riesgo_victima`),
- mismo split y tamano de entrenamiento (`n_train=96000`, `n_test=24000`),
- mismos modelos (`RF`, `RL`, `MLP`) en escenario baseline.

### `tipo_violencia`
- Hibrido obtuvo mejor desempeno en los tres modelos:
  - `RL`: `F1-macro=0.9700`
  - `MLP`: `F1-macro=0.9694`
  - `RF`: `F1-macro=0.9687`
- MOES quedo por debajo en todos los casos:
  - `MLP`: `0.9630`
  - `RL`: `0.9621`
  - `RF`: `0.9615`

### `nivel_riesgo_victima`
- El target mantiene mayor complejidad y menor desempeno global.
- Mejor resultado: `RF` con subset hibrido (`F1-macro=0.5304`) vs `RF` con subset MOES (`0.5217`).
- MOES solo supera levemente en `RL` (`0.3652` vs `0.3626`), ambos con rendimiento bajo.

### Decision metodologica de cierre de etapa
- En esta corrida baseline, no se confirma superioridad de MOES en desempeno final.
- Se prioriza el **subset hibrido** como referencia principal para la siguiente fase de modelado y despliegue.
- MOES se mantiene como contraste metodologico y validacion de estabilidad/parsimonia.

### Nota de balanceo de clases
- Se incorporo bloque de validacion focalizada de balanceo para `RF` (`baseline`, `SMOTE`, `SMOTETomek`) en el notebook final.
- En la corrida registrada actual se dispone de baseline consolidado; la comparacion completa con remuestreo queda como siguiente validacion operativa segun disponibilidad de entorno/dependencias.

## Proximos pasos

1. Ampliar benchmark con metricas adicionales por modelo (ademas de F1-macro).
2. Evaluar escenarios de remuestreo (SMOTE/SMOTETomek) por target.
3. Consolidar subset final de variables con estabilidad por semillas (42/52/62).
4. Cerrar comparacion final de modelos y documentar decision metodologica.
