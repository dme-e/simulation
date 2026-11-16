package modelo;

/**
 * Immutable result of one Monte Carlo run for a sample size N.
 * Fields mirror the variables required by the practice guide.
 */
public record ResultadoExperimento(
        int n,
        int aciertos,
        double piEstimado,
        double errorAbsoluto,
        double tiempoSegundos) {
}
