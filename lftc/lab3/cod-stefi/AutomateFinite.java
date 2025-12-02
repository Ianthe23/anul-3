package org.example.AF;

import java.util.List;

public class AutomateFinite {
    private Stare initialState;
    private List<Stare> finalStates;
    private List<Tranzitie> transitions;
    private List<Stare> allStates;
    private List<Alfabet> alphabet;

    public AutomateFinite(Stare initialState, List<Stare> finalStates, List<Tranzitie> transitions, List<Stare> allStates,List<Alfabet> alphabet) {
        this.initialState = initialState;
        this.finalStates = finalStates;
        this.transitions = transitions;
        this.allStates = allStates;
        this.alphabet = alphabet;
    }
    public AutomateFinite() {

    }

    public List<Alfabet> getAlphabet() {
        return alphabet;
    }

    public void setAlphabet(List<Alfabet> alphabet) {
        this.alphabet = alphabet;
    }

    public void setBNF(String BNF) {
        this.BNF = BNF;
    }

    public Stare getInitialState() {
        return initialState;
    }

    public void setInitialState(Stare initialState) {
        this.initialState = initialState;
    }

    public List<Stare> getFinalStates() {
        return finalStates;
    }

    public void setFinalStates(List<Stare> finalStates) {
        this.finalStates = finalStates;
    }

    public List<Tranzitie> getTransitions() {
        return transitions;
    }

    public void setTransitions(List<Tranzitie> transitions) {
        this.transitions = transitions;
    }

    public List<Stare> getAllStates() {
        return allStates;
    }

    public void setAllStates(List<Stare> allStates) {
        this.allStates = allStates;
    }

    public String getBNF() {
        return BNF;
    }
    public boolean isInitialized() {
        return initialState != null && finalStates != null && transitions != null && allStates != null;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Stare initiala: ").append(initialState != null ? initialState.getValue() : "null").append("\n");
        sb.append("Stare finala: ");
        if (finalStates != null) {
            for (Stare state : finalStates) {
                sb.append(state.getValue()).append(" ");
            }
        }
        sb.append("\n");
        sb.append("Tranzitii: \n");
        if (transitions != null) {
            for (Tranzitie transition : transitions) {
                sb.append(transition.getSource().getValue()).append(" -> ").append(transition.getDestination().getValue()).append(", ").append(transition.getAlfabet().getValue()).append("\n");
            }
        }
        return sb.toString();
    }
    private boolean isDeterminist()
    {
        for(Stare state: allStates)
        {
            for(Alfabet alphabet: alphabet)
            {
                int count = 0;
                for(Tranzitie transition: transitions)
                {
                    if(transition.getSource().equals(state) && transition.getAlfabet().equals(alphabet))
                    {
                        count++;
                    }
                }
                if(count > 1)
                {
                    return false;
                }
            }
        }
        return true;
    }
    public boolean acceptsSequence(String sequence) {
        if (!isDeterminist()) {
            throw new IllegalArgumentException("Automatul nu este determinist, deci secventa nu poate fi verificata!");
        }
        if (sequence.isEmpty() && finalStates.contains(initialState)) {
            System.out.println("Secventa acceptata: ε (starea initiala este si stare finala)");
            return true;
        }
        Stare currentState = initialState;
        for (char symbol : sequence.toCharArray()) {
            boolean transitionFound = false;
            System.out.println("Stare curenta: " + currentState.getValue() + ", Simbol: " + symbol);

            for (Tranzitie transition : transitions) {
                System.out.println("Verificare tranzitie: " + transition.getSource().getValue() + " " + transition.getAlfabet().getValue() + " " + transition.getDestination().getValue());
                System.out.println("Potrivire sursa: " + transition.getSource().equals(currentState));
                System.out.println("Potrivire simbol: " + transition.getAlfabet().getValue().equals(String.valueOf(symbol)));

                if (transition.getSource().equals(currentState) &&
                        transition.getAlfabet().getValue().equals(String.valueOf(symbol))) {

                    currentState = transition.getDestination();
                    transitionFound = true;
                    break;
                }
            }

            if (!transitionFound) {
                System.out.println("Nu a fost gasita nicio tranzitie pentru simbol: " + symbol + " din stare: " + currentState);
                return false;
            }
        }

        if (finalStates.contains(currentState)) {
            System.out.println("Secventa acceptata, stare finala: " + currentState.getValue());
            return true;
        } else {
            System.out.println("A fost atinsa o stare nefinală: " + currentState.getValue());
            return false;
        }
    }



    public String longestPrefixAccepted(String sequence) {
        if (!isDeterminist()) {
            throw new IllegalArgumentException("Automatul nu este determinist, deci secventa nu poate fi verificata!");
        }
        if (sequence.isEmpty() && finalStates.contains(initialState)) {
            return "ε";
        }

        String longestPrefix = "";
        Stare currentState = initialState;
        StringBuilder currentPrefix = new StringBuilder();

        for (char symbol : sequence.toCharArray()) {
            boolean transitionFound = false;
            for (Tranzitie transition : transitions) {
                if (transition.getSource().equals(currentState) && transition.getAlfabet().getValue().equals(String.valueOf(symbol))) {
                    currentState = transition.getDestination();
                    currentPrefix.append(symbol);
                    transitionFound = true;
                    break;
                }
            }
            if (!transitionFound) {
                break;
            }
            if (finalStates.contains(currentState)) {
                longestPrefix = currentPrefix.toString();
            }
        }
        if(longestPrefix.isEmpty() && finalStates.contains(initialState))
        {
            return "ε";
        }
        return longestPrefix;
    }

}
