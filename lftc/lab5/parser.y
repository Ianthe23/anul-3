%{
#include <cstdio>
#include <cstdlib>
#include <string>
#include <iostream>
#include <vector>
#include "../lab2/part-2/headers/SymbolTable.h"

extern int yylineno;
extern FILE* yyin;
int yylex();
void yyerror(const char* s);
extern SymbolTable symbolTable;
static int syntax_errors = 0;
%}

%union {
    char* str;
    long long ival;
    double fval;
}

%token IF THEN ENDIF WHILE RETURN ELSE
%token INT FLOAT DOUBLE CHAR
%token INCLUDE USING NAMESPACE STD MAIN HASH MAIN_INT IOSTREAM
%token <str> IDENTIFIER STRING
%token <ival> NUMBER_INT
%token <fval> NUMBER_REAL
%token EQ NEQ LE GE AND OR

%type <fval> expr

%left OR
%left AND
%left EQ NEQ
%left '<' '>' LE GE
%left '+' '-'
%left '*' '/' '%'
%right '!' UMINUS

%%

program
    : preamble stmt_list
    ;

preamble
    : preamble include_stmt
    | preamble using_stmt
    | preamble main_def
    | /* empty */
    ;

include_stmt
    : HASH INCLUDE '<' IDENTIFIER '>'
    | HASH INCLUDE '<' IOSTREAM '>'
    | HASH INCLUDE STRING
    ;

using_stmt
    : USING NAMESPACE STD ';'
    ;

stmt_list
    : stmt_list stmt
    | /* empty */
    ;

stmt
    : decl ';'
    | assign ';'
    | if_stmt
    | while_stmt
    | block
    | return_stmt ';'
    ;

decl
    : type IDENTIFIER
    | type IDENTIFIER '=' expr
    ;

type
    : INT
    | FLOAT
    | DOUBLE
    | CHAR
    ;

assign
    : IDENTIFIER '=' expr
    ;

return_stmt
    : RETURN expr
    ;

block
    : '{' stmt_list '}'
    ;

if_stmt
    : IF '(' expr ')' THEN stmt_list ENDIF
    ;

while_stmt
    : WHILE '(' expr ')' stmt
    ;

main_def
    : MAIN_INT '(' ')' block
    | MAIN '(' ')' block
    ;

expr
    : expr '+' expr        { $$ = 0; }
    | expr '-' expr        { $$ = 0; }
    | expr '*' expr        { $$ = 0; }
    | expr '/' expr        { $$ = 0; }
    | expr '%' expr        { $$ = 0; }
    | expr EQ expr         { $$ = 0; }
    | expr NEQ expr        { $$ = 0; }
    | expr '<' expr        { $$ = 0; }
    | expr '>' expr        { $$ = 0; }
    | expr LE expr         { $$ = 0; }
    | expr GE expr         { $$ = 0; }
    | expr AND expr        { $$ = 0; }
    | expr OR expr         { $$ = 0; }
    | '!' expr             { $$ = 0; }
    | '-' expr %prec UMINUS{ $$ = 0; }
    | '(' expr ')'         { $$ = $2; }
    | IDENTIFIER           { $$ = 0; }
    | NUMBER_INT           { $$ = (double)$1; }
    | NUMBER_REAL          { $$ = $1; }
    | STRING               { $$ = 0; }
    ;

%%

void yyerror(const char* s) {
    std::cerr << "Eroare sintactica la linia " << yylineno << ": " << s << "\n";
    syntax_errors++;
}

static void printSymbolTable() {
    auto symbols = symbolTable.getAllSymbols();
    std::cout << "\n=== Tabela de Simboluri (BST) ===\n";
    std::cout << "INDEX  SIMBOL\n";
    for (const auto& p : symbols) {
        std::cout << p.second << "     " << p.first << "\n";
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string inputPath;
    std::cout << "Introduceti calea catre fisierul sursa: ";
    std::getline(std::cin, inputPath);

    FILE* f = fopen(inputPath.c_str(), "r");
    if (!f) {
        std::cerr << "Eroare: nu pot deschide fisierul '" << inputPath << "'\n";
        return 1;
    }
    yyin = f;

    int res = yyparse();
    fclose(f);

    if (syntax_errors == 0 && res == 0) {
        std::cout << "\n=== Program corect din punct de vedere sintactic ===\n";
    } else {
        std::cout << "\n=== Erori sintactice: " << syntax_errors << " ===\n";
    }

    printSymbolTable();
    return syntax_errors == 0 ? 0 : 1;
}