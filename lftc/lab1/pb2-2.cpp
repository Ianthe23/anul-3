#include <iostream>

using namespace std;

int main() {
    int a; 
    int b;
    cout << "Enter the two integers: ";
    cin >> a;
    cin >> b;

    int rest = 0;
    while (b != 0) {
        rest = a % b;
        a = b;
        b = rest;
    }

    cout << "The CMMDC of the two integers is: ";
    cout << a;
    cout << '\n';
}