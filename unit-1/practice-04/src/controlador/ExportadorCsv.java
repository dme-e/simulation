package controlador;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;
import modelo.ConfiguracionSIR;
import modelo.ResultadoPaso;

/**
 * Encargado de exportar resultados y configuración a CSV, y copiarlos a la carpeta de NetLogo.
 */
public class ExportadorCsv {

    public void exportarResultados(List<ResultadoPaso> resultados, Path archivo) throws IOException {
        Files.createDirectories(archivo.getParent());
        try (BufferedWriter escritor = Files.newBufferedWriter(archivo, StandardCharsets.UTF_8)) {
            escritor.write("tiempo,susceptibles,infectados,recuperados");
            escritor.newLine();
            for (ResultadoPaso paso : resultados) {
                escritor.write(paso.tiempo() + "," + paso.susceptibles() + ","
                        + paso.infectados() + "," + paso.recuperados());
                escritor.newLine();
            }
        }
    }

    public void exportarConfiguracion(ConfiguracionSIR config, Path archivo) throws IOException {
        Files.createDirectories(archivo.getParent());
        try (BufferedWriter escritor = Files.newBufferedWriter(archivo, StandardCharsets.UTF_8)) {
            escritor.write("poblacion,infectados_iniciales,beta,gamma,tiempo_maximo,semilla");
            escritor.newLine();
            escritor.write(config.poblacion() + ","
                    + config.infectadosIniciales() + ","
                    + config.beta() + ","
                    + config.gamma() + ","
                    + config.tiempoSimulacion() + ","
                    + config.semilla());
            escritor.newLine();
        }
    }

    public void copiarANetLogo(Path origenResultados, Path origenParametros) throws IOException {
        Files.createDirectories(Paths.get("netlogo"));
        Files.copy(origenResultados, Paths.get("netlogo", "resultados_java.csv"),
                StandardCopyOption.REPLACE_EXISTING);
        Files.copy(origenParametros, Paths.get("netlogo", "parametros_java.csv"),
                StandardCopyOption.REPLACE_EXISTING);
    }
}