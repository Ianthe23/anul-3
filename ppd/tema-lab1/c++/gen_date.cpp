#include <iostream>
#include <fstream>
#include <random>
using namespace std;

static const int MAX_ABS_F = 9;
static const int MAX_ABS_C = 3;

int main(int argc, char** argv) {
    if (argc < 6) {
        cerr << "Usage: " << argv[0] << " N M n m p [seed]\n";
        return 1;
    }
    int N = stoi(argv[1]), M = stoi(argv[2]);
    int n = stoi(argv[3]), m = stoi(argv[4]);
    int p = stoi(argv[5]);
    int seed = (argc >= 7) ? stoi(argv[6]) : 123456;

    if (N <= 0 || M <= 0 || n <= 0 || m <= 0 || p <= 0) {
        cerr << "Dimensions and p must be > 0.\n";
        return 1;
    }

    mt19937 rng(seed);
    uniform_int_distribution<int> distF(-MAX_ABS_F, MAX_ABS_F);
    uniform_int_distribution<int> distC(-MAX_ABS_C, MAX_ABS_C);

    ofstream out("date.txt");
    out << N << " " << M << "\n";
    out << n << " " << m << "\n";
    out << p << "\n";

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            out << distF(rng) << (j + 1 < M ? ' ' : '\n');
        }
    }
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            out << distC(rng) << (j + 1 < m ? ' ' : '\n');
        }
    }
    cerr << "Wrote date.txt (N=" << N << ", M=" << M
         << ", n=" << n << ", m=" << m << ", p=" << p
         << ", seed=" << seed
         << ", ranges F=[-" << MAX_ABS_F << "," << MAX_ABS_F
         << "], C=[-" << MAX_ABS_C << "," << MAX_ABS_C << "])\n";
    return 0;
}