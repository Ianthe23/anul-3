%option noyywrap
%option yylineno

%{
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <algorithm>
#include "parser.tab.h"
#include "../lab2/part-2/headers/SymbolTable.h"

SymbolTable symbolTable;

static int is_kw(const std::string& s) {
    std::string t = s;
    std::transform(t.begin(), t.end(), t.begin(), [](unsigned char c){ return (char)std::tolower(c); });
    if (t == "if") return IF;
    if (t == "then") return THEN;
    if (t == "endif") return ENDIF;
    if (t == "while") return WHILE;
    if (t == "return") return RETURN;
    if (t == "else") return ELSE;
    if (t == "int") return INT;
    if (t == "float") return FLOAT;
    if (t == "double") return DOUBLE;
    if (t == "char") return CHAR;
    if (t == "include") return INCLUDE;
    if (t == "using") return USING;
    if (t == "namespace") return NAMESPACE;
    if (t == "std") return STD;
    if (t == "iostream") return IOSTREAM;
    if (t == "main") return MAIN;
    return 0;
}
%}

ws          [ \t\r]+
id          [a-zA-Z_][a-zA-Z0-9_]*
intlit      [0-9]+
reallit     [0-9]+\.[0-9]+([eE][+-]?[0-9]+)?
strlit      \"([^\"\\\n]|\\.)*\"

%%

{ws}                ;
"//".*              ;
"/*"([^*]|\*+[^/])*\*+"/" ;

"=="                { return EQ; }
"!="                { return NEQ; }
"<="                { return LE; }
">="                { return GE; }
"&&"                { return AND; }
"||"                { return OR; }

"#"                 { return HASH; }

int[ \t]+main       { return MAIN_INT; }

{reallit}           { yylval.fval = strtod(yytext, nullptr); symbolTable.addSymbol(std::string(yytext)); return NUMBER_REAL; }
{intlit}            { yylval.ival = strtoll(yytext, nullptr, 10); symbolTable.addSymbol(std::string(yytext)); return NUMBER_INT; }
{strlit}            { yylval.str = strndup(yytext, yyleng); symbolTable.addSymbol(std::string(yytext)); return STRING; }

{id}                {
                      std::string s(yytext, yyleng);
                      int kw = is_kw(s);
                      if (kw) return kw;
                      yylval.str = strndup(yytext, yyleng);
                      symbolTable.addSymbol(s);
                      return IDENTIFIER;
                    }

"+"                 { return '+'; }
"-"                 { return '-'; }
"*"                 { return '*'; }
"/"                 { return '/'; }
"%"                 { return '%'; }
"="                 { return '='; }
"<"                 { return '<'; }
">"                 { return '>'; }
"!"                 { return '!'; }
"("                 { return '('; }
")"                 { return ')'; }
"{"                 { return '{'; }
"}"                 { return '}'; }
";"                 { return ';'; }
","                 { return ','; }

\n                  ;
.                   { return yytext[0]; }

%%

