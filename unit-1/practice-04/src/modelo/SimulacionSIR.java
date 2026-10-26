package modelo;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import modelo.Persona.Estado;

public class SimulacionSIR {

    private final ConfiguracionSIR config;

    public SimulacionSIR(ConfiguracionSIR config) {
        this.config = config;
    }

    public SimulacionSIR() {
        this(ConfiguracionSIR.POR_DEFECTO);
    }

    /**
     * Ejecuta la simulación y devuelve la lista de resultados por paso.
     * El primer elemento (índice 0) corresponde al tiempo 0 (estado inicial).
     */
    public List<ResultadoPaso> ejecutar() {
        Random azar = new Random(config.semilla());
        Persona[] personas = new Persona[config.poblacion()];
        for (int i = 0; i < config.poblacion(); i++) {
            personas[i] = new Persona(i < config.infectadosIniciales()
                    ? Estado.INFECTADO : Estado.SUSCEPTIBLE);
        }

        List<ResultadoPaso> resultados = new ArrayList<>();
        resultados.add(contar(personas, 0));

        for (int tiempo = 1; tiempo <= config.tiempoSimulacion(); tiempo++) {
            avanzar(personas, azar);
            resultados.add(contar(personas, tiempo));
        }
        return resultados;
    }

    private void avanzar(Persona[] personas, Random azar) {
        Estado[] siguientes = new Estado[config.poblacion()];
        for (int i = 0; i < config.poblacion(); i++) {
            siguientes[i] = personas[i].getEstado();
        }

        for (int i = 0; i < config.poblacion(); i++) {
            if (personas[i].getEstado() != Estado.INFECTADO) {
                continue;
            }

            if (config.poblacion() > 1) {
                int contacto = azar.nextInt(config.poblacion() - 1);
                if (contacto >= i) {
                    contacto++;
                }
                if (personas[contacto].getEstado() == Estado.SUSCEPTIBLE
                        && azar.nextDouble() < config.beta()) {
                    siguientes[contacto] = Estado.INFECTADO;
                }
            }
            if (azar.nextDouble() < config.gamma()) {
                siguientes[i] = Estado.RECUPERADO;
            }
        }

        for (int i = 0; i < config.poblacion(); i++) {
            personas[i].setEstado(siguientes[i]);
        }
    }

    private ResultadoPaso contar(Persona[] personas, int tiempo) {
        int susceptibles = 0;
        int infectados = 0;
        int recuperados = 0;
        for (Persona persona : personas) {
            switch (persona.getEstado()) {
                case SUSCEPTIBLE:
                    susceptibles++;
                    break;
                case INFECTADO:
                    infectados++;
                    break;
                case RECUPERADO:
                    recuperados++;
                    break;
            }
        }
        return new ResultadoPaso(tiempo, susceptibles, infectados, recuperados);
    }
}