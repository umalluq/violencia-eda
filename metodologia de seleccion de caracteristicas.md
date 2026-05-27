# Metodologia de Seleccion de Caracteristicas

## Objetivo
Definir un subconjunto de variables por target que sea predictivo, interpretable y metodologicamente trazable.

## Enfoques comparados

### 1) Seleccion hibrida por consenso
Se combinan cinco tecnicas:
- Cramer's V
- Mutual Information
- Random Forest Importance
- Permutation Importance
- RFECV

Cada ranking se normaliza y se integra en un score de consenso ponderado.

### 2) MOES-RF (busqueda multiobjetivo)
Se optimizan simultaneamente:
- error predictivo,
- numero de variables.

Se usa frente de Pareto para elegir soluciones no dominadas.

## Comparacion hibrido vs MOES

### Comparacion estructural (Top 30)
- `tipo_violencia`: interseccion 21/30, Jaccard 0.6774.
- `nivel_riesgo_victima`: interseccion 12/30, Jaccard 0.3529.

### Comparacion por entrenamiento final (mismo K, mismo split, mismos modelos)
Se compararon subsets en condiciones equivalentes:
- `tipo_violencia`: `K=22`
- `nivel_riesgo_victima`: `K=16`

Modelos usados en baseline: `RF`, `RL`, `MLP`.

#### Resultado principal
- En `tipo_violencia`, el subset hibrido supero al subset MOES en los tres modelos.
- En `nivel_riesgo_victima`, el mejor resultado tambien fue con subset hibrido (RF).
- En esta etapa baseline, no se evidencia superioridad global de MOES en desempeno final.

## Decision metodologica de cierre de etapa
- Se adopta el **subset hibrido** como referencia principal para la siguiente fase de modelado.
- MOES se conserva como contraste metodologico y evidencia de parsimonia/robustez.

## Archivos de evidencia
- `resumen_comparativo_features.csv`
- `detalle_interseccion_hibrido_moes.csv`
- `benchmark_moes_vs_hibrido.csv`
- `benchmark_moes_vs_hibrido_tipo_violencia.csv`
- `benchmark_moes_vs_hibrido_nivel_riesgo_victima.csv`
