%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

extern FILE* yyin;

int yywrap(void) { return 1; }

/* ===== STATE ===== */
int line = 1;

/* ===== SYMBOL TABLE ===== */
char *symbols[2048];
int symbolsCount = 0;

/* ===== FIP STRUCT ===== */
typedef struct {
    char token[32];
    char lexeme[128];
    int lineTS;
    int line;
} FIPEntry;

FIPEntry fip[4096];
int fipCount = 0;

/* ===== HELPERS ===== */

void add_symbol(const char *s) {
    for (int i = 0; i < symbolsCount; i++)
        if (strcmp(symbols[i], s) == 0) return;

    symbols[symbolsCount] = strdup(s);
    symbolsCount++;
}

int cmpstr(const void *a, const void *b) {
    char *sa = *(char**)a;
    char *sb = *(char**)b;
    return strcmp(sa, sb);
}

int find_symbol(const char *s) {
    for (int i = 0; i < symbolsCount; i++)
        if (strcmp(symbols[i], s) == 0)
            return i + 1;
    return -1;
}

void add_fip(const char *token, const char *lexeme, int addToTS) {
    strcpy(fip[fipCount].token, token);
    strcpy(fip[fipCount].lexeme, lexeme);
    fip[fipCount].line = line;
    fip[fipCount].lineTS = -1;

    if (addToTS)
        add_symbol(lexeme);

    fipCount++;
}

void lex_error(const char *msg) {
    fprintf(stderr, "Lexical error at line %d: %s\n", line, msg);
}

%}


WS          [ \t\r]+
NEWLINE     \n

ID          [a-zA-Z_][a-zA-Z0-9_]*
KEYWORD     (int|float|double|char|if|else|while|for|return)

INT_BIN     0[bB][01]+
INT_HEX     0[xX][0-9a-fA-F]+
INT_OCT     0[0-7]+
INT_DEC     [0-9]+

REAL        [0-9]+\.[0-9]+([eE][+-]?[0-9]+)?[fFlL]?

STRING      \"([^\"\\]|\\.)*\"

OP_MULTI    (==|!=|<<|>>)
OP_SINGLE   [+\-*/%><=]

SEP         [(),;{}\.\[] 

%%

{WS}            { }
{NEWLINE}       { line++; }

"//".*          { }

{STRING}        { add_fip("STRING", yytext, 0); }

{KEYWORD}       { add_fip("KEYWORD", yytext, 0); }

{REAL}          { add_fip("CONSTANT_REAL", yytext, 1); }

{INT_BIN}       { add_fip("CONSTANT_INT", yytext, 1); }
{INT_HEX}       { add_fip("CONSTANT_INT", yytext, 1); }
{INT_OCT}       { add_fip("CONSTANT_INT", yytext, 1); }
{INT_DEC}       { add_fip("CONSTANT_INT", yytext, 1); }

{ID}    {
            if (strlen(yytext) > 8) {
                lex_error("Identifier too long (max 8 chars)");
            } else {
                add_fip("IDENTIFIER", yytext, 1);
            }
        }

{OP_MULTI}      { add_fip("OPERATOR", yytext, 0); }
{OP_SINGLE}     { add_fip("OPERATOR", yytext, 0); }

{SEP}           { add_fip("SEPARATOR", yytext, 0); }

. {
        char msg[64];
        sprintf(msg, "Unknown character '%c'", yytext[0]);
        lex_error(msg);
    }

%%

/* ===== MAIN ===== */

int main(int argc, char **argv) {

    if (argc > 1) {
        FILE *f = fopen(argv[1], "r");
        if (!f) {
            printf("Cannot open file: %s\n", argv[1]);
            return 1;
        }
        yyin = f;
    }

    yylex();

    /* Sort symbol table */
    qsort(symbols, symbolsCount, sizeof(char*), cmpstr);

    /* Remap FIP */
    for (int i = 0; i < fipCount; i++) {
        if (strcmp(fip[i].token, "IDENTIFIER") == 0 ||
            strcmp(fip[i].token, "CONSTANT_INT") == 0 ||
            strcmp(fip[i].token, "CONSTANT_REAL") == 0)
        {
            fip[i].lineTS = find_symbol(fip[i].lexeme);
        }
    }

    /* Write TS */
    FILE *fts = fopen("TS.txt", "w");
    for (int i = 0; i < symbolsCount; i++)
        fprintf(fts, "%s\n", symbols[i]);
    fclose(fts);

    /* Write FIP */
    FILE *ffip = fopen("FIP.txt", "w");
    for (int i = 0; i < fipCount; i++)
        fprintf(ffip, "%s %s %d %d\n",
            fip[i].token,
            fip[i].lexeme,
            fip[i].lineTS,
            fip[i].line);
    fclose(ffip);

    printf("Generated: TS.txt and FIP.txt\n");

    return 0;
}
