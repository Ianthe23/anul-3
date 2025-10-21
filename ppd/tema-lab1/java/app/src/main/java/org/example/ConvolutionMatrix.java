package org.example;

import java.io.*;
import java.util.*;

public class ConvolutionMatrix {
    private int N, M;           // Matrix F dimensions
    private int KH, KW;         // Kernel C dimensions (n x m)
    private int P;              // Number of threads from file
    
    private int[][] F;          // Input matrix N x M
    private int[][] V;          // Output matrix N x M
    private int[][] C;          // Convolution kernel KH x KW
    
    // Read input from date.txt with format:
    // N M
    // KH KW  
    // P
    // (N lines) M integers each -> F
    // (KH lines) KW integers each -> C
    public boolean readInput(String filePath) {
        try {
            Scanner scanner;
            File f = new File(filePath);
            if (f.exists()) {
                scanner = new Scanner(f);
            } else {
                InputStream is = ConvolutionMatrix.class.getResourceAsStream("/" + filePath);
                if (is == null) {
                    System.err.println("Eroare: nu pot gasi fisierul " + filePath + " nici in working dir, nici pe classpath.");
                    return false;
                }
                scanner = new Scanner(is);
            }

            N = scanner.nextInt();
            M = scanner.nextInt();
            KH = scanner.nextInt();
            KW = scanner.nextInt();
            P = scanner.nextInt();
            
            if (N <= 0 || M <= 0 || KH <= 0 || KW <= 0 || P <= 0) {
                System.err.println("Eroare: dimensiuni sau p invalid.");
                scanner.close();
                return false;
            }
            
            // Allocate matrices
            F = new int[N][M];
            V = new int[N][M];
            C = new int[KH][KW];
            
            // Read matrix F
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < M; j++) {
                    F[i][j] = scanner.nextInt();
                }
            }
            
            // Read kernel C
            for (int a = 0; a < KH; a++) {
                for (int b = 0; b < KW; b++) {
                    C[a][b] = scanner.nextInt();
                }
            }

            scanner.close();
            
            return true;
        } catch (FileNotFoundException e) {
            System.err.println("Eroare: nu pot deschide fisierul " + filePath);
            return false;
        } catch (Exception e) {
            System.err.println("Eroare: format invalid in fisier.");
            return false;
        }
    }
    
    // Write output to file
    public void writeOutput(String filePath) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filePath))) {
            writer.println(N + " " + M);
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < M; j++) {
                    writer.print(V[i][j]);
                    if (j < M - 1) writer.print(" ");
                }
                writer.println();
            }
        } catch (IOException e) {
            System.err.println("Eroare: nu pot scrie in fisierul " + filePath);
        }
    }
    
    // Convolution for a single cell (zero padding, anchor at floor(KH/2), floor(KW/2))
    private int convolveCell(int i, int j) {
        long sum = 0;
        int rH = KH / 2;  // height offset
        int rW = KW / 2;  // width offset
        
        for (int a = 0; a < KH; a++) {
            int ii = i + a - rH;
            if (ii < 0 || ii >= N) continue;
            
            for (int b = 0; b < KW; b++) {
                int jj = j + b - rW;
                if (jj < 0 || jj >= M) continue;
                
                sum += (long) F[ii][jj] * C[a][b];
            }
        }
        
        // Clamp to int range
        if (sum > Integer.MAX_VALUE) return Integer.MAX_VALUE;
        if (sum < Integer.MIN_VALUE) return Integer.MIN_VALUE;
        return (int) sum;
    }
    
    // Sequential convolution
    public void convolveSequential() {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < M; j++) {
                V[i][j] = convolveCell(i, j);
            }
        }
    }
    
    // Worker class for row-based parallelization
    private class RowWorker implements Runnable {
        private final int startRow, endRow;
        
        public RowWorker(int startRow, int endRow) {
            this.startRow = startRow;
            this.endRow = endRow;
        }
        
        @Override
        public void run() {
            for (int i = startRow; i < endRow; i++) {
                for (int j = 0; j < M; j++) {
                    V[i][j] = convolveCell(i, j);
                }
            }
        }
    }
    
    // Worker class for column-based parallelization
    private class ColWorker implements Runnable {
        private final int startCol, endCol;
        
        public ColWorker(int startCol, int endCol) {
            this.startCol = startCol;
            this.endCol = endCol;
        }
        
        @Override
        public void run() {
            for (int j = startCol; j < endCol; j++) {
                for (int i = 0; i < N; i++) {
                    V[i][j] = convolveCell(i, j);
                }
            }
        }
    }
    
    // Parallel convolution - horizontal decomposition (rows)
    public void convolveParallelHorizontal(int numThreads) throws InterruptedException {
        int blocks = Math.min(numThreads, N);
        if (blocks <= 0) return;
        
        Thread[] threads = new Thread[blocks];
        int base = N / blocks;
        int remainder = N % blocks;
        int start = 0;
        
        for (int t = 0; t < blocks; t++) {
            int length = base + (t < remainder ? 1 : 0);
            int end = start + length;
            threads[t] = new Thread(new RowWorker(start, end));
            threads[t].start();
            start = end;
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    // Parallel convolution - vertical decomposition (columns)
    public void convolveParallelVertical(int numThreads) throws InterruptedException {
        int blocks = Math.min(numThreads, M);
        if (blocks <= 0) return;
        
        Thread[] threads = new Thread[blocks];
        int base = M / blocks;
        int remainder = M % blocks;
        int start = 0;
        
        for (int t = 0; t < blocks; t++) {
            int length = base + (t < remainder ? 1 : 0);
            int end = start + length;
            threads[t] = new Thread(new ColWorker(start, end));
            threads[t].start();
            start = end;
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Utilizare:");
            System.err.println("  java ConvolutionMatrix seq");
            System.err.println("  java ConvolutionMatrix par h|v [p]");
            System.err.println("  p este optional; daca lipseste se citeste din 'date.txt'.");
            System.exit(1);
        }
        
        ConvolutionMatrix conv = new ConvolutionMatrix();
        String inputPath = "date.txt";
        String outputPath = "output.txt";
        
        long totalStart = System.nanoTime();
        
        if (!conv.readInput(inputPath)) {
            System.exit(2);
        }
        
        String mode = args[0];
        
        try {
            if ("seq".equals(mode)) {
                long computeStart = System.nanoTime();
                conv.convolveSequential();
                long computeEnd = System.nanoTime();
                double computeMs = (computeEnd - computeStart) / 1_000_000.0;
                System.out.println("Compute time [ms]: " + computeMs);
                
            } else if ("par".equals(mode)) {
                if (args.length < 2) {
                    System.err.println("Eroare: lipsesc parametrii pentru modul paralel (h|v [p]).");
                    System.exit(3);
                }
                
                String split = args[1];
                int pForRun = conv.P; // default: p from file
                
                if (args.length >= 3) {
                    try {
                        int overrideP = Integer.parseInt(args[2]);
                        if (overrideP > 0) pForRun = overrideP;
                    } catch (NumberFormatException e) {
                        System.err.println("Avertisment: p override invalid, folosesc p din fisier (" + conv.P + ").");
                    }
                }
                
                long computeStart = System.nanoTime();
                if ("h".equals(split)) {
                    conv.convolveParallelHorizontal(pForRun);
                } else if ("v".equals(split)) {
                    conv.convolveParallelVertical(pForRun);
                } else {
                    System.err.println("Eroare: al doilea argument trebuie sa fie 'h' sau 'v'.");
                    System.exit(3);
                }
                long computeEnd = System.nanoTime();
                double computeMs = (computeEnd - computeStart) / 1_000_000.0;
                System.out.println("Compute time [ms]: " + computeMs);
                
            } else {
                System.err.println("Eroare: mod necunoscut '" + mode + "'. Foloseste 'seq' sau 'par'.");
                System.exit(1);
            }
            
        } catch (InterruptedException e) {
            System.err.println("Eroare: thread-urile au fost intrerupte.");
            System.exit(4);
        }
        
        conv.writeOutput(outputPath);
        
        long totalEnd = System.nanoTime();
        double totalMs = (totalEnd - totalStart) / 1_000_000.0;
        System.out.println("Total time [ms]: " + totalMs);
    }
}
