# Práctica 02: Comparación de Modelos de Crecimiento Poblacional

## Objetivo

Diferenciar los principales paradigmas de simulación mediante la construcción de modelos computacionales que representen el crecimiento poblacional:

1. **Modelo determinístico** (crecimiento exponencial continuo)
2. **Modelo discreto** (crecimiento por períodos)
3. **Modelo estocástico** (con aleatoriedad)
4. **Modelo continuo** (aproximación numérica de Euler)

Analizar y comparar el comportamiento de cada modelo frente a datos reales de población.

---

## Estructura del Proyecto

```
practice-02/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada
│   ├── model/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuración inmutable con validación
│   │   ├── data.py             # Datos reales (DATOS, TIEMPOS)
│   │   └── strategies.py       # Modelos (Strategy Pattern)
│   ├── controller/
│   │   ├── __init__.py
│   │   └── controller.py       # Orquesta la ejecución de todos los modelos
│   └── view/
│       ├── __init__.py
│       └── visualization.py    # Gráficas comparativas (testable)
├── tests/
│   └── test_models.py          # Pruebas unitarias (pytest)
├── output/                     # Gráficas generadas (gitignored)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Instrucciones de Ejecución

### 1. Crear y activar entorno virtual

```bash
cd /home/dome/Documents/computer-engineering/fifth-cycle/simulation/practices/unit-1/practice-02
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la simulación

```bash
# Desde la raíz del proyecto practice-02
python -m src.main
```

### 4. Ejecutar pruebas

```bash
python -m pytest tests/ -v
```

---

## Tabla de Parámetros

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `P0` | 1000 | Población inicial |
| `r` | 0.15 | Tasa de crecimiento (aproximada) |
| `σ` (sigma) | 20 | Desviación estándar del ruido (modelo estocástico) |
| `dt` | 0.1 | Paso de tiempo para Euler |
| `tiempo` | 6 | Tiempo total de simulación (períodos) |
| `DATOS` | [1000, 1100, 1250, 1400, 1600, 1850, 2100] | Datos reales de población |

---

## Tabla de Resultados (t=0 y t=6)

| Modelo | t=0 | t=6 |
|--------|-----|-----|
| Determinista | 1000.00 | 2459.60 |
| Discreto | 1000.00 | 2313.06 |
| Estocástico (seed=42) | 1000.00 | ~2290-2400* |
| Continuo (Euler) | 1000.00 | 2443.22 |
| **Datos reales** | **1000** | **2100** |

*El modelo estocástico produce valores variables; con seed=42 el resultado es reproducible.

---

## Interpretación de Cada Modelo

### 1. Modelo Determinista (Exponencial)
**Fórmula:** `P(t) = P0 × e^(r×t)`

- **Comportamiento:** Crecimiento suave, continuo y predecible.
- **Supuesto:** La población crece de forma continua e instantánea a una tasa proporcional a su tamaño actual.
- **Resultado:** Sobreestima la población real (2459 vs 2100) porque asume crecimiento compuesto continuo sin límites.

### 2. Modelo Discreto
**Fórmula:** `P_{n+1} = P_n + r × P_n = P_n × (1 + r)`

- **Comportamiento:** Crecimiento por saltos en intervalos discretos (cada período).
- **Supuesto:** La reproducción ocurre en eventos discretos (ej. una vez al año).
- **Resultado:** También sobreestima (2313 vs 2100), pero menos que el continuo porque el compuesto es por períodos.

### 3. Modelo Estocástico
**Fórmula:** `P_{n+1} = P_n + r × P_n + ruido`, donde `ruido ~ Normal(0, σ)`

- **Comportamiento:** Trayectoria aleatoria alrededor de la tendencia determinista.
- **Supuesto:** Factores ambientales impredecibles afectan la población cada período.
- **Resultado:** Con σ=20, el ruido es pequeño relativo a la población; la trayectoria sigue siendo creciente pero con fluctuaciones. La semilla fija (42) garantiza reproducibilidad.

### 4. Modelo Continuo (Euler)
**Fórmula:** `P_{t+dt} = P_t + dt × r × P_t`

- **Comportamiento:** Aproximación numérica paso a paso de la ecuación diferencial `dP/dt = r×P`.
- **Supuesto:** El tiempo avanza en pasos pequeños `dt`; en el límite `dt→0` converge al modelo determinista.
- **Resultado:** Muy cercano al determinista (2443 vs 2459) porque `dt=0.1` es pequeño. Diferencia numérica por error de discretización.

---

## Respuestas a las 10 Preguntas de Control

### 1. ¿Qué representa el arreglo de entrada?
El arreglo `DATOS = [1000, 1100, 1250, 1400, 1600, 1850, 2100]` representa **observaciones reales de población** en 7 momentos temporales consecutivos (t=0 a t=6). Sirven como "datos de verdad" (ground truth) para validar y comparar la precisión de cada modelo de simulación.

### 2. ¿Cuál es la diferencia entre un modelo determinístico y uno estocástico?
- **Determinístico:** Dadas las mismas condiciones iniciales y parámetros, **siempre produce exactamente el mismo resultado**. No hay aleatoriedad; la salida es una función pura de las entradas (ej. `P(t) = P0·e^(rt)`).
- **Estocástico:** Incorpora **variables aleatorias** (ruido). Dadas las mismas condiciones iniciales, **puede producir resultados diferentes** en cada ejecución. Requiere una semilla (seed) para reproducibilidad.

### 3. ¿Qué efecto produce modificar la tasa (r)?
La tasa `r` controla la **velocidad de crecimiento**:
- `r` mayor → crecimiento más rápido, curvas más empinadas, mayor separación entre modelos.
- `r` menor → crecimiento más lento, curvas más planas, modelos convergen.
- `r = 0` → población constante.
- `r < 0` → decrecimiento poblacional (extinción).
En todos los modelos, `r` escala el término de crecimiento (`r×P`), amplificando o reduciendo el cambio poblacional por unidad de tiempo.

### 4. ¿Qué representa el parámetro (σ)?
**Sigma (σ)** es la **desviación estándar de la distribución normal** de la que se extrae el ruido aleatorio en el modelo estocástico. Representa la **magnitud de la variabilidad ambiental** o incertidumbre del sistema:
- σ = 0 → modelo estocástico se vuelve determinístico.
- σ grande → fluctuaciones fuertes, posible extinción (población → 0).
- σ pequeño → fluctuaciones leves alrededor de la tendencia determinista.

### 5. ¿Qué ocurre cuando aumenta el nivel de ruido?
Al aumentar σ:
1. **Mayor dispersión** de las trayectorias estocásticas alrededor de la media.
2. **Probabilidad de extinción** aumenta (población puede llegar a 0 y quedarse ahí por el clamp).
3. **Menor poder predictivo** del modelo; intervalos de confianza más anchos.
4. **Divergencia** entre ejecuciones con diferentes semillas.
5. El modelo determinístico/continuo/discreto **no se ven afectados** (no usan σ).

### 6. ¿Cuál es la diferencia entre los modelos discreto y continuo?
| Aspecto | Discreto | Continuo (Euler) |
|---------|----------|------------------|
| **Tiempo** | Avanza en saltos de 1 (períodos) | Avanza en pasos `dt` (ej. 0.1) |
| **Fórmula** | `P_{n+1} = P_n(1+r)` | `P_{t+dt} = P_t + dt·r·P_t` |
| **Naturaleza** | Eventos puntuales por período | Aproximación de proceso continuo |
| **Límite dt→0** | No aplica | Converge a solución analítica `P0·e^(rt)` |
| **Uso típico** | Censos anuales, reproducción estacional | Sistemas físicos/químicos, alta resolución |

### 7. ¿Qué función cumple (dt)?
`dt` (delta time) es el **tamaño del paso de integración numérica** en el método de Euler:
- Controla el **trade-off precisión vs. costo computacional**.
- `dt` pequeño → más pasos, mayor precisión, más cálculos.
- `dt` grande → menos pasos, error de discretización mayor, posible inestabilidad numérica.
- En el límite `dt → 0`, Euler converge a la solución analítica exacta (modelo determinista).

### 8. ¿Por qué es importante visualizar los resultados mediante gráficas?
1. **Comparación visual inmediata** de trayectorias y divergencias.
2. **Identificación de patrones**: crecimiento exponencial vs. lineal, ruido, saturación.
3. **Validación contra datos reales**: superposición de puntos observados.
4. **Comunicación efectiva** a stakeholders no técnicos.
5. **Detección de anomalidades**: valores negativos, explosiones numéricas, convergencia.
6. **Análisis de sensibilidad** visual al variar parámetros.

### 9. ¿Qué modelo presenta comportamiento aleatorio?
El **modelo estocástico** es el único con comportamiento aleatorio intrínseco, debido al término de ruido `Normal(0, σ)`. Los otros tres (determinista, discreto, continuo/Euler) son completamente determinísticos: misma entrada → misma salida siempre.

### 10. ¿Cómo cambia la simulación cuando se introduce un nuevo arreglo de datos?
Al cambiar `DATOS`:
1. **`tiempo` se recalcula** automáticamente como `len(DATOS) - 1`.
2. **Todos los modelos se ejecutan** sobre el nuevo horizonte temporal.
3. **La gráfica comparativa** se adapta al nuevo rango de tiempo y escala de población.
4. **La validación** (configuración) verifica que `len(DATOS) == tiempo + 1`.
5. **Interpretación**: nuevos datos pueden implicar distinta `r` óptima; los modelos actuales usan `r=0.15` fija (aproximada). Para ajuste riguroso, se requeriría estimación de parámetros (mínimos cuadrados, MLE, etc.).

> **Nota:** La guía menciona NetLogo/pyNetLogo para visualización, pero esta implementación es **Python-only** (NumPy + Matplotlib), cumpliendo con el alcance del grupo sin dependencias externas adicionales.

---

## Licencia

Práctica académica - Simulación (Ciclo 5, Unidad 1)