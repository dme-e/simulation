package modelo;

/**
 * Configuración inmutable para la simulación SIR con validación en el constructor.
 */
public final class ConfiguracionSIR {
    private final int poblacion;
    private final int infectadosIniciales;
    private final double beta;
    private final double gamma;
    private final int tiempoSimulacion;
    private final long semilla;

    public ConfiguracionSIR(int poblacion, int infectadosIniciales, double beta, double gamma,
                            int tiempoSimulacion, long semilla) {
        if (poblacion < 1) {
            throw new IllegalArgumentException("POBLACION debe ser un entero positivo.");
        }
        if (infectadosIniciales < 0 || infectadosIniciales > poblacion) {
            throw new IllegalArgumentException("INFECTADOS_INICIALES debe estar entre 0 y POBLACION.");
        }
        if (!Double.isFinite(beta) || beta < 0 || beta > 1) {
            throw new IllegalArgumentException("BETA debe ser un número finito entre 0 y 1.");
        }
        if (!Double.isFinite(gamma) || gamma < 0 || gamma > 1) {
            throw new IllegalArgumentException("GAMMA debe ser un número finito entre 0 y 1.");
        }
        if (tiempoSimulacion < 0) {
            throw new IllegalArgumentException("TIEMPO_SIMULACION debe ser un entero no negativo.");
        }
        if (semilla < Integer.MIN_VALUE || semilla > Integer.MAX_VALUE) {
            throw new IllegalArgumentException("SEMILLA debe estar entre -2147483648 y 2147483647 para NetLogo.");
        }
        this.poblacion = poblacion;
        this.infectadosIniciales = infectadosIniciales;
        this.beta = beta;
        this.gamma = gamma;
        this.tiempoSimulacion = tiempoSimulacion;
        this.semilla = semilla;
    }

    public int poblacion() { return poblacion; }
    public int infectadosIniciales() { return infectadosIniciales; }
    public double beta() { return beta; }
    public double gamma() { return gamma; }
    public int tiempoSimulacion() { return tiempoSimulacion; }
    public long semilla() { return semilla; }

    public int susceptiblesIniciales() {
        return poblacion - infectadosIniciales;
    }

    public static final ConfiguracionSIR POR_DEFECTO = new ConfiguracionSIR(
            100,      // poblacion
            5,        // infectadosIniciales
            0.30,     // beta
            0.10,     // gamma
            100,      // tiempoSimulacion
            42L       // semilla
    );

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof ConfiguracionSIR)) return false;
        ConfiguracionSIR that = (ConfiguracionSIR) o;
        return poblacion == that.poblacion
                && infectadosIniciales == that.infectadosIniciales
                && Double.compare(beta, that.beta) == 0
                && Double.compare(gamma, that.gamma) == 0
                && tiempoSimulacion == that.tiempoSimulacion
                && semilla == that.semilla;
    }

    @Override
    public int hashCode() {
        int result = poblacion;
        result = 31 * result + infectadosIniciales;
        long temp = Double.doubleToLongBits(beta);
        result = 31 * result + (int) (temp ^ (temp >>> 32));
        temp = Double.doubleToLongBits(gamma);
        result = 31 * result + (int) (temp ^ (temp >>> 32));
        result = 31 * result + tiempoSimulacion;
        result = 31 * result + (int) (semilla ^ (semilla >>> 32));
        return result;
    }

    @Override
    public String toString() {
        return "ConfiguracionSIR[poblacion=" + poblacion + ", infectadosIniciales=" + infectadosIniciales
                + ", beta=" + beta + ", gamma=" + gamma + ", tiempoSimulacion=" + tiempoSimulacion
                + ", semilla=" + semilla + "]";
    }
}