package controlador;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import modelo.ConfiguracionSIR;
import modelo.ResultadoPaso;
import modelo.SimulacionSIR;
import vista.VistaConsola;

public class SimulacionControlador {

    private final ConfiguracionSIR config;
    private final SimulacionSIR simulacion;
    private final ExportadorCsv exportador;
    private final VistaConsola vista;

    public SimulacionControlador() {
        this(ConfiguracionSIR.POR_DEFECTO);
    }

    public SimulacionControlador(ConfiguracionSIR config) {
        this.config = config;
        this.simulacion = new SimulacionSIR(config);
        this.exportador = new ExportadorCsv();
        this.vista = new VistaConsola();
    }

    public void ejecutar() throws IOException {
        long inicio = System.nanoTime();
        List<ResultadoPaso> resultados = simulacion.ejecutar();
        double segundos = (System.nanoTime() - inicio) / 1_000_000_000.0;

        Path archivoResultados = Paths.get("resultados", "resultados_java.csv");
        Path archivoParametros = Paths.get("resultados", "parametros_java.csv");

        exportador.exportarResultados(resultados, archivoResultados);
        exportador.exportarConfiguracion(config, archivoParametros);
        exportador.copiarANetLogo(archivoResultados, archivoParametros);

        vista.mostrar(config, resultados, segundos);
    }
}