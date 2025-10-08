#include <iostream>

using namespace std;

struct Circle {
    float radius;
} circle;
// The perimeter and the area of a circle with a given radius
int main() {
    float pi = 3.14;
    cout << "Enter the radius of the circle: ";
    cin >> circle.radius;

    float perimeter = 2 * pi * circle.radius;
    cout << "The perimeter of the circle is: ";
    cout << perimeter; 
    cout << '\n';

    float area = pi * circle.radius * circle.radius;
    cout << "The area of the circle is: ";
    cout << area;
    cout << '\n';
}