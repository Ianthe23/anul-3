#ifndef FIP_H
#define FIP_H

#include <string>
using namespace std;

struct FIPEntry {
    string tokenType;
    int code;
    int symbolTableIndex; // -1 daca nu e in tabela de simboluri
    int line;
    int col;
};

// Coduri pentru tipurile de token-uri
enum TokenCodes {
    KEYWORD_CODE = 1,
    IDENTIFIER_CODE = 2,
    CONSTANT_CODE = 3,
    OPERATOR_CODE = 4,
    SEPARATOR_CODE = 5,
    STRING_CODE = 6,
    HASH_CODE = 7
};

#endif