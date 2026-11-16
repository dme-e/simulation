# Práctica 07 - Estimación de resultados mediante el método de Monte Carlo

Estimación de **π** mediante el método de Monte Carlo, con dos implementaciones
(Python y Java) organizadas con el patrón **Modelo - Vista - Controlador (MVC)**
y una comparación de resultados y tiempos de ejecución.

## Modelo matemático

Se generan `N` puntos aleatorios uniformes dentro del cuadrado `[-1, 1] x [-1, 1]`
con un círculo inscrito de radio 1. Se cuenta cuántos puntos caen dentro del
círculo (`Nc`, con `x² + y² ≤ 1`):

```text
π ≈ 4 · (Nc / N)
```

Tamaños de muestra ejecutados: **1 000, 10 000, 100 000 y 1 000 000** de puntos.

## Misma secuencia en Python y Java

La guía pide que ambas implementaciones "produzcan la misma secuencia cuando
utilizan los mismos parámetros". Para lograrlo, la implementación en Python
incluye `GeneradorJava`, una réplica exacta del generador `java.util.Random`
(LCG de 48 bits con las mismas fórmulas de muestreo). Con la misma semilla,
ambos programas generan los mismos puntos y, por lo tanto, el mismo `Nc` y la
misma estimación de π.

## Estructura (MVC)

```text
practice-07/
├── python/
│   ├── src/
│   │   ├── modelo.py        Modelo: GeneradorJava + ExperimentoMonteCarlo
│   │   ├── vista.py         Vista: tabla de consola, CSV y gráfico
│   │   ├── controlador.py   Controlador: orquesta modelo y vistas
│   │   └── main.py          Punto de entrada (argparse)
│   └── tests/
│       └── test_modelo.py   Pruebas del modelo
├── java/
│   ├── src/
│   │   ├── modelo/          ExperimentoMonteCarlo, ResultadoExperimento
│   │   ├── vista/           VistaConsola, ExportadorCsv
│   │   ├── controlador/     ExperimentoControlador
│   │   ├── verificacion/    VerificacionMonteCarlo
│   │   └── Main.java        Punto de entrada
│   └── build/               Clases compiladas
├── resultados/              CSV, gráficos y tabla comparativa
├── scripts/
│   └── comparar_resultados.py
└── README.md
```

| Rol MVC | Responsabilidad |
|---|---|
| **Modelo** | Generador pseudoaleatorio y experimento Monte Carlo (cálculo de `Nc`, estimación y error). No conoce la salida. |
| **Vista** | Presenta resultados: tabla de consola, exportación CSV y gráfico. |
| **Controlador** | Coordina la ejecución para cada `N`, registra el tiempo y entrega los resultados a la vista. |

## Cómo ejecutar

### Python

```bash
cd python
python -m src.main                          # valores por defecto
python -m src.main --tamanos 1000 10000     # tamaños personalizados
python -m src.main --semilla 2026 --csv ../resultados/resultados_python.csv
python -m src.main --grafico ../resultados/error_vs_n.png   # requiere matplotlib
```

Pruebas:

```bash
cd python
python tests/test_modelo.py     # o: pytest tests/
```

### Java

```bash
cd java
javac -encoding UTF-8 -d build $(find src -name "*.java")
java -cp build Main                                    # valores por defecto
java -cp build Main --tamanos 1000 10000 --semilla 2026
```

### Tabla comparativa

```bash
python scripts/comparar_resultados.py
```

Genera `resultados/tabla_comparativa.md` con las columnas de la guía
(N, π estimado, Error, Tiempo Python, Tiempo Java) y verifica que ambas
implementaciones generaron la misma secuencia.

## Variables registradas

- Estimación de π.
- Error absoluto (`|π estimado − π real|`).
- Tiempo de ejecución en Python.
- Tiempo de ejecución en Java.

## Nota

El criterio de evaluación de la guía menciona "modelo M/M/1" por error de
copia: el modelo de esta práctica es el método de Monte Carlo para estimar π.
