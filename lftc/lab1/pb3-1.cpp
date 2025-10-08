#include <iostream>

using namespace std;

int main () {
    int nr = 10;
    int sum = 0;
    int 0abc;

    while (nr !==  0) {
        sum = sum + nr % 10;
        nr = nr / 10;
    }

    cout << sum;
    cout << '\n';
}