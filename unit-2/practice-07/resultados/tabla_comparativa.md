# Tabla comparativa Python vs Java

Ambas implementaciones usan la misma semilla y el mismo generador
(LCG de java.util.Random), por lo que producen la misma secuencia.

| N | pi estimado | Error | Tiempo Python | Tiempo Java |
|---|---|---|---|---|
| 1 000 | 3.088000 | 0.053593 | 0.0007 s | 0.0000 s |
| 10 000 | 3.141200 | 0.000393 | 0.0075 s | 0.0004 s |
| 100 000 | 3.134360 | 0.007233 | 0.0746 s | 0.0042 s |
| 1 000 000 | 3.140140 | 0.001453 | 0.7543 s | 0.0395 s |
