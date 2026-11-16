package verificacion;

import modelo.ExperimentoMonteCarlo;
import modelo.ResultadoExperimento;

/**
 * Sanity checks run before the experiment: determinism, convergence and input
 * validation. Mirrors the repo's verificacion package convention.
 */
public final class VerificacionMonteCarlo {

    private VerificacionMonteCarlo() {
    }

    public static void ejecutar() {
        ResultadoExperimento r1 = new ExperimentoMonteCarlo(2026).ejecutar(100_000);
        comprobar(r1.errorAbsoluto() < 0.02, "convergencia con N=100000");
        ResultadoExperimento r2 = new ExperimentoMonteCarlo(2026).ejecutar(100_000);
        comprobar(r1.aciertos() == r2.aciertos(), "determinismo con la misma semilla");
        boolean rechazaNInvalido;
        try {
            new ExperimentoMonteCarlo(2026).ejecutar(0);
            rechazaNInvalido = false;
        } catch (IllegalArgumentException e) {
            rechazaNInvalido = true;
        }
        comprobar(rechazaNInvalido, "rechazo de N invalido");
        System.out.println("Verificacion: OK");
    }

    private static void comprobar(boolean condicion, String descripcion) {
        if (!condicion) {
            throw new IllegalStateException("Verificacion fallida: " + descripcion);
        }
    }
}
