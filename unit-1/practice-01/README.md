# Práctica 01 - Construcción y simulación computacional de un modelo matemático

## Objetivo

Comprender el proceso de construcción de un modelo matemático y analizar su
comportamiento mediante Python. En esta práctica se simula el comportamiento de
la atmósfera durante 24 horas para determinar en qué horas existe posibilidad de
lluvia.

## Modelo matemático

El índice de lluvia se calcula como:

```text
I = 0.5·H + 0.3·N + 0.2·Tf
```

Donde:

- `H` = humedad normalizada (0-1).
- `N` = nubosidad normalizada (0-1).
- `Tf` = factor de temperatura obtenido de la tabla del docente.

### Factor de temperatura

| Temperatura | Tf   |
|-------------|------|
| ≤ 10 °C     | 1.00 |
| 12 °C       | 0.90 |
| 14 °C       | 0.80 |
| 16 °C       | 0.70 |
| 18 °C       | 0.60 |
| 20 °C       | 0.50 |
| 22 °C       | 0.40 |
| 24 °C       | 0.30 |
| 26 °C       | 0.20 |
| ≥ 28 °C     | 0.10 |

### Estados del modelo

| Índice I          | Estado            |
|-------------------|-------------------|
| I < 0.40          | Sin lluvia        |
| 0.40 ≤ I < 0.60   | Baja posibilidad  |
| 0.60 ≤ I < 0.75   | Lluvia probable   |
| I ≥ 0.75          | Lluvia            |

## Estructura del proyecto

```text
unit-1/practice-01/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada
│   ├── controller/
│   │   └── controller.py       # Orquesta la simulación sobre DATA
│   ├── model/
│   │   ├── data.py             # Datos horarios de la guía
│   │   ├── rain_model.py       # Modelo principal
│   │   ├── state_classifier.py # Clasificación del estado de lluvia
│   │   ├── strategies.py       # Estrategias de cálculo (patrón Strategy)
│   │   ├── temperature.py      # Tabla de factor de temperatura
│   │   └── validators.py       # Validación de entradas
│   └── view/
│       └── visualization.py    # Gráficas del índice de lluvia
├── tests/
│   └── test_rain_model.py      # Pruebas unitarias con pytest
├── output/                     # Gráficas generadas (no se versiona)
├── README.md
└── requirements.txt
```

### Patrones de diseño y principios SOLID

- **MVC**: separación clara entre modelo (`model/`), vista (`view/`) y controlador
  (`controller/`).
- **Strategy**: `RainModelStrategy` define la interfaz de cálculo;
  `BaseModelStrategy` y `AdjustedModelStrategy` implementan fórmulas distintas.
  Esto permite cambiar o agregar modelos sin modificar `RainModel` (principio
  abierto/cerrado).
- **SRP**: cada clase tiene una sola responsabilidad:
  - `RainModel` valida, normaliza y coordina.
  - `StateClassifier` decide el estado a partir del índice.
  - `validators.py` centraliza la validación.
  - `SimulationController` itera sobre el conjunto de datos.
- **DIP**: `RainModel` depende de la abstracción `RainModelStrategy`, no de una
  implementación concreta.
- **LSP**: cualquier estrategia que implemente `RainModelStrategy` puede
  sustituir a otra sin alterar el comportamiento esperado del modelo.

## Instalación

El entorno virtual ya se encuentra en la raíz del repositorio. Actívalo y
instala las dependencias:

```bash
source ../../.venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Desde el directorio de la práctica:

```bash
python -m src.main
```

Esto imprime las tablas de resultados para el modelo base y el modelo ajustado,
y guarda las gráficas en la carpeta `output/`.

### Ejecutar las pruebas

```bash
python -m pytest tests/ -v
```

## Datos de entrada

| Hora  | Humedad (%) | Nubosidad (%) | Temp. (°C) |
|-------|-------------|---------------|------------|
| 06:00 | 65          | 40            | 14         |
| 08:00 | 70          | 50            | 16         |
| 10:00 | 68          | 45            | 18         |
| 12:00 | 60          | 30            | 22         |
| 14:00 | 75          | 70            | 20         |
| 16:00 | 85          | 85            | 18         |
| 18:00 | 92          | 95            | 16         |
| 20:00 | 88          | 90            | 17         |
| 22:00 | 80          | 75            | 15         |

## Resultados del modelo base

| Hora  | H    | N    | Tf   | Índice | Estado            |
|-------|------|------|------|--------|-------------------|
| 06:00 | 0.65 | 0.40 | 0.80 | 0.605  | Lluvia probable   |
| 08:00 | 0.70 | 0.50 | 0.70 | 0.640  | Lluvia probable   |
| 10:00 | 0.68 | 0.45 | 0.60 | 0.595  | Baja posibilidad  |
| 12:00 | 0.60 | 0.30 | 0.40 | 0.470  | Baja posibilidad  |
| 14:00 | 0.75 | 0.70 | 0.50 | 0.685  | Lluvia probable   |
| 16:00 | 0.85 | 0.85 | 0.60 | 0.800  | Lluvia            |
| 18:00 | 0.92 | 0.95 | 0.70 | 0.885  | Lluvia            |
| 20:00 | 0.88 | 0.90 | 0.70 | 0.850  | Lluvia            |
| 22:00 | 0.80 | 0.75 | 0.80 | 0.785  | Lluvia            |

## Resultados del modelo ajustado

En el modelo ajustado se le da el mismo peso a la humedad y a la nubosidad
(0.4 cada una), manteniendo el factor de temperatura en 0.2:

```text
I = 0.4·H + 0.4·N + 0.2·Tf
```

| Hora  | H    | N    | Tf   | Índice | Estado            |
|-------|------|------|------|--------|-------------------|
| 06:00 | 0.65 | 0.40 | 0.80 | 0.580  | Baja posibilidad  |
| 08:00 | 0.70 | 0.50 | 0.70 | 0.620  | Lluvia probable   |
| 10:00 | 0.68 | 0.45 | 0.60 | 0.572  | Baja posibilidad  |
| 12:00 | 0.60 | 0.30 | 0.40 | 0.440  | Baja posibilidad  |
| 14:00 | 0.75 | 0.70 | 0.50 | 0.680  | Lluvia probable   |
| 16:00 | 0.85 | 0.85 | 0.60 | 0.800  | Lluvia            |
| 18:00 | 0.92 | 0.95 | 0.70 | 0.888  | Lluvia            |
| 20:00 | 0.88 | 0.90 | 0.70 | 0.852  | Lluvia            |
| 22:00 | 0.80 | 0.75 | 0.80 | 0.780  | Lluvia            |

## Interpretación

- Durante la mañana (06:00-12:00) el índice es relativamente bajo; alcanza
  valores de "Baja posibilidad" o "Lluvia probable" según el modelo.
- A partir de las 14:00 el índice crece progresivamente y entre las 16:00 y
  22:00 ambos modelos predicen lluvia.
- El modelo base es más sensible a la humedad (peso 0.5), por lo que alcanza la
  categoría "Lluvia" antes que el modelo ajustado.
- El modelo ajustado da más peso a la nubosidad, lo que genera índices
  ligeramente diferentes pero con la misma tendencia general.

## Gráficas

Las gráficas se generan automáticamente en la carpeta `output/`:

- `output/rain_index_base.png`
- `output/rain_index_adjusted.png`

## Preguntas de control

> **Nota:** las preguntas de la guía hacen referencia a un modelo de
> crecimiento exponencial (`P₀`, `r`), mientras que la práctica desarrollada
> corresponde a un modelo de predicción de lluvia. A continuación se responden
> las preguntas adaptándolas al modelo implementado.

1. **¿Qué es un modelo matemático?**
   Es una representación simplificada de un fenómeno real mediante variables,
   parámetros y relaciones matemáticas que permiten predecir comportamientos.

2. **¿Cuál es la diferencia entre variable y parámetro?**
   Una *variable* cambia durante la simulación (humedad, nubosidad,
   temperatura); un *parámetro* es un valor fijo que define el modelo (los
   pesos 0.5, 0.3 y 0.2 y los umbrales de clasificación).

3. **¿Qué representa `P₀`?**
   En un modelo exponencial representaría la población o cantidad inicial. En
   este modelo de lluvia no existe `P₀`; el equivalente conceptual sería el
   conjunto inicial de condiciones atmosféricas (humedad, nubosidad y
   temperatura a las 06:00).

4. **¿Qué ocurre cuando `r < 0`?**
   En un modelo exponencial una tasa negativa implica decrecimiento. En el
   modelo de lluvia no hay una tasa `r`; el cambio del índice depende de las
   variaciones horarias de las variables de entrada.

5. **¿Qué limitaciones tiene el modelo exponencial?**
   No considera recursos limitados, saturación ni factores externos. De forma
   análoga, el modelo de lluvia implementado es determinista, no usa datos
   históricos reales ni incluye otros factores como presión atmosférica,
   velocidad del viento o topografía local.
