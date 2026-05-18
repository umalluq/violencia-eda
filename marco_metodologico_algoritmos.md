# Marco Metodologico de Algoritmos

Este documento consolida los algoritmos usados en la investigacion, su objetivo, su justificacion tecnica y referencias bibliograficas por seccion. Es un documento vivo: cada vez que se agregue un metodo nuevo en la tesis, se documenta aqui.

## 1) Preparacion de datos (ETL y EDA)

### 1.1 Estandarizacion y limpieza
- Normalizacion de nombres de columnas (minusculas, sin acentos, separador `_`).
- Tipado semantico: variables categoricas, numericas, codificadas y de identificacion.
- Tratamiento de nulos: imputacion por mediana (numericas) y categoria controlada (categoricas).
- Eliminacion de columnas con alta ausencia o baja utilidad analitica.
- Exclusiones de dominio definidas por criterio sustantivo (por ejemplo, categorias con baja representatividad para esta etapa).

**Sustento**
- La calidad de datos es condicion necesaria para inferencia y modelado robusto.
- Evitar inconsistencias de codificacion reduce ruido y errores de entrenamiento.

**Referencias**
- Kuhn, M., & Johnson, K. (2013). *Applied Predictive Modeling*. Springer.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer.

## 2) Ingenieria de variables

### 2.1 Enriquecimiento geografico (UBIGEO)
- Construccion de clave geografica y cruce con maestro territorial.
- Generacion de variables derivadas geograficas para analisis espacial.

### 2.2 Recodificacion de targets
- Estandarizacion a base 0 para compatibilidad con modelos multiclase (0, 1, 2).
- Conservacion opcional de columnas `*_orig` para trazabilidad (estas columnas no deben entrar al modelado por leakage).

**Sustento**
- Las variables derivadas aumentan interpretabilidad y consistencia operativa.
- La trazabilidad permite auditar decisiones de preprocesamiento.

**Referencias**
- Kuhn, M., & Johnson, K. (2013). *Applied Predictive Modeling*. Springer.

## 3) Seleccion de caracteristicas (enfoque hibrido)

En esta tesis se utiliza una bateria hibrida que combina filtros, metodos embedded y wrappers para obtener un ranking de consenso.

### 3.1 Cramer's V (filtro para categoricas)
- Calcula fuerza de asociacion entre feature categorica y target categorico.
- Se deriva de Chi-cuadrado y se normaliza a [0,1].

**Formula**
- `V = sqrt((chi2 / n) / min(r-1, k-1))`

**Por que usarlo y no solo Chi-cuadrado**
- Chi-cuadrado bruto depende del tamano muestral y de grados de libertad.
- Cramer's V normaliza y permite comparar mejor entre variables con distinta cardinalidad.

**Referencias**
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum.

### 3.2 Mutual Information (filtro)
- Mide cuanta informacion aporta cada variable sobre el target.
- Captura relaciones no lineales y no exige supuestos de linealidad.

**Referencias**
- Kraskov, A., Stoegbauer, H., & Grassberger, P. (2004). Estimating mutual information. *Physical Review E*, 69(6), 066138.

### 3.3 Random Forest Feature Importance (embedded)
- Estima importancia por reduccion media de impureza (MDI).
- Rapido para ranking inicial y util en datos mixtos.

**Referencias**
- Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5-32.

### 3.4 Permutation Importance (model-agnostic)
- Se entrena un modelo, luego se desordena una variable en test y se mide la caida del score.
- Si el score cae mucho, la variable es relevante para prediccion.

**Interpretacion simple**
- "Rompo una variable; si el modelo empeora, esa variable era importante".

**Nota de criterio**
- En presencia de variables redundantes/correlacionadas, su efecto puede verse atenuado.
- Por eso se usa como evidencia complementaria, no como unica fuente de decision.

**Referencias**
- Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5-32.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825-2830.

### 3.5 RFECV (wrapper)
- Elimina variables recursivamente y valida con CV el subconjunto optimo.
- Tiende a ser mas costoso, pero aporta seleccion mas estructural.

**Referencias**
- Guyon, I., Weston, J., Barnhill, S., & Vapnik, V. (2002). Gene selection for cancer classification using support vector machines. *Machine Learning*, 46, 389-422.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825-2830.

### 3.6 Score de consenso
- Se normaliza cada ranking a escala comun y se combina por pesos.
- Pesos actuales (ajustables):
  - Cramer's V: 0.20
  - Mutual Information: 0.25
  - RF Importance: 0.25
  - Permutation Importance: 0.20
  - RFECV: 0.10

**Sustento**
- Evita depender de un solo criterio de relevancia.
- Mejora robustez del ranking final frente a sesgos de cada metodo.

**Referencias**
- Molina, L. C., Belanche, L., & Nebot, A. (2002). Feature selection algorithms: A survey and experimental evaluation. *ICDM 2002*.

## 4) MOES-RF (busqueda evolutiva multiobjetivo)

### 4.1 Que es
- MOES (Multi-Objective Evolutionary Search) busca simultaneamente:
  1) minimizar error predictivo,
  2) minimizar numero de variables.

### 4.2 Como se implementa en esta tesis
- Se usa una aproximacion practica MOES-RF en notebook:
  - poblacion inicial de subconjuntos,
  - evaluacion por `F1_macro` (objetivo: minimizar `1 - F1`),
  - objetivo secundario: numero de features,
  - operadores evolutivos (cruce, mutacion),
  - seleccion por frente de Pareto.

### 4.3 Por que lo usamos
- Complementa la seleccion hibrida con una busqueda explicita del equilibrio precision-parsimonia.
- Permite responder: "cuantas variables necesito como minimo para mantener rendimiento competitivo".

### 4.4 Comparacion operacional MOES vs Hibrido
- Se compara Top-K de ambos enfoques por target usando:
  - interseccion de features,
  - indice de Jaccard,
  - mejor punto Pareto de MOES (`1 - obj_error`, `obj_nfeat`).
- Implementacion en script: `scripts/resumen_comparativo_features.py`.

**Resultado actual**
- `tipo_violencia`: interseccion 21/30, Jaccard 0.6774, mejor MOES F1=0.9586 con 22 variables.
- `nivel_riesgo_victima`: interseccion 12/30, Jaccard 0.3529, mejor MOES F1=0.5252 con 16 variables.

**Lectura metodologica**
- Alta convergencia en `tipo_violencia` (evidencia de estabilidad entre paradigmas).
- Convergencia moderada-baja en `nivel_riesgo_victima` (target mas complejo, posible menor senal o mayor ruido).

**Referencias**
- Deb, K. (2001). *Multi-Objective Optimization using Evolutionary Algorithms*. Wiley.
- Sarker, R. A., & Coello Coello, C. A. (2002). Evolutionary optimization. In *EOLSS*.

## 5) Metricas de evaluacion

### 5.1 F1-macro
- Promedia F1 por clase con igual peso, util para desbalance de clases.
- Evita que una clase mayoritaria domine la metrica.

### 5.2 Estabilidad del ranking
- Recomendacion operativa: repetir con varias semillas (`random_state`: 42, 52, 62).
- Consolidar promedio de score y frecuencia de aparicion en Top-K.

**Referencias**
- Kuhn, M., & Johnson, K. (2013). *Applied Predictive Modeling*. Springer.

## 6) Riesgos metodologicos y controles

### 6.1 Leakage
- Excluir siempre targets directos y derivados (`*_orig`, labels derivadas, proxies obvios).

### 6.1.1 Verificacion operativa de leakage (implementada en notebook)
- Se ejecuta una auditoria previa a la seleccion de caracteristicas para cada target.
- La auditoria marca `leakage_flag=1` cuando se cumple al menos una condicion:
  - copia exacta numerica de la columna respecto al target,
  - acuerdo directo muy alto con el target (`agreement_vs_target_str >= 0.98`),
  - nombre sospechoso (por ejemplo tokens `_orig`, `_lbl`, `tipo_violencia`, `nivel_riesgo`).
- Resultado actual de la tesis: no se detectaron columnas con `leakage_flag=1` en `tipo_violencia` ni en `nivel_riesgo_victima` bajo esta regla automatizada.

### 6.2 Alta cardinalidad categorica
- Controlar cardinalidad para evitar explosiones de tablas y sesgos en asociaciones.

### 6.3 Restricciones de RAM
- Muestreo estratificado para seleccion de variables.
- Control de `n_jobs`, downcast numerico y limpieza de memoria.

**Referencias**
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825-2830.

## 7) Criterio de inclusion/exclusion de algoritmos

Un algoritmo se mantiene en la bateria si:
- aporta informacion no redundante,
- mejora estabilidad del ranking o desempeno final,
- su costo computacional es razonable para el entorno disponible.

Un algoritmo puede bajar de peso (o retirarse) si:
- no aporta diferencia sistematica,
- introduce inestabilidad alta entre semillas,
- su costo no se justifica por ganancia de desempeno.

**Referencias**
- Molina, L. C., Belanche, L., & Nebot, A. (2002). Feature selection algorithms: A survey and experimental evaluation. *ICDM 2002*.

## 8) Bitacora de actualizacion

- Fecha: 2026-05-17
  - Se crea el documento base consolidado.
  - Se incluyen metodos actuales: Cramer's V, MI, RF importance, Permutation, RFECV, MOES-RF.
  - Se migra bibliografia: de lista final a referencias al pie de cada seccion.

## 9) Decisiones metodologicas vigentes

- Se excluyen `*_orig` y `*_lbl` de modelado para evitar fuga de informacion y sesgo en ranking.
- MOES-RF usa `min_features=8` para evitar soluciones triviales demasiado pequenas (por ejemplo, 3 variables) que no son estables metodologicamente.
- Permutation Importance se mantiene como evidencia complementaria en el consenso, no como criterio unico, por sensibilidad a redundancia entre variables.
- La estabilidad del ranking se evalua con multiples semillas (`42, 52, 62`) y consolidacion de resultados.
- La comparacion hibrido vs MOES se reporta con interseccion/Jaccard y mejor punto Pareto por target.
