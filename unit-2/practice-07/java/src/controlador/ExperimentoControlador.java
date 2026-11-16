package controlador;

import modelo.ExperimentoMonteCarlo;
import modelo.ResultadoExperimento;
import vista.ExportadorCsv;
import vista.VistaConsola;

import java.util.ArrayList;
import java.util.List;

/**
 * Controller: runs the experiment for each sample size and hands the results
 * to the views (console table and CSV export).
 */
public final class ExperimentoControlador {

    private final ExperimentoMonteCarlo modelo;
    private final VistaConsola vista;
    private final List<Integer> tamanos;
    private final List<ResultadoExperimento> resultados = new ArrayList<>();

    public ExperimentoControlador(ExperimentoMonteCarlo modelo, List<Integer> tamanos) {
        this(modelo, new VistaConsola(), tamanos);
    }

    public ExperimentoControlador(ExperimentoMonteCarlo modelo, VistaConsola vista,
                                  List<Integer> tamanos) {
        this.modelo = modelo;
        this.vista = vista;
        this.tamanos = List.copyOf(tamanos);
    }

    public List<ResultadoExperimento> ejecutar() {
        resultados.clear();
        for (int n : tamanos) {
            ResultadoExperimento resultado = modelo.ejecutar(n);
            resultados.add(resultado);
            vista.mostrarFila(resultado);
        }
        vista.mostrarTabla(resultados);
        return List.copyOf(resultados);
    }

    public void exportar(String rutaCsv) {
        String ruta = ExportadorCsv.guardar(resultados, rutaCsv);
        System.out.println("Resultados guardados en " + ruta);
    }
}
