package org.example;

import java.io.*;
import java.util.Random;

public class GenerateData {
    private static final int MAX_ABS_F = 9;
    private static final int MAX_ABS_C = 3;
    
    public static void main(String[] args) {
        if (args.length < 5) {
            System.err.println("Utilizare: java GenerateData N M n m p [seed]");
            System.err.println("  N, M: dimensiuni matrice F");
            System.err.println("  n, m: dimensiuni kernel C");
            System.err.println("  p: numar thread-uri");
            System.err.println("  seed: optional, pentru reproducibilitate");
            System.exit(1);
        }
        
        try {
            int N = Integer.parseInt(args[0]);
            int M = Integer.parseInt(args[1]);
            int n = Integer.parseInt(args[2]);
            int m = Integer.parseInt(args[3]);
            int p = Integer.parseInt(args[4]);
            
            if (N <= 0 || M <= 0 || n <= 0 || m <= 0 || p <= 0) {
                System.err.println("Eroare: toate dimensiunile si p trebuie sa fie pozitive.");
                System.exit(2);
            }
            
            long seed = System.currentTimeMillis();
            if (args.length >= 6) {
                seed = Long.parseLong(args[5]);
            }
            Random rand = new Random(seed);
            
            // Write directly to app/src/main/resources/date.txt
            java.nio.file.Path resourcesDir = java.nio.file.Paths.get("src", "main", "resources");
            try {
                java.nio.file.Files.createDirectories(resourcesDir);
            } catch (java.io.IOException e) {
                System.err.println("Eroare: nu pot crea directorul de resurse: " + resourcesDir.toAbsolutePath());
                System.exit(3);
            }
            java.nio.file.Path outputPath = resourcesDir.resolve("date.txt");

            try (PrintWriter writer = new PrintWriter(new FileWriter(outputPath.toFile()))) {
                // Write dimensions and thread count
                writer.println(N + " " + M);
                writer.println(n + " " + m);
                writer.println(p);

                // Generate matrix F
                for (int i = 0; i < N; i++) {
                    for (int j = 0; j < M; j++) {
                        int val = rand.nextInt(2 * MAX_ABS_F + 1) - MAX_ABS_F;
                        writer.print(val);
                        if (j < M - 1) writer.print(" ");
                    }
                    writer.println();
                }

                // Generate kernel C
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < m; j++) {
                        int val = rand.nextInt(2 * MAX_ABS_C + 1) - MAX_ABS_C;
                        writer.print(val);
                        if (j < m - 1) writer.print(" ");
                    }
                    writer.println();
                }

                System.out.println("Generated date.txt at: " + outputPath.toAbsolutePath());
                System.out.println("  Matrix F: " + N + "x" + M + " (range [-" + MAX_ABS_F + ", " + MAX_ABS_F + "])");
                System.out.println("  Kernel C: " + n + "x" + m + " (range [-" + MAX_ABS_C + ", " + MAX_ABS_C + "])");
                System.out.println("  Threads: " + p);
                System.out.println("  Seed: " + seed);

            } catch (IOException e) {
                System.err.println("Eroare: nu pot scrie fisierul " + outputPath);
                System.exit(3);
            }
            
        } catch (NumberFormatException e) {
            System.err.println("Eroare: argumentele trebuie sa fie numere intregi valide.");
            System.exit(2);
        }
    }
}