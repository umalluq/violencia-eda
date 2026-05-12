Para la selección de características en el modelado de la violencia de género, el estudio utiliza una metodología que compara diferentes métodos de búsqueda y evaluadores de atributos para identificar las variables más relevantes.

Las técnicas principales empleadas se dividen de la siguiente manera:

### 1. Métodos de Búsqueda (Search Methods)
El estudio utiliza dos estrategias principales para explorar el conjunto de datos:
*   **Estrategia de Búsqueda Evolutiva Multiobjetivo (MOES):** Específicamente, se aplica el algoritmo evolutivo de búsqueda aleatoria llamado **ENORA** (*Evolutionary NOn-dominated Radial slots-based Algorithm*), el cual busca minimizar simultáneamente el número de características seleccionadas y el error de predicción (RMSE).
*   **Estrategia Ranker:** Esta técnica clasifica y ordena las características individualmente basándose en sus evaluaciones estadísticas.

### 2. Evaluadores de Atributos (Attribute Evaluators)
Estas técnicas se encargan de calificar la utilidad de los subconjuntos de variables y se agruparon en dos categorías:
*   **Métodos Wrapper (Multivariantes):** Evalúan combinaciones de factores utilizando algoritmos predictivos para determinar su fuerza de pronóstico. En este trabajo, se utilizaron los siguientes predictores dentro del enfoque wrapper:
    *   **Regresión Lineal (LR)**.
    *   **Random Forest (RF)**.
    *   **K-vecinos más cercanos (IBk)**.
*   **Métodos Filter (Univariantes):** Evalúan el poder predictivo de cada variable de forma individual. Se emplearon:
    *   **Relief Attribute (Rlf):** Basado en la identificación de diferencias de valores entre pares de instancias cercanas.
    *   **Análisis de Componentes Principales (PCA):** Transforma los datos a una menor dimensionalidad maximizando la varianza.

### La técnica ganadora
De todas las combinaciones probadas, las fuentes señalan que la técnica más eficaz fue la **Búsqueda Evolutiva Multiobjetivo combinada con Random Forest (MOES-RF)**. Esta combinación permitió obtener las predicciones más precisas de denuncias por violencia de género, logrando un error medio (RMSE) de solo **0.1686 denuncias por cada 10,000 habitantes** en el territorio español.
