package org.example.AF;

import java.util.Objects;

public class Stare {
    private String value;
    private StareType type = StareType.NORMAL;

    public Stare(String value)
    {
        if(isValid(value)){
            this.value = value;
        }
        else{
            throw  new IllegalArgumentException("Invalid value");
        }
    }

    public Stare(String value, StareType type){
        if(isValid(value)){
            this.value = value;
            this.type = type;
        }
        else{
            throw  new IllegalArgumentException("Invalid value");
        }
    }
    public String getValue() {
        return value;
    }
    public void setValue(String value) {
        if(isValid(value)) {
            this.value = value;
        }
        else {
            throw new IllegalArgumentException("Invalid value for state");
        }
    }

    //vf daca e ok pt bnf
    //<stare> ::= <string>
    //<string> ::= <caracter> {<caracter>}*
    //<string> ::= <caracter> {<caracter>}*
    public boolean isValid(String value){
        if(value == null || value.isEmpty()) {
            return false;
        }

        char firstChar = value.charAt(0);
        if(!((firstChar >= 'a' && firstChar <= 'z') || (firstChar >= 'A' && firstChar <= 'Z'))) {
            return false;
        }

        for(int i = 1; i < value.length(); i++) {
            char c = value.charAt(i);
            if(!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9'))) {
                return false;
            }
        }

        return true;
    }

    public StareType getType() {
        return type;
    }
    public void setType(StareType type) {
        this.type = type;
    }

    @Override
    public String toString() {
        if(type == StareType.INITIAL) {
            return "Initial state: " + value;
        }
        else if(type == StareType.FINAL) {
            return "Final state: " + value;
        }
        return "State: " + value;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Stare state)) return false;
        return Objects.equals(getValue(), state.getValue()) ;
    }

    @Override
    public int hashCode() {
        return Objects.hash(getValue());
    }
}
