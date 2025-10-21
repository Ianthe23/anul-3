#include "headers/LexicalAnalyzer.h"

// Cuvinte cheie predefinite
static const unordered_set<string> KEYWORDS = {
    "include","iostream","using","namespace","std",
    "cout","cin","main","while","return","int",
    "struct","double","if","else","float","char","for","do"
};

// Operatori
static const unordered_set<string> MULTI_OP = { ">>", "<<", "==", "!=" };
static const string SINGLE_OP = "+-=*/%><";
static const string SEPS = ",;(){}.";

void LexicalAnalyzer::addToFIP(const string& tokenType, int code, const string& lexeme, int line, int col) {
    FIPEntry entry;
    entry.tokenType = tokenType;
    entry.code = code;
    entry.line = line;
    entry.col = col;
    entry.symbolTableIndex = -1;
    
    // Adauga in tabela de simboluri doar identificatorii si constantele
    if (tokenType == "IDENTIFIER" || tokenType == "CONSTANT_INT") {
        int symbolIndex = symbolTable.addSymbol(lexeme);
        // if (symbolIndex == -1 && tokenType == "IDENTIFIER") {
        //     addError("Identificator prea lung (max 8 caractere): " + lexeme, line, col);
        //     return;
        // }
        entry.symbolTableIndex = symbolIndex;
    }
    
    fip.push_back(entry);
}

void LexicalAnalyzer::addError(const string& msg, int line, int col) {
    errors.push_back("Eroare lexicala la (linia " + to_string(line) + ", coloana " + to_string(col) + "): " + msg);
}

bool LexicalAnalyzer::isLetter(char c) { 
    return std::isalpha((unsigned char)c); 
}

bool LexicalAnalyzer::isDigit(char c) { 
    return std::isdigit((unsigned char)c); 
}

void LexicalAnalyzer::analyzeLine(const string& s, int lineNum) {
    int i = 0, n = s.size();
    
    while (i < n) {
        char c = s[i];
        int col = i + 1;
        
        // Sari peste spatii
        if (std::isspace((unsigned char)c)) {
            ++i;
            continue;
        }
        
        // Comentarii
        if (c == '/' && i + 1 < n && s[i + 1] == '/') {
            break;
        }
        
        // String-uri
        if (c == '"') {
            int j = i + 1;
            bool closed = false;
            while (j < n) {
                if (s[j] == '"') {
                    closed = true;
                    ++j;
                    break;
                }
                ++j;
            }
            string lex = s.substr(i, j - i);
            if (!closed) {
                addError("String neterminat", lineNum, col);
            }
            addToFIP("STRING", STRING_CODE, lex, lineNum, col);
            i = j;
            continue;
        }
        
        // Operatori multi-caracter
        if (i + 1 < n) {
            string two = s.substr(i, 2);
            if (MULTI_OP.count(two)) {
                addToFIP("OPERATOR", OPERATOR_CODE, two, lineNum, col);
                i += 2;
                continue;
            }
        }
        
        // Operatori single-caracter
        if (SINGLE_OP.find(c) != string::npos) {
            addToFIP("OPERATOR", OPERATOR_CODE, string(1, c), lineNum, col);
            ++i;
            continue;
        }
        
        // Separatori
        if (SEPS.find(c) != string::npos) {
            addToFIP("SEPARATOR", SEPARATOR_CODE, string(1, c), lineNum, col);
            ++i;
            continue;
        }
        
        // Hash
        if (c == '#') {
            addToFIP("HASH", HASH_CODE, "#", lineNum, col);
            ++i;
            continue;
        }
        
        // Constante numerice
        if (isDigit(c)) {
            int j = i;
            while (j < n && isDigit(s[j])) ++j;
            string lex = s.substr(i, j - i);
            addToFIP("CONSTANT_INT", CONSTANT_CODE, lex, lineNum, col);
            i = j;
            continue;
        }
        
        // Identificatori si cuvinte cheie
        if (isLetter(c) || c == '_') {
            int j = i;
            while (j < n && (isLetter(s[j]) || isDigit(s[j]) || s[j] == '_')) ++j;
            string lex = s.substr(i, j - i);
            string lower = lex;
            transform(lower.begin(), lower.end(), lower.begin(), 
                     [](unsigned char ch) { return (char)tolower(ch); });
            
            if (KEYWORDS.count(lower)) {
                addToFIP("KEYWORD", KEYWORD_CODE, lower, lineNum, col);
            } else {
                addToFIP("IDENTIFIER", IDENTIFIER_CODE, lex, lineNum, col);
            }
            i = j;
            continue;
        }
        
        // Caracter necunoscut
        addError(string("Caracter necunoscut '") + c + "'", lineNum, col);
        ++i;
    }
}

void LexicalAnalyzer::analyze(istream& input) {
    lines.clear();
    fip.clear();
    errors.clear();
    
    string line;
    while (getline(input, line)) {
        lines.push_back(line);
    }
    
    for (int i = 0; i < lines.size(); ++i) {
        analyzeLine(lines[i], i + 1);
    }
}

void LexicalAnalyzer::printFIP() {
    // Output to console
    cout << "\n=== FORMA INTERNA A PROGRAMULUI (FIP) ===\n";
    cout << left << setw(15) << "TIP TOKEN" << setw(8) << "COD" 
         << setw(12) << "INDEX TS" << setw(8) << "LINIA" << "COLOANA" << '\n';
    cout << string(60, '-') << '\n';
    
    for (const auto& entry : fip) {
        cout << left << setw(15) << entry.tokenType 
             << setw(8) << entry.code;
        
        if (entry.symbolTableIndex != -1) {
            cout << setw(12) << entry.symbolTableIndex;
        } else {
            cout << setw(12) << "-";
        }
        
        cout << setw(8) << entry.line << entry.col << '\n';
    }
    
    // Output to file
    ofstream fipFile("output/out-fip.txt");
    if (fipFile) {
        fipFile << "=== FORMA INTERNA A PROGRAMULUI (FIP) ===\n";
        fipFile << left << setw(15) << "TIP TOKEN" << setw(8) << "COD" 
                << setw(12) << "INDEX TS" << setw(8) << "LINIA" << "COLOANA" << '\n';
        fipFile << string(60, '-') << '\n';
        
        for (const auto& entry : fip) {
            fipFile << left << setw(15) << entry.tokenType 
                    << setw(8) << entry.code;
            
            if (entry.symbolTableIndex != -1) {
                fipFile << setw(12) << entry.symbolTableIndex;
            } else {
                fipFile << setw(12) << "-";
            }
            
            fipFile << setw(8) << entry.line << entry.col << '\n';
        }
        fipFile.close();
        cout << "\nFIP salvat in fisierul 'out-fip.txt'\n";
    } else {
        cout << "\nEroare: nu pot crea fisierul 'out-fip.txt'\n";
    }
}

void LexicalAnalyzer::printSymbolTable() {
    // Output to console
    cout << "\n=== TABELA DE SIMBOLURI (TS) ===\n";
    cout << left << setw(10) << "INDEX" << "SIMBOL" << '\n';
    cout << string(30, '-') << '\n';
    
    auto symbols = symbolTable.getAllSymbols();
    for (const auto& symbol : symbols) {
        cout << left << setw(10) << symbol.second << symbol.first << '\n';
    }
    
    // Output to file
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

void LexicalAnalyzer::printErrors() {
    if (!errors.empty()) {
        cout << "\n=== ERORI LEXICALE (" << errors.size() << ") ===\n";
        for (const auto& error : errors) {
            cout << error << '\n';
        }
    }
}

void LexicalAnalyzer::demonstrateDirectAccess() {
    cout << "\n=== DEMONSTRARE ACCES theta(1) LA TS ===\n";
    cout << "Accesul la simboluri pe baza indexului din FIP:\n";
    
    for (const auto& entry : fip) {
        if (entry.symbolTableIndex != -1) {
            string symbol = symbolTable.getSymbolByIndex(entry.symbolTableIndex);
            cout << "Index " << entry.symbolTableIndex << " -> Simbol: '" 
                 << symbol << "' (linia " << entry.line << ")\n";
        }
    }
}