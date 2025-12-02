package org.example.AF;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class FileManager {
    public static AutomateFinite readAF(String path) throws IOException {
        //incerc sa accesez fisierul
        //daca nu exista => exceptie
        BufferedReader reader = null;
        try{
            reader = Files.newBufferedReader(Paths.get(path), StandardCharsets.UTF_8);
        }catch(FileNotFoundException e){
            e.printStackTrace();
        }
        //pe prima linie vor fi starile
        List<Stare> stareLista = new ArrayList<>();
        String line = reader.readLine();
        String[] stari = line.split(",");
        for(String stare: stari){
            stareLista.add(new Stare(stare));
        }

        //pe a doua linie va fi alfabetul
        List<Alfabet>  alfabetLista = new ArrayList<>();
        line = reader.readLine();
        String[] alfabets = line.split(",");
        for(String alfabet: alfabets){
            alfabetLista.add(new Alfabet(alfabet));
        }

        //pe a treia linie va fi stare initiala
        Stare stareinitiala = new Stare(reader.readLine().trim(), StareType.INITIAL);

        //pe a patra linie va fi starea finala
        List<Stare> starefinala = new ArrayList<>();
        line = reader.readLine();
        String[] starifinale = line.split(",");
        for(String starefinal: starifinale){
            starefinala.add(new Stare(starefinal, StareType.FINAL));
        }

        //pe urmatoarele liniii vor fi tranzitiile
        List<Tranzitie> tranzitii = new ArrayList<>();
        while((line = reader.readLine()) != null){
            tranzitii.add(Tranzitie.stringToTransition(line));
        }

        reader.close();
        return new AutomateFinite(stareinitiala,starefinala, tranzitii,stareLista,alfabetLista);
    }
}

