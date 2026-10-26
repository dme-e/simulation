# Simulación - Prácticas

Repositorio de las prácticas de la asignatura **Simulación** (ciclo 5, Carrera de Computación).

Cada práctica está organizada como un proyecto independiente con código fuente, pruebas (donde aplica) y un `README.md` propio. Los proyectos siguen una organización **MVC** simple y, cuando el problema lo permite, usan el patrón **Strategy** para separar variantes de un mismo modelo.

---

## Estructura del repositorio

```text
.
├── unit-1/
│   ├── practice-01/   Modelo matemático de predicción de lluvia (Python)
│   ├── practice-02/   Comparación de modelos de crecimiento poblacional (Python)
│   ├── practice-03/   Simulación de cola M/M/1 con SimPy (Python)
│   └── practice-04/   Modelo epidemiológico SIR en Java y NetLogo
├── unit-2/
│   └── (pendiente)
├── unit-3/
│   └── (pendiente)
├── .venv/             Entorno virtual compartido para las prácticas en Python
└── README.md          Este archivo
```

---

## Prácticas implementadas

| Práctica | Tema | Tecnología | Patrones / principios |
|---|---|---|---|
| `unit-1/practice-01` | Predicción de lluvia con humedad, nubosidad y temperatura | Python, Matplotlib | MVC, Strategy, SOLID |
| `unit-1/practice-02` | Comparación de modelos determinístico, discreto, estocástico y continuo | Python, NumPy, Matplotlib | MVC, Strategy, SOLID |
| `unit-1/practice-03` | Simulación de una cola M/M/1 | Python, SimPy, Matplotlib | MVC, SOLID |
| `unit-1/practice-04` | Modelo epidemiológico SIR | Java, NetLogo | MVC |

---

## Entorno virtual

La mayoría de las prácticas en Python pueden usar el entorno virtual compartido en la raíz:

```bash
source .venv/bin/activate
```

Si la práctica tiene su propio `.venv/`, se indica en su `README.md` interno.

---

## Cómo ejecutar cada práctica

### Practice-01 (Python)

```bash
cd unit-1/practice-01
python -m src.main          # ejecuta la simulación y guarda las gráficas
python -m pytest tests/ -v  # ejecuta las pruebas
```

### Practice-02 (Python)

```bash
cd unit-1/practice-02
python -m src.main          # compara los cuatro modelos de crecimiento
python -m pytest tests/ -v  # ejecuta las pruebas
```

### Practice-03 (Python + SimPy)

```bash
cd unit-1/practice-03
python main.py              # ejecuta los tres escenarios M/M/1
```

### Practice-04 (Java + NetLogo)

```bash
cd unit-1/practice-04
javac -encoding UTF-8 --release 11 -d build \
  src/Main.java src/modelo/*.java src/vista/*.java \
  src/controlador/*.java src/verificacion/*.java
java -cp build Main
java -ea -cp build verificacion.VerificacionSIR
```

NetLogo lee los CSV generados por Java desde `netlogo/`.

---

## Convenciones

- **MVC**: separación clara entre modelo, vista y controlador.
- **Strategy**: cuando una práctica necesita varias variantes de un cálculo, cada variante es una clase pequeña que implementa una interfaz común.
- **SOLID**: clases con una sola responsabilidad, configuración inmutable con validación, y dependencia de abstracciones.
- **Tests**: las prácticas 01 y 02 incluyen pruebas con `pytest`.
- **Datos y figuras**: los archivos CSV y las imágenes generadas por los programas se conservan cuando la guía los solicita como entregables. Los documentos PDF, fuentes LaTeX y plantillas de informe no se versionan.

---

## Autor

Doménica Anahí Rojas Curimilma
