package verificacion;

import java.util.List;
import modelo.ConfiguracionSIR;
import modelo.ResultadoPaso;
import modelo.SimulacionSIR;

/**
 * Verificación automática de invariantes del modelo SIR.
 * Se ejecuta con {@code java -ea} para habilitar las aserciones.
 */
public class VerificacionSIR {

    public static void main(String[] args) {
        System.out.println("=== Verificación SIR (aserciones habilitadas) ===");
        ConfiguracionSIR config = ConfiguracionSIR.POR_DEFECTO;
        List<ResultadoPaso> resultados = new SimulacionSIR(config).ejecutar();

        verificarPoblacionConstante(config, resultados);
        verificarConteosNoNegativos(resultados);
        verificarEstadoInicial(config, resultados);
        verificarExtincionInfectados(resultados);

        System.out.println("Todas las verificaciones pasaron correctamente.");
    }

    private static void verificarPoblacionConstante(ConfiguracionSIR config, List<ResultadoPaso> resultados) {
        int poblacionEsperada = config.poblacion();
        for (ResultadoPaso paso : resultados) {
            assert paso.poblacionTotal() == poblacionEsperada
                    : "Población no constante en tiempo " + paso.tiempo()
                    + ": esperaba " + poblacionEsperada + ", obtuvo " + paso.poblacionTotal();
        }
        System.out.println("✓ Población constante en todos los pasos.");
    }

    private static void verificarConteosNoNegativos(List<ResultadoPaso> resultados) {
        for (ResultadoPaso paso : resultados) {
            assert paso.susceptibles() >= 0 : "Susceptibles negativo en tiempo " + paso.tiempo();
            assert paso.infectados() >= 0 : "Infectados negativo en tiempo " + paso.tiempo();
            assert paso.recuperados() >= 0 : "Recuperados negativo en tiempo " + paso.tiempo();
        }
        System.out.println("✓ Conteos nunca negativos.");
    }

    private static void verificarEstadoInicial(ConfiguracionSIR config, List<ResultadoPaso> resultados) {
        ResultadoPaso inicial = resultados.get(0);
        assert inicial.tiempo() == 0 : "El primer paso debe ser tiempo 0";
        assert inicial.susceptibles() == config.susceptiblesIniciales()
                : "Susceptibles inicial incorrecto: " + inicial.susceptibles()
                + " (esperaba " + config.susceptiblesIniciales() + ")";
        assert inicial.infectados() == config.infectadosIniciales()
                : "Infectados inicial incorrecto: " + inicial.infectados()
                + " (esperaba " + config.infectadosIniciales() + ")";
        assert inicial.recuperados() == 0 : "Recuperados inicial debe ser 0, era " + inicial.recuperados();
        System.out.println("✓ Estado inicial coincide con la configuración.");
    }

    private static void verificarExtincionInfectados(List<ResultadoPaso> resultados) {
        boolean extinguido = false;
        for (ResultadoPaso paso : resultados) {
            if (extinguido) {
                assert paso.infectados() == 0
                        : "Infectados debería permanecer en 0 después de extinción, pero en tiempo "
                        + paso.tiempo() + " es " + paso.infectados();
            }
            if (paso.infectados() == 0) {
                extinguido = true;
            }
        }
        System.out.println("✓ Una vez I==0, se mantiene en 0.");
    }
}