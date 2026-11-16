package vista;

import modelo.ResultadoExperimento;

import java.util.List;
import java.util.Locale;

/**
 * View: renders Monte Carlo results to the standard output.
 * Column headers follow the comparison table required by the practice guide.
 */
public final class VistaConsola {

    private static final int ANCHO_N = 12;
    private static final int ANCHO_NUM = 14;

    public void mostrarFila(ResultadoExperimento resultado) {
        System.out.println(formatearFila(resultado));
    }

    public void mostrarTabla(List<ResultadoExperimento> resultados) {
        System.out.println();
        System.out.printf(Locale.US, "%" + ANCHO_N + "s %" + ANCHO_NUM + "s %"
                        + ANCHO_NUM + "s %" + ANCHO_NUM + "s%n",
                "N", "pi estimado", "Error", "Tiempo Java");
        System.out.println("-".repeat(ANCHO_N + 3 * ANCHO_NUM));
        for (ResultadoExperimento resultado : resultados) {
            System.out.println(formatearFila(resultado));
        }
        System.out.println();
    }

    private static String formatearFila(ResultadoExperimento r) {
        return String.format(Locale.US, "%" + ANCHO_N + "d %" + ANCHO_NUM + ".6f %"
                        + ANCHO_NUM + ".6f %" + ANCHO_NUM + ".4f",
                r.n(), r.piEstimado(), r.errorAbsoluto(), r.tiempoSegundos());
    }
}
