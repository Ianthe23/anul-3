#include <iostream>
#include <fstream>
#include "headers/LexicalAnalyzer.h"

using namespace std;

int main() {
    string inputPath;
    cout << "Introduceti calea catre fisierul sursa: ";
    getline(cin, inputPath);
    
    // Input from file
    ifstream input(inputPath);
    if (!input) {
        cerr << "Eroare: nu pot deschide fisierul '" << inputPath << "'\n";
        return 1;
    }
    
    LexicalAnalyzer analyzer;
    analyzer.analyze(input);
    
    analyzer.printFIP();
    analyzer.printSymbolTable();
    analyzer.printErrors();
    analyzer.demonstrateDirectAccess();
    
    return 0;
}