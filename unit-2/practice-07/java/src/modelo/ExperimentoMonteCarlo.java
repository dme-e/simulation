package modelo;

import java.util.Random;

/**
 * Model: Monte Carlo experiment that estimates pi by sampling points uniformly
 * in the square [-1, 1] x [-1, 1] and counting how many fall inside the
 * inscribed circle (x^2 + y^2 &lt;= 1).
 *
 * <p>pi ~= 4 * (Nc / N)</p>
 *
 * <p>The generator is java.util.Random with an explicit seed, so the Python
 * implementation (which replicates the same LCG) produces the exact same
 * sequence of points for the same seed and sample size.</p>
 */
public final class ExperimentoMonteCarlo {

    private final long semilla;

    public ExperimentoMonteCarlo(long semilla) {
        this.semilla = semilla;
    }

    public long getSemilla() {
        return semilla;
    }

    public ResultadoExperimento ejecutar(int n) {
        if (n <= 0) {
            throw new IllegalArgumentException("n must be positive");
        }
        Random rng = new Random(semilla);
        int aciertos = 0;
        long inicio = System.nanoTime();
        for (int i = 0; i < n; i++) {
            double x = rng.nextDouble() * 2.0 - 1.0;
            double y = rng.nextDouble() * 2.0 - 1.0;
            if (x * x + y * y <= 1.0) {
                aciertos++;
            }
        }
        double tiempo = (System.nanoTime() - inicio) / 1_000_000_000.0;
        double piEstimado = 4.0 * aciertos / n;
        return new ResultadoExperimento(
                n,
                aciertos,
                piEstimado,
                Math.abs(piEstimado - Math.PI),
                tiempo);
    }
}
