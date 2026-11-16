import controlador.ExperimentoControlador;
import modelo.ExperimentoMonteCarlo;
import verificacion.VerificacionMonteCarlo;

import java.util.ArrayList;
import java.util.List;

/**
 * Entry point of the Java Monte Carlo experiment (practice 07).
 *
 * <p>Usage: java -cp build Main [--tamanos 1000 10000 ...] [--semilla N] [--csv ruta]</p>
 */
public final class Main {

    private static final long SEMILLA_DEFECTO = 2026;
    private static final String CSV_DEFECTO = "../resultados/resultados_java.csv";

    private Main() {
    }

    public static void main(String[] args) {
        List<Integer> tamanos = new ArrayList<>(List.of(1000, 10000, 100000, 1000000));
        long semilla = SEMILLA_DEFECTO;
        String csv = CSV_DEFECTO;

        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--tamanos" -> {
                    tamanos.clear();
                    while (i + 1 < args.length && !args[i + 1].startsWith("--")) {
                        tamanos.add(Integer.parseInt(args[++i]));
                    }
                }
                case "--semilla" -> semilla = Long.parseLong(args[++i]);
                case "--csv" -> csv = args[++i];
                case "--ayuda", "--help" -> {
                    mostrarAyuda();
                    return;
                }
                default -> {
                    System.err.println("Opcion desconocida: " + args[i]);
                    mostrarAyuda();
                    System.exit(2);
                }
            }
        }

        VerificacionMonteCarlo.ejecutar();
        ExperimentoControlador controlador =
                new ExperimentoControlador(new ExperimentoMonteCarlo(semilla), tamanos);
        controlador.ejecutar();
        controlador.exportar(csv);
    }

    private static void mostrarAyuda() {
        System.out.println("Uso: java -cp build Main [opciones]");
        System.out.println("  --tamanos N1 N2 ...   tamanos de muestra (defecto: 1000 10000 100000 1000000)");
        System.out.println("  --semilla N           semilla del generador (defecto: 2026)");
        System.out.println("  --csv ruta            archivo CSV de resultados");
        System.out.println("  --ayuda               muestra esta ayuda");
    }
}
