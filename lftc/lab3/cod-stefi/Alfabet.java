package org.example.AF;

import java.util.Objects;

public class Alfabet {
    private String value;
    private static final String EPSILON ="ε";
    public Alfabet(String value) {
        if(isValid(value)){
            this.value = value;
        }
        else{
            throw new IllegalArgumentException("Invalid Alfabet value");
        }
    }

    public boolean isValid(String value) {
        //vf daca val. corespunde bnf
        //<symbol> ::= <caracter>
        //<caracter> ::= "a"|"b"| ... | "z" |"A"| ... |"Z"| "0"| ... | "9" | -
        if(value.equals(EPSILON)) {
            return true;
        }
        if(value.length() == 1 && (( value.charAt(0)=='-' )|| value.charAt(0) >= 'a' && value.charAt(0) <= 'z') || (value.charAt(0) >= '0' && value.charAt(0) <= '9') || (value.charAt(0)>='A' && value.charAt(0)<='Z') ) {
            return true;
        }
        return false;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        if(isValid(value)){
            this.value = value;
        }
        else{
            throw new IllegalArgumentException("Invalid Alfabet value");
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Alfabet alphabet)) return false;
        return Objects.equals(getValue(), alphabet.getValue());
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(getValue());
    }

    @Override
    public String toString() {
        return value;
    }
}
