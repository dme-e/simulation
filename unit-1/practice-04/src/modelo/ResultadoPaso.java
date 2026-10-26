package modelo;

/**
 * Clase inmutable que representa el estado de la simulación en un paso de tiempo.
 */
public final class ResultadoPaso {
    private final int tiempo;
    private final int susceptibles;
    private final int infectados;
    private final int recuperados;

    public ResultadoPaso(int tiempo, int susceptibles, int infectados, int recuperados) {
        if (susceptibles < 0 || infectados < 0 || recuperados < 0) {
            throw new IllegalArgumentException("Los conteos no pueden ser negativos.");
        }
        if (tiempo < 0) {
            throw new IllegalArgumentException("El tiempo no puede ser negativo.");
        }
        this.tiempo = tiempo;
        this.susceptibles = susceptibles;
        this.infectados = infectados;
        this.recuperados = recuperados;
    }

    public int tiempo() { return tiempo; }
    public int susceptibles() { return susceptibles; }
    public int infectados() { return infectados; }
    public int recuperados() { return recuperados; }

    public int poblacionTotal() {
        return susceptibles + infectados + recuperados;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof ResultadoPaso)) return false;
        ResultadoPaso that = (ResultadoPaso) o;
        return tiempo == that.tiempo
                && susceptibles == that.susceptibles
                && infectados == that.infectados
                && recuperados == that.recuperados;
    }

    @Override
    public int hashCode() {
        int result = tiempo;
        result = 31 * result + susceptibles;
        result = 31 * result + infectados;
        result = 31 * result + recuperados;
        return result;
    }

    @Override
    public String toString() {
        return "ResultadoPaso[tiempo=" + tiempo + ", S=" + susceptibles + ", I=" + infectados + ", R=" + recuperados + "]";
    }
}