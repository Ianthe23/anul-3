package org.example.AF;


public class Tranzitie {
    private Stare source;
    private Alfabet alfabet;
    private Stare destination;

    public Tranzitie(Stare source, Alfabet alfabet, Stare destination) {
        this.source = source;
        this.alfabet = alfabet;
        this.destination = destination;
    }

    public Stare getSource() {
        return source;
    }

    public void setSource(Stare source) {
        this.source = source;
    }

    public Alfabet getAlfabet() {
        return alfabet;
    }

    public void setAlfabet(Alfabet alfabet) {
        this.alfabet = alfabet;
    }

    public Stare getDestination() {
        return destination;
    }

    public void setDestination(Stare destination) {
        this.destination = destination;
    }

    public static Tranzitie stringToTransition(String string){
        String[] parts = string.split("->");
        Stare source = new Stare(parts[0].trim());
        Stare destination = new Stare(parts[1].split(",")[0].trim());
        Alfabet alphabet = new Alfabet(parts[1].split(",")[1].trim());
        return new Tranzitie(source, alphabet, destination);
    }

    @Override
    public String toString() {
        return source.getValue() + " -> " + destination.getValue() + ", " + alfabet.getValue();
    }
}
