package modelo;

public class Persona {
    public enum Estado { SUSCEPTIBLE, INFECTADO, RECUPERADO }

    private Estado estado;

    public Persona(Estado estado) {
        this.estado = estado;
    }

    public Estado getEstado() {
        return estado;
    }

    public void setEstado(Estado estado) {
        this.estado = estado;
    }
}
