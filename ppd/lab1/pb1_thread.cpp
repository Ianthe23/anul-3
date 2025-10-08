#include <iostream>
#include <thread>
#include <chrono>
#include <cmath>

using namespace std;
using namespace chrono;

const int N = 1000000;
const int P = 8;
const int MAX_VAL = 100000;
int a[N], b[N], c[N], c_secv[N];

void init(int *v, int len) {
    for (int i = 0; i < len; i++) {
        v[i] = rand() % MAX_VAL;
    }
}

void sum(const int *a, const int *b, int *c, int len) {
    for (int i = 0; i < len; i++) {
        // c[i] = a[i] + b[i];
        c[i] = sqrt(a[i] * a[i] * a[i]) + b[i] * b[i];
    }
}

void sum_par(const int *a, const int *b, int *c, int start, int end) {
    for (int i = start; i < end; i++) {
        // c[i] = a[i] + b[i];
        c[i] = sqrt(a[i] * a[i] * a[i]) + b[i] * b[i];
    }
}

void start_thr(const int *a, const int *b, int *c, const int *c_secv) {
    int dim_thr = N / P;
    int rest = N % P;
    int start_index = 0;
    int end_index = dim_thr;

    thread thr[P];

    auto start_par = high_resolution_clock::now();
    for (int thr_id = 0; thr_id < P; thr_id++) {
        if (rest > 0) {
            end_index ++;
            rest --;
        }

        // cout << "thr_id: " << thr_id << ' ' << "start_index: " << start_index << ' ' << "end_index: " << end_index << '\n';
        thr[thr_id] = thread(sum_par, a, b, c, start_index, end_index);

        start_index = end_index;
        end_index += dim_thr;
    }

    for (int thr_id = 0; thr_id < P; thr_id++) {
        thr[thr_id].join();
    }
    auto end_par = high_resolution_clock::now();
    duration<double, micro> delta_time_par = end_par - start_par;
    cout << "delta_time_par: " << delta_time_par.count() << " us\n";



    bool ok = true;
    for (int i = 0; i < N; i++) {
        if (c_secv[i] != c[i]) {
            ok = false;
            cout << "err at: " << i << " expected:" << c_secv[i] << " got:" << c[i] << '\n';
            break;
        }
    }

    if(ok) {
        cout << "ok\n";
    }
}

int main() {
    auto start = high_resolution_clock::now();
    cout << "Hello World!" << '\n';

    init(a, N);
    init(b, N);

    auto start_secv = high_resolution_clock::now();
    sum(a, b, c_secv, N);
    auto end_secv = high_resolution_clock::now();
    duration<double, micro> delta_time_secv = end_secv - start_secv;
    cout << "delta_time_secv: " << delta_time_secv.count() << " us\n";

    for (int i = 0; i < 5; i++) {
        cout << "a: " << a[i] << ' ' << "b: " << b[i] << ' ' << "c_secv: " << c_secv[i] << '\n';
    }

    start_thr(a, b, c, c_secv);

    auto end = high_resolution_clock::now();
    duration<double, micro> delta_time = end - start;
    cout << "delta_time: " << delta_time.count() << " us\n";
    
    cout << '\n';

    int *a_dynamic = new int[N];
    int *b_dynamic = new int[N];
    int *c_dynamic = new int[N];

    int *all = new int[N * 3];

    for (int i = 0; i < N; i++) {
        a_dynamic[i] = a[i];
        b_dynamic[i] = b[i];
        all[i] = a[i];
        all[i + N] = b[i];
    }

    start_thr(a_dynamic, b_dynamic, c_dynamic, c_secv);
    start_thr(all, all + N, all + N * 2, c_secv);

    delete[] a_dynamic;
    delete[] b_dynamic;
    delete[] c_dynamic;
}