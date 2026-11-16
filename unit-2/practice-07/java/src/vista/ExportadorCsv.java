package vista;

import modelo.ResultadoExperimento;

import java.io.IOException;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;

/**
 * View: writes results to a CSV file with the schema shared with the Python
 * run (n, aciertos, pi_estimado, error_absoluto, tiempo_segundos).
 */
public final class ExportadorCsv {

    public static final String COLUMNAS =
            "n,aciertos,pi_estimado,error_absoluto,tiempo_segundos";

    private ExportadorCsv() {
    }

    public static String guardar(List<ResultadoExperimento> resultados, String ruta) {
        Path destino = Path.of(ruta);
        try {
            if (destino.getParent() != null) {
                Files.createDirectories(destino.getParent());
            }
            try (Writer escritor = Files.newBufferedWriter(destino)) {
                escritor.write(COLUMNAS + System.lineSeparator());
                for (ResultadoExperimento r : resultados) {
                    escritor.write(String.format(Locale.US, "%d,%d,%.12f,%.12f,%.6f%n",
                            r.n(), r.aciertos(), r.piEstimado(),
                            r.errorAbsoluto(), r.tiempoSegundos()));
                }
            }
        } catch (IOException e) {
            throw new RuntimeException("No se pudo escribir " + destino, e);
        }
        return destino.toString();
    }
}
