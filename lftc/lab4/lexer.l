/* lab2/part-2/lexer.l */
/* %option noyywrap tells Flex not to call yywrap at EOF; scanning ends without extra hooks. */
/* %option yylineno tells Flex to keep track of line numbers. */
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
    "struct","double","if","else","float","char","for","do",
    "then","endif"
};

static const string SINGLE_OP = "+-=*/%><";

SymbolTable symbolTable;
vector<FIPEntry> fip;
vector<string> errors;

int column = 1;

void addToFIP(const string& tokenType, int code, int line, int col, const string& lexeme);
void addError(const string& msg, int line, int col);
void updateIfFSM(const string& tokenType, const string& lexeme, int line, int col);
void printFIP();
void printSymbolTable();
void printErrors();

%}
%%

[ \t\r]+   { 
    /* Spatii albe */ 
    column += yyleng; 
}

\n         { 
    /* Newline */
    column = 1;
}


\/\/[^\n]*     { 
    /* Comentariu linie */
    column += yyleng; 
}


\"([^\"\\\n]|\\.)*\" {
    /* String */
    int start_col = column;
    column += yyleng;
    addToFIP("STRING", STRING_CODE, yylineno, start_col, string(yytext, yyleng));
}


\"([^\"\n]|\\.)*[\n] {
    /* String neterminat */
    int start_col = column;
    /* consumam tot; resetam col daca contine \\n */
    column = 1;
    addError("String neterminat", yylineno, start_col);
    addToFIP("STRING", STRING_CODE, yylineno, start_col, string(yytext, yyleng));
}


>>|<<|==|!= {
    /* Operator */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("OPERATOR", OPERATOR_CODE, yylineno, start_col, lex);
}


[+\-=\*/%><] {
    /* Operator */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("OPERATOR", OPERATOR_CODE, yylineno, start_col, lex);
}


[,;(){}.] {
    /* Separatoare */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("SEPARATOR", SEPARATOR_CODE, yylineno, start_col, lex);
}


# {
    /* Hash */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("HASH", HASH_CODE, yylineno, start_col, lex);
}


[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?[fFlL]? {
    /* Constant Real */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("CONSTANT_REAL", CONSTANT_CODE, yylineno, start_col, lex);
}

0[xX][0-9a-fA-F]+([uUlL]{1,3})? {
    /* Constant Int (Hex) */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("CONSTANT_INT", CONSTANT_CODE, yylineno, start_col, lex);
}

0[bB][01]+([uUlL]{1,3})? {
    /* Constant Int (Binary) */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("CONSTANT_INT", CONSTANT_CODE, yylineno, start_col, lex);
}

0[0-7]+([uUlL]{1,3})? {
    /* Constant Int (Octal) */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("CONSTANT_INT", CONSTANT_CODE, yylineno, start_col, lex);
}

[0-9]+([uUlL]{1,3})? {
    /* Constant Int (Decimal) */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    addToFIP("CONSTANT_INT", CONSTANT_CODE, yylineno, start_col, lex);
}


[a-zA-Z_][a-zA-Z0-9_]* {
    /* Identifier sau Keyword */
    int start_col = column;
    string lex(yytext, yyleng);
    column += yyleng;
    string lower = lex;
    transform(lower.begin(), lower.end(), lower.begin(), [](unsigned char ch){ return (char)tolower(ch); });
    if (KEYWORDS.count(lower)) {
        addToFIP("KEYWORD", KEYWORD_CODE, yylineno, start_col, lower);
    } else {
        addToFIP("IDENTIFIER", IDENTIFIER_CODE, yylineno, start_col, lex);
    }
}


. {
    /* Caracter necunoscut */
    int start_col = column;
    column += yyleng;
    addError(string("Caracter necunoscut '") + string(yytext, yyleng) + "'", yylineno, start_col);
}


%%

void addToFIP(const string& tokenType, int code, int line, int col, const string& lexeme) {
    FIPEntry entry;
    entry.tokenType = tokenType;
    entry.code = code;
    entry.line = line;
    entry.col = col;
    entry.symbolTableIndex = -1;
    if (tokenType == "IDENTIFIER") {
        string lowerLex = lexeme;
        transform(lowerLex.begin(), lowerLex.end(), lowerLex.begin(), [](unsigned char ch){ return (char)tolower(ch); });
        if (!KEYWORDS.count(lowerLex)) {
            int idx = symbolTable.addSymbol(lexeme);
            entry.symbolTableIndex = idx;
        }
    } else if (tokenType == "CONSTANT_INT") {
        int idx = symbolTable.addSymbol(lexeme);
        entry.symbolTableIndex = idx;
    }
    fip.push_back(entry);
    updateIfFSM(tokenType, lexeme, line, col);
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

static int if_state = 0;
static int if_start_line = 0;
static int if_start_col = 0;
static int if_ok_count = 0;

void updateIfFSM(const string& tokenType, const string& lexeme, int line, int col) {
    switch (if_state) {
        case 0:
            if (tokenType == "KEYWORD" && lexeme == "if") {
                if_state = 1;
                if_start_line = line;
                if_start_col = col;
            }
            break;
        case 1:
            if (tokenType == "SEPARATOR" && lexeme == "(") {
                if_state = 2;
            } else {
                addError("Se astepta '(' dupa 'if'", line, col);
                if_state = 0;
            }
            break;
        case 2:
            if (tokenType == "IDENTIFIER") {
                if_state = 3;
            } else {
                addError("Se astepta IDENTIFIER in 'if (...)'", line, col);
                if_state = 0;
            }
            break;
        case 3:
            if (tokenType == "SEPARATOR" && lexeme == ")") {
                if_state = 4;
            } else {
                addError("Se astepta ')' dupa 'if (ID'", line, col);
                if_state = 0;
            }
            break;
        case 4:
            if (tokenType == "KEYWORD" && lexeme == "then") {
                if_state = 5;
            } else {
                addError("Se astepta 'then' dupa 'if (ID)'", line, col);
                if_state = 0;
            }
            break;
        case 5:
            if (tokenType == "KEYWORD" && lexeme == "endif") {
                if_ok_count++;
                if_state = 0;
            }
            break;
        case 6:
            if_state = 0;
            break;
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

    /* Lexer - generare FIP */
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