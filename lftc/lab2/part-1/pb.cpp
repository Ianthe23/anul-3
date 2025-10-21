#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_set>
#include <iomanip>
#include <cctype>
#include <algorithm>

using namespace std;

struct Token {
    string type;
    string lexeme;
    int line;
    int col;
};

static const unordered_set<string> KEYWORDS = {
    "include","iostream","using","namespace","std",
    "cout","cin","main","while","return","int",
    "struct","double","if","else","float","char","for","do"
};

static const unordered_set<string> MULTI_OP = { ">>", "<<", "==", "!=" };
static const string SINGLE_OP = "+-=*/%><";
static const string SEPS = ",;(){}.";

struct Lexer {
    vector<string> lines;
    
    vector<Token> tokens;
    vector<string> errors;

    void addTok(string t, string lx, int ln, int col) { 
        tokens.push_back({t,lx,ln,col}); 
    }

    void addErr(string msg, int ln, int col) {
        errors.push_back("Eroare lexicala la linia " + to_string(ln) + ", coloana " + to_string(col) + ": " + msg); 
    }

    static bool isLetter(char c) {
        return std::isalpha((unsigned char)c); 
    }
    static bool isDigit(char c) {
        return std::isdigit((unsigned char)c); 
    }

    void lexLine(const string& s, int ln){
        int i = 0, n = s.size();
        while (i < n) {
            char c = s[i]; int col = (int)i + 1;
            if (std::isspace((unsigned char)c)) { 
                ++i; continue; 
            }

            if (c == '/' && i+1 < n && s[i+1] == '/') 
                break;

            if (c == '"') {
                int j = i+1; bool closed=false;
                while(j < n) { 
                    if (s[j] == '"'){ closed = true; ++j; break; } ++j; 
                }
                string lex = s.substr(i, j-i);
                if (!closed) addErr("Literal de string neinchis", ln, col);
                addTok("STRING", lex, ln, col);
                i = j; continue;
            }

            if (i+1 < n) {
                string two = s.substr(i,2);
                if (MULTI_OP.count(two)) { 
                    addTok("OPERATOR", two, ln, col); i += 2; continue; 
                }
            }

            if (SINGLE_OP.find(c) != string::npos){ 
                addTok("OPERATOR", string(1,c), ln, col); ++i; continue; 
            }

            if (SEPS.find(c) != string::npos){ 
                addTok("SEPARATOR", string(1,c), ln, col); ++i; continue; 
            }

            if (c == '#'){ 
                addTok("HASH", "#", ln, col); ++i; continue; 
            }

            if (isDigit(c)){
                int j = i; while (j < n && isDigit(s[j])) ++j;
                addTok("CONSTANT_INT", s.substr(i, j-i), ln, col);
                i = j; continue;
            }

            if (isLetter(c) || c == '_'){
                int j = i; 
                while(j < n && (isLetter(s[j]) || isDigit(s[j]) || s[j]=='_')) 
                    ++j;
                string lex = s.substr(i, j-i);

                string lower = lex; 
                transform(lower.begin(), lower.end(), lower.begin(), [](unsigned char ch){ return (char)tolower(ch); });

                if (KEYWORDS.count(lower)) addTok("KEYWORD", lower, ln, col);
                else addTok("IDENTIFIER", lex, ln, col);
                i = j; continue;
            }

            addErr(string("Caracter necunoscut '") + c + "'", ln, col);
            ++i;
        }
    }

    void run(istream& in){
        lines.clear(); tokens.clear(); errors.clear();
        string s; 
        while (getline(in,s)) 
            lines.push_back(s);

        for (int k = 0; k < lines.size(); ++k) 
            lexLine(lines[k], (int)k+1);
    }
};

int main() {

    string inPath;
    cout << "Introduceti calea catre fisierul sursa: ";
    getline(cin, inPath);

    ifstream fin(inPath);
    if (!fin) {
         cerr << "Eroare: nu se poate deschide fisierul '"<<inPath<<"'\n"; return 1;
    }

    Lexer L; L.run(fin);

    cout << left << setw(16) << "TYPE" << setw(24) << "LEXEME" << setw(8) << "LINE" << "COL" << '\n';
    cout << string(51,'-') << '\n';
    for (auto& t : L.tokens) cout << left << setw(16) <<  t.type << setw(24) << t.lexeme << setw(8) << t.line << t.col << '\n';

    if (!L.errors.empty()) {
        cout << "\nEroare lexicala ("<<L.errors.size()<<"):\n";
        for (auto& e : L.errors) 
            cout << e << '\n';
    }

    return 0;
}
