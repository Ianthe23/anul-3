#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <thread>
#include <limits>
#include <chrono>
using namespace std;

// Configuratii maxime pentru alocare statica
static const int MAXN = 10000;
static const int MAXM = 10000;
static const int MAXKH = 101; // înălțime nucleu (n)
static const int MAXKW = 101; // lățime nucleu (m)

// Dimensiuni citite din fisier
int N = 0, M = 0, KH = 0, KW = 0;
int P = 1;

// Matrici alocate static
int F[MAXN][MAXM];
int V[MAXN][MAXM];
int C[MAXKH][MAXKW];

// Citeste datele din 'date.txt' cu format:
// N M
// KH KW
// P
// (N linii) câte M întregi -> F
// (KH linii) câte KW întregi -> C
bool read_input(const string& path) {
    ifstream in(path);
    if (!in) {
        cerr << "Eroare: nu pot deschide fisierul de intrare '" << path << "'.\n";
        return false;
    }

    in >> N >> M;
    in >> KH >> KW;
    int p_in_file = 0;
    in >> p_in_file;
    if (!in) {
        cerr << "Eroare: fisierul nu contine dimensiuni valide sau p.\n";
        return false;
    }
    if (N <= 0 || M <= 0 || KH <= 0 || KW <= 0 || p_in_file <= 0) {
        cerr << "Eroare: dimensiuni nenule/negative sau p invalid.\n";
        return false;
    }
    if (N > MAXN || M > MAXM || KH > MAXKH || KW > MAXKW) {
        cerr << "Eroare: depasire limite alocare statica ("
             << "N<= " << MAXN << ", M<= " << MAXM << ", KH<= " << MAXKH << ", KW<= " << MAXKW << ").\n";
        return false;
    }
    P = p_in_file;

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            if (!(in >> F[i][j])) {
                cerr << "Eroare: valori insuficiente pentru matricea F.\n";
                return false;
            }
        }
    }

    for (int a = 0; a < KH; ++a) {
        for (int b = 0; b < KW; ++b) {
            if (!(in >> C[a][b])) {
                cerr << "Eroare: valori insuficiente pentru matricea C.\n";
                return false;
            }
        }
    }
    return true;
}

// Scrie rezultatul in 'output.txt':
// n m
// (n linii) câte m întregi -> V
void write_output(const string& path) {
    ofstream out(path);
    if (!out) {
        cerr << "Eroare: nu pot deschide fisierul de iesire '" << path << "'.\n";
        return;
    }
    out << N << " " << M << "\n";
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            out << V[i][j] << (j + 1 < M ? ' ' : '\n');
        }
    }
}

// Convolutia pentru o singură celulă (padding zero, ancoră la floor(KH/2), floor(KW/2))
inline int convolve_cell(int i, int j) {
    long long sum = 0;
    const int r_h = KH / 2; // offset pe înălțime
    const int r_w = KW / 2; // offset pe lățime

    for (int a = 0; a < KH; ++a) {
        int ii = i + a - r_h;
        if (ii < 0 || ii >= N) continue;
        for (int b = 0; b < KW; ++b) {
            int jj = j + b - r_w;
            if (jj < 0 || jj >= M) continue;
            sum += static_cast<long long>(F[ii][jj]) * C[a][b];
        }
    }

    if (sum > std::numeric_limits<int>::max()) return std::numeric_limits<int>::max();
    if (sum < std::numeric_limits<int>::min()) return std::numeric_limits<int>::min();
    return static_cast<int>(sum);
}

// Mod secvential
void convolve_seq() {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            V[i][j] = convolve_cell(i, j);
        }
    }
}

// Worker: pe interval de linii [startRow, endRow)
void convolve_rows_range(int startRow, int endRow) {
    for (int i = startRow; i < endRow; ++i) {
        for (int j = 0; j < M; ++j) {
            V[i][j] = convolve_cell(i, j);
        }
    }
}

// Worker: pe interval de coloane [startCol, endCol)
void convolve_cols_range(int startCol, int endCol) {
    for (int j = startCol; j < endCol; ++j) {
        for (int i = 0; i < N; ++i) {
            V[i][j] = convolve_cell(i, j);
        }
    }
}

// Paralel: descompunere pe orizontală (linii)
void run_parallel_horizontal(int p) {
    int blocks = std::min(p, N);
    if (blocks <= 0) return;

    vector<thread> threads;
    threads.reserve(blocks);

    int base = N / blocks;
    int rem  = N % blocks;
    int start = 0;

    for (int t = 0; t < blocks; ++t) {
        int len = base + (t < rem ? 1 : 0);
        int end = start + len;
        threads.emplace_back(convolve_rows_range, start, end);
        start = end;
    }
    for (auto& th : threads) th.join();
}

// Paralel: descompunere pe verticală (coloane)
void run_parallel_vertical(int p) {
    int blocks = std::min(p, M);
    if (blocks <= 0) return;

    vector<thread> threads;
    threads.reserve(blocks);

    int base = M / blocks;
    int rem  = M % blocks;
    int start = 0;

    for (int t = 0; t < blocks; ++t) {
        int len = base + (t < rem ? 1 : 0);
        int end = start + len;
        threads.emplace_back(convolve_cols_range, start, end);
        start = end;
    }
    for (auto& th : threads) th.join();
}

int main(int argc, char** argv) {
    ios::sync_with_stdio(false);
    auto t_all_start = chrono::steady_clock::now();

    if (argc < 2) {
        cerr << "Utilizare:\n"
             << "  " << argv[0] << " seq\n"
             << "  " << argv[0] << " par h|v [p]\n"
             << "  p este optional; daca lipseste se citeste din 'date.txt'.\n";
        return 1;
    }

    const string inputPath = "date.txt";
    const string outputPath = "output.txt";

    if (!read_input(inputPath)) {
        return 2;
    }

    const string mode = argv[1];
    if (mode == "seq") {
        auto t_comp_start = chrono::steady_clock::now();
        convolve_seq();
        auto t_comp_end = chrono::steady_clock::now();
        double ms = chrono::duration_cast<chrono::microseconds>(t_comp_end - t_comp_start).count() / 1000.0;
        cout << "Compute time [ms]: " << ms << "\n";
    } else if (mode == "par") {
        if (argc < 3) {
            cerr << "Eroare: lipsesc parametrii pentru modul paralel (h|v [p]).\n";
            return 3;
        }
        const string split = argv[2];
        int pForRun = P; // default: p din fisier
        if (argc >= 4) {
            try {
                int overrideP = stoi(argv[3]);
                if (overrideP > 0) pForRun = overrideP;
            } catch (...) {
                cerr << "Avertisment: p override invalid, folosesc p din fisier (" << P << ").\n";
            }
        }

        auto t_comp_start = chrono::steady_clock::now();
        if (split == "h") {
            run_parallel_horizontal(pForRun);
        } else if (split == "v") {
            run_parallel_vertical(pForRun);
        } else {
            cerr << "Eroare: al doilea argument trebuie sa fie 'h' sau 'v'.\n";
            return 3;
        }
        auto t_comp_end = chrono::steady_clock::now();
        double ms = chrono::duration_cast<chrono::microseconds>(t_comp_end - t_comp_start).count() / 1000.0;
        cout << "Compute time [ms]: " << ms << "\n";
    } else {
        cerr << "Eroare: mod necunoscut '" << mode << "'. Foloseste 'seq' sau 'par'.\n";
        return 1;
    }

    write_output(outputPath);
    auto t_all_end = chrono::steady_clock::now();
    double total_ms = chrono::duration_cast<chrono::microseconds>(t_all_end - t_all_start).count() / 1000.0;
    cout << "Total time [ms]: " << total_ms << "\n";
    return 0;
}