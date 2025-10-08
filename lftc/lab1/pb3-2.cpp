#include <iostream>

using namespace std;

int main() {
    int nr = 10;
    cout << "Numarul este: " << nr; // Eroare in MLP - nu se poate folosi operatorul de afisare pentru mai multe variabile
    cout << " ";

    int a = 4;
    a += nr; // Eroare in MLP - nu exista operatorul += pentru tipul de date int
    cout << "Suma dintre a si nr este: " << a << '\n'; // Eroare in MLP - nu se poate folosi operatorul de afisare pentru mai multe variabile
}