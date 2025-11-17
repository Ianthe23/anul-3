/* lab4/lexer_test.l */
%option noyywrap yylineno
%{
#include <stdio.h>
%}
%%
[ \t\r]+      ;
\n            ;
[0-9]+        { printf("INT %.*s at L%d\n", yyleng, yytext, yylineno); }
[a-zA-Z_][a-zA-Z0-9_]* { printf("ID %.*s at L%d\n", yyleng, yytext, yylineno); }
.             { fprintf(stderr, "Error L%d: '%c'\n", yylineno, *yytext); }
%%
int main(){ yylex(); return 0;}