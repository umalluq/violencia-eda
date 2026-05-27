# Estado Actual del Proyecto

## Objetivo vigente
- Construir un pipeline reproducible de seleccion de caracteristicas para dos targets:
  - `tipo_violencia`
  - `nivel_riesgo_victima`
- Comparar dos enfoques:
  1) seleccion hibrida por consenso,
  2) MOES-RF (multiobjetivo: error vs numero de variables).

## Estado de decision (actual)
- La comparacion de entrenamiento final (mismo K, mismo split, mismos modelos baseline) favorece al subset **hibrido** sobre MOES en desempeno global.
- Decision de etapa: usar subset hibrido como referencia principal para la fase de modelado productivo.
- MOES se mantiene como contraste metodologico.

## Notebook oficial de trabajo
- `seleccion_caracteristicas_multimetodo_FULL.ipynb`

## Parametros vigentes (version actual)
- `SAMPLE_SIZE`: 50000 (editable segun RAM/estabilidad).
- Semillas recomendadas para estabilidad: `42, 52, 62`.
- MOES-RF:
  - `n_generations=10`
  - `pop_size=40`
  - `min_features=8`

## Reglas metodologicas activas
- Excluir siempre leakage directo/derivado:
  - `tipo_violencia`, `nivel_riesgo_victima`
  - `tipo_violencia_orig`, `nivel_riesgo_victima_orig`
  - columnas `*_lbl` y proxies obvios.
- Mantener auditoria de leakage previa en notebook.

## Salidas esperadas (final de notebook)
- Hibrido:
  - `ranking_cv_*.csv`
  - `ranking_mi_*.csv`
  - `ranking_rfimp_*.csv`
  - `ranking_perm_*.csv`
  - `ranking_rfe_*.csv`
  - `top30_consenso_*.csv`
- MOES:
  - `ranking_moes_*.csv`
  - `pareto_moes_*.csv`

## Interpretacion operativa rapida
- Si hibrido y MOES convergen en variables comunes, hay evidencia de robustez.
- Si difieren mucho, revisar:
  - leakage,
  - redundancia de variables,
  - sensibilidad a `random_state` y `SAMPLE_SIZE`.

## Proximo paso sugerido
- Ejecutar benchmark ampliado con metricas adicionales y escenarios de balanceo (SMOTE/SMOTETomek).
