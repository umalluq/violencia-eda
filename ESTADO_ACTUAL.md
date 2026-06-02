# Estado Actual del Proyecto - Etapa de Modelado y Balanceo

## Objetivo Vigente
- Construir y validar un pipeline predictivo reproducible y con sólido sustento metodológico para dos targets de la tesis:
  - `tipo_violencia` (Psicológica, Física, Sexual)
  - `nivel_riesgo_victima` (Bajo, Medio, Alto)

## Estado de Decisiones Metodológicas (Cierre de Fases 1 y 2)

### 1) Selección de Características Híbrida como Estándar
- Tras el benchmark comparativo contra MOES, se ratifica al **Top 30 Híbrido por Consenso** como el subconjunto de referencia del proyecto por su consistencia predictiva y estabilidad estructural superior en todos los clasificadores.

### 2) Estrategia de Reducción Dimensional Excepcional
- Si se requiere un modelo compacto de 10 dimensiones en producción, se descarta el Top 10 univariante directo. Se establece a **MCA (10 componentes)** como el reductor óptimo estándar por su capacidad de actuar como regularizador ortogonal, superando al Top 10 directo por más del $4.0\%$ absoluto de F1-macro.

### 3) Estrategias de Balanceo de Clases por Target
- **Para `nivel_riesgo_victima`**: Requiere balanceo mandatorio. Se adopta la configuración **Top 30 Híbrido + SMOTETomek** entrenado bajo **XGBoost**, logrando el mejor F1-macro promedio registrado de **$58.5\%$** con alta consistencia inter-semilla.
- **Para `tipo_violencia`**: Se prescinde del balanceo sintético. Se adopta la configuración **Top 30 Híbrido en escenario Baseline (sin balanceo)** entrenado bajo **XGBoost**, alcanzando un desempeño sobresaliente de **$98.1\%$** en F1-macro.

---

## Notebooks y Documentos Oficiales Activos
- **`evaluacion_dimensionalidad_y_balanceo.ipynb`**: Notebook oficial vigente de evaluación avanzada y benchmarks.
- **`seleccion_caracteristicas_multimetodo_FULL.ipynb`**: Notebook de generación de rankings y consenso de variables.
- **`interpretacion_resultados_completo.md`**: Reporte formal de interpretación y métricas consolidadas.
- **`marco_metodologico_algoritmos.md`**: Sustento teórico, justificación y referencias científicas de la tesis.

---

## Parámetros Operativos Vigentes
- `SAMPLE_SIZE`: 50000 (muestra aleatoria balanceada óptima para control de memoria en 16GB RAM).
- Semillas evaluadas sistemáticamente: `42`, `52`, `62` (reportado en formato $Media \pm Desviación\ Estándar$).
- Exclusión total de fugas de información (leakage): directas, indirectas y proxies (`*_orig`, `*_lbl`).

---

## Próximos Pasos Sugeridos
1. **Optimización Fina de Hiperparámetros**: Ejecutar búsqueda sistemática (`GridSearchCV` o `RandomizedSearchCV`) para el clasificador principal **XGBoost** sobre la estructura óptima de cada target.
2. **Validación Cruzada Estratificada de 5 pliegues final**: Evaluar el pipeline óptimo definitivo en validación cruzada para certificar la estabilidad general del modelo en la tesis.
3. **Reportes Gráficos Definitivos**: Generar las curvas ROC/AUC multiclase, curvas de aprendizaje y matrices de confusión definitivas en resolución de publicación (300 DPI) para el capítulo de resultados.
