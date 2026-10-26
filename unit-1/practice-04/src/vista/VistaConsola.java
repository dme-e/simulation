package vista;

import java.util.List;
import modelo.ConfiguracionSIR;
import modelo.ResultadoPaso;

public class VistaConsola {

    public void mostrar(ConfiguracionSIR config, List<ResultadoPaso> resultados, double segundos) {
        System.out.println("PRÁCTICA 04 - MODELO SIR EN JAVA");
        System.out.printf("Población: %d | Infectados iniciales: %d%n",
                config.poblacion(), config.infectadosIniciales());
        System.out.printf("Beta: %.2f | Gamma: %.2f | Pasos: %d | Semilla: %d%n",
                config.beta(), config.gamma(),
                config.tiempoSimulacion(), config.semilla());
        System.out.println("S: susceptibles | I: infectados | R: recuperados");
        System.out.printf("%6s %6s %6s %6s%n", "Tiempo", "S", "I", "R");

        ResultadoPaso pico = resultados.get(0);
        for (ResultadoPaso paso : resultados) {
            if (paso.tiempo() % 10 == 0 || paso == resultados.get(resultados.size() - 1)) {
                System.out.printf("%6d %6d %6d %6d%n",
                        paso.tiempo(), paso.susceptibles(), paso.infectados(), paso.recuperados());
            }
            if (paso.infectados() > pico.infectados()) {
                pico = paso;
            }
        }
        System.out.printf("Máximo de infectados: %d en el tiempo %d.%n", pico.infectados(), pico.tiempo());
        System.out.printf("Tiempo de cálculo (sin escribir archivos): %.6f s%n", segundos);
        System.out.println("CSV: resultados/resultados_java.csv");
        System.out.println("Copia para NetLogo: netlogo/resultados_java.csv");
        System.out.println("Parámetros para NetLogo: netlogo/parametros_java.csv");
    }
}