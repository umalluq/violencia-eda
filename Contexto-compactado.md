Goal
- Realizar un Análisis Exploratorio de Datos (EDA) y selección multimetodo de características sobre registros de violencia contra la mujer para generar una base en Parquet optimizada para modelado predictivo.
Constraints & Preferences
- Hardware: 16 GB RAM, Intel i7-13650HX, NVIDIA RTX 4050 (Manjaro Linux).
- Dataset: ~936k filas x 186 columnas (BD_2020-2025.csv).
- Target Encoding: Los targets deben empezar en 0 (0, 1, 2) para compatibilidad con XGBoost.
- Exclusión: Eliminar registros de "Violencia Económica" por baja representatividad.
Progress
Done
- Creación de eda_denuncias.ipynb con limpieza, tipado semántico e imputación trazable.
- Generación de base_modelado.parquet con targets estandarizados y enriquecimiento de UBIGEO.
- Desarrollo de analisis_estadistico_y_features.ipynb con gráficos de series temporales, geografía y asociación inicial.
- Creación de script ETL automatizado scripts/update_parquet_pipeline.py y skill etl-tesis-v2.skill.
- Configuración de repositorio Git local y remoto (GitHub) con documentación README.md y README_ejecutivo.md.
- Definición de targets: tipo_violencia (0: Psicológica, 1: Física, 2: Sexual) y nivel_riesgo_victima (0: Bajo, 1: Medio, 2: Alto).
- Optimización de seleccion_caracteristicas_multimetodo.ipynb: implementado muestreo estratificado (100k), preprocesamiento diferido y uso eficiente de memoria (float32, gc.collect) para evitar crashes OOM en 16GB RAM.
In Progress
- Ejecución de la selección multimetodo optimizada para obtener el ranking final de características.
Key Decisions
- Uso de Parquet: Para mejorar el rendimiento de lectura y reducir el tamaño en disco vs CSV.
- Normalización de Nombres: Columnas en minúsculas, sin acentos ni espacios para evitar errores de codificación.
- Tipado Semántico: Diferenciación entre categorica_codificada y numerica_real para aplicar imputaciones lógicas (mediana vs "desconocido").
- Estandarización 0-based: Recodificación de targets a [0, 1, 2] para cumplir requisitos de algoritmos como XGBoost.
Next Steps
- Implementar muestreo estratificado (ej. 100k filas) en el notebook de selección de características para estabilizar el uso de RAM.
- Optimizar el paso de RFECV aumentando el step y reduciendo el número de estimadores.
- Cruzar resultados de Chi2, MI, Random Forest Importance y Permutation Importance para obtener un ranking de consenso.
Critical Context
- El error KeyError: 'ubigeo_nombre' en el notebook de análisis fue resuelto limpiando columnas conflictivas antes del merge.
- La identidad de Git fue configurada localmente para permitir el versionado.
- El archivo original BD_2020-2025.csv supera el límite de 100MB de GitHub y fue excluido del repositorio mediante .gitignore.
Relevant Files
- /home/munasqa/MAESTRIA/opencode/BD_2020-2025.csv: Dataset original.
- /home/munasqa/MAESTRIA/opencode/base_modelado.parquet: Base limpia para modelos.
- /home/munasqa/MAESTRIA/opencode/seleccion_caracteristicas_multimetodo.ipynb: Notebook que causa el crash de RAM.
- /home/munasqa/MAESTRIA/opencode/ubigeo_trabajar.csv: Maestro para enriquecimiento geográfico.
- /home/munasqa/MAESTRIA/opencode/scripts/update_parquet_pipeline.py: Pipeline para procesar nueva data.
