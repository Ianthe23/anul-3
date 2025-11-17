/* lab2/part-2/lexer.l */
%option noyywrap
%option yylineno

%{
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
#include <unordered_set>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <iomanip>
#include "../lab2/part-2/headers/FIP.h"
#include "../lab2/part-2/headers/SymbolTable.h"

using namespace std;

static const unordered_set<string> KEYWORDS = {
    "include","iostream","using","namespace","std",
    "cout","cin","main","while","return","int",
    "struct","double","if","else","float","char","for","do"
};

static const string SINGLE_OP = "+-=*/%><";

SymbolTable symbolTable;
vector<FIPEntry> fip;
vector<string> errors;

int column = 1;

void addToFIP(const string& tokenType, int code, int line, int col, const string& lexeme = "");
void addError(const string& msg, int line, int col);
void printFIP();
void printSymbolTable();
void printErrors();

%}
%%

/* Spatii albe */
[ \t\r]+   { column += yyleng; }

/* Newline */
\n         { column = 1; }

/* Comentariu //... */
\/\/[^\n]*     { column += yyleng; }

/* String inchis: permite escape-uri, fara newline */
\"([^\"\\\n]|\\.)*\" {
    int start_col = column;
    column += yyleng;
    addToFIP("STRING", STRING_CODE, yylineno, start_col, string(yytext, yyleng));
}

/* String neterminat: ajunge la newline sau EOF fara " */
\"([^\"\n]|\\.)*[\n] {
    int start_col = column;
    /* consumam tot; resetam col daca contine \\n */
    column = 1;
    addError("String neterminat", yylineno, start_col);
    addToFIP("STRING", STRING_CODE, yylineno, start_col, string(yytext, yyleng));
}

/* Operatori multi-caracter */
>>|<<|==|!= {
    int start_col = column;
    column += yyleng;
    addToFIP("OPERATOR", OPERATOR_CODE, yylineno, start_col);
}

/* Operatori single-caracter */
[+\-=\*/%><] {
    int start_col = column;
    column += yyleng;
    addToFIP("OPERATOR", OPERATOR_CODE, yylineno, start_col);
}

/* Separatori */
[,;(){}.] {
    int start_col = column;
    column += yyleng;
    addToFIP("SEPARATOR", SEPARATOR_CODE, yylineno, start_col);
}

/* Hash (preprocesor) */
# {
    int start_col = column;
    column += yyleng;
    addToFIP("HASH", HASH_CODE, yylineno, start_col);
}

/* Constante intregi (zecimale) */
[0-9]+ {
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("CONSTANT_INT", CONSTANT_CODE, yylineno, start_col, lex);
}

/* Identificatori si cuvinte-cheie (case-insensitive pentru keywords) */
[a-zA-Z_][a-zA-Z0-9_]* {
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    string lower = lex;
    transform(lower.begin(), lower.end(), lower.begin(), [](unsigned char ch){ return (char)tolower(ch); });
    if (KEYWORDS.count(lower)) {
        addToFIP("KEYWORD", KEYWORD_CODE, yylineno, start_col);
    } else {
        addToFIP("IDENTIFIER", IDENTIFIER_CODE, yylineno, start_col, lex);
    }
}

/* Caracter necunoscut */
. {
    int start_col = column;
    column += yyleng;
    addError(string("Caracter necunoscut '") + string(yytext, yyleng) + "'", yylineno, start_col);
}

/* User code: main */
%%

void addToFIP(const string& tokenType, int code, int line, int col, const string& lexeme) {
    FIPEntry entry;
    entry.tokenType = tokenType;
    entry.code = code;
    entry.line = line;
    entry.col = col;
    entry.symbolTableIndex = -1;
    if (tokenType == "IDENTIFIER" || tokenType == "CONSTANT_INT") {
        int idx = symbolTable.addSymbol(lexeme);
        entry.symbolTableIndex = idx;
    }
    fip.push_back(entry);
}

void addError(const string& msg, int line, int col) {
    errors.push_back("Eroare lexicala la (linia " + to_string(line) + ", coloana " + to_string(col) + "): " + msg);
}

void printFIP() {
    cout << "\n=== FORMA INTERNA A PROGRAMULUI (FIP) ===\n";
    cout << left << setw(15) << "TIP TOKEN" << setw(8) << "COD"
         << setw(12) << "INDEX TS" << setw(8) << "LINIA" << "COLOANA" << '\n';
    cout << string(60, '-') << '\n';
    for (const auto& entry : fip) {
        cout << left << setw(15) << entry.tokenType
             << setw(8) << entry.code
             << setw(12) << (entry.symbolTableIndex != -1 ? to_string(entry.symbolTableIndex) : string("-"))
             << setw(8) << entry.line << entry.col << '\n';
    }
    ofstream fipFile("output/out-fip.txt");
    if (fipFile) {
        fipFile << "=== FORMA INTERNA A PROGRAMULUI (FIP) ===\n";
        fipFile << left << setw(15) << "TIP TOKEN" << setw(8) << "COD"
                << setw(12) << "INDEX TS" << setw(8) << "LINIA" << "COLOANA" << '\n';
        fipFile << string(60, '-') << '\n';
        for (const auto& entry : fip) {
            fipFile << left << setw(15) << entry.tokenType
                    << setw(8) << entry.code
                    << setw(12) << (entry.symbolTableIndex != -1 ? to_string(entry.symbolTableIndex) : string("-"))
                    << setw(8) << entry.line << entry.col << '\n';
        }
        fipFile.close();
        cout << "\nFIP salvat in fisierul 'out-fip.txt'\n";
    } else {
        cout << "\nEroare: nu pot crea fisierul 'out-fip.txt'\n";
    }
}

void printSymbolTable() {
    cout << "\n=== TABELA DE SIMBOLURI (TS) ===\n";
    cout << left << setw(10) << "INDEX" << "SIMBOL" << '\n';
    cout << string(30, '-') << '\n';
    auto symbols = symbolTable.getAllSymbols();
    for (const auto& symbol : symbols) {
        cout << left << setw(10) << symbol.second << symbol.first << '\n';
    }
    ofstream tsFile("output/out-ts.txt");
    if (tsFile) {
        tsFile << "=== TABELA DE SIMBOLURI (TS) ===\n";
        tsFile << left << setw(10) << "INDEX" << "SIMBOL" << '\n';
        tsFile << string(30, '-') << '\n';
        for (const auto& symbol : symbols) {
            tsFile << left << setw(10) << symbol.second << symbol.first << '\n';
        }
        tsFile.close();
        cout << "\nTS salvat in fisierul 'out-ts.txt'\n";
    } else {
        cout << "\nEroare: nu pot crea fisierul 'out-ts.txt'\n";
    }
}

void printErrors() {
    if (!errors.empty()) {
        cout << "\n=== ERORI LEXICALE (" << errors.size() << ") ===\n";
        for (const auto& e : errors) cout << e << '\n';
    } else {
        cout << "\n=== Analiza lexicala reusita (fara erori) ===\n";
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string inputPath;
    cout << "Introduceti calea catre fisierul sursa: ";
    getline(cin, inputPath);

    FILE* f = fopen(inputPath.c_str(), "r");
    if (!f) {
        cerr << "Eroare: nu pot deschide fisierul '" << inputPath << "'\n";
        return 1;
    }
    yyin = f;

    yylex();

    fclose(f);

    printFIP();
    printSymbolTable();
    printErrors();

    // Demonstratie acces theta(1) la TS
    cout << "\n=== DEMONSTRARE ACCES theta(1) LA TS ===\n";
    cout << "Accesul la simboluri pe baza indexului din FIP:\n";
    for (const auto& entry : fip) {
        if (entry.symbolTableIndex != -1) {
            string symbol = symbolTable.getSymbolByIndex(entry.symbolTableIndex);
            cout << "Index " << entry.symbolTableIndex << " -> Simbol: '"
                 << symbol << "' (linia " << entry.line << ")\n";
        }
    }

    return 0;
}
