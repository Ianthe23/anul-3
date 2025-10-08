#include <iostream>

using namespace std;

const int N = 100;
const int MAX_VAL = 100000;
int a[N], b[N], c[N], c_secv[N];

void init(int *v, int len) {
    for (int i = 0; i < len; i++) {
        v[i] = rand() % MAX_VAL;
    }
}

void sum(const int *a, const int *b, int *c, int len) {
    for (int i = 0; i < len; i++) {
        c[i] = a[i] + b[i];
    }
}

int main() {
    cout << "Hello World!" << '\n';

    init(a, N);
    init(b, N);

    sum(a, b, c, N);

    for (int i = 0; i < 5; i++) {
        cout << "a: " << a[i] << ' ' << "b: " << b[i] << ' ' << "c: " << c[i] << '\n';
    }
}