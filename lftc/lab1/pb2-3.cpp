#include <iostream>

using namespace std;

int main() {
    int n;
    cout << "Enter the length of the sequence: ";
    cin >> n;

    int sum = 0;
    int number;
    while (n != 0) {
        cout << "Enter the number: ";
        cin >> number;
        sum = sum + number;
        n = n - 1;
    }

    cout << "The sum of the sequence is: ";
    cout << sum;
    cout << '\n';
}