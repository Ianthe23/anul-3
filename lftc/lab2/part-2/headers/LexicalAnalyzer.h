#ifndef LEXICALANALYZER_H
#define LEXICALANALYZER_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_set>
#include <iomanip>
#include <cctype>
#include <algorithm>
#include "SymbolTable.h"
#include "FIP.h"

using namespace std;

class LexicalAnalyzer {
private:
    SymbolTable symbolTable;
    vector<FIPEntry> fip;
    vector<string> errors;
    vector<string> lines;
    
    void addToFIP(const string& tokenType, int code, const string& lexeme, int line, int col);
    void addError(const string& msg, int line, int col);
    static bool isLetter(char c);
    static bool isDigit(char c);
    void analyzeLine(const string& s, int lineNum);
    
public:
    void analyze(istream& input);
    void printFIP();
    void printSymbolTable();
    void printErrors();
    void demonstrateDirectAccess();
};

#endif