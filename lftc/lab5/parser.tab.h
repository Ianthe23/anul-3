/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     IF = 258,
     THEN = 259,
     ENDIF = 260,
     WHILE = 261,
     RETURN = 262,
     ELSE = 263,
     INT = 264,
     FLOAT = 265,
     DOUBLE = 266,
     CHAR = 267,
     INCLUDE = 268,
     USING = 269,
     NAMESPACE = 270,
     STD = 271,
     MAIN = 272,
     HASH = 273,
     MAIN_INT = 274,
     IOSTREAM = 275,
     IDENTIFIER = 276,
     STRING = 277,
     NUMBER_INT = 278,
     NUMBER_REAL = 279,
     EQ = 280,
     NEQ = 281,
     LE = 282,
     GE = 283,
     AND = 284,
     OR = 285,
     UMINUS = 286
   };
#endif
/* Tokens.  */
#define IF 258
#define THEN 259
#define ENDIF 260
#define WHILE 261
#define RETURN 262
#define ELSE 263
#define INT 264
#define FLOAT 265
#define DOUBLE 266
#define CHAR 267
#define INCLUDE 268
#define USING 269
#define NAMESPACE 270
#define STD 271
#define MAIN 272
#define HASH 273
#define MAIN_INT 274
#define IOSTREAM 275
#define IDENTIFIER 276
#define STRING 277
#define NUMBER_INT 278
#define NUMBER_REAL 279
#define EQ 280
#define NEQ 281
#define LE 282
#define GE 283
#define AND 284
#define OR 285
#define UMINUS 286




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
#line 17 "parser.y"
{
    char* str;
    long long ival;
    double fval;
}
/* Line 1529 of yacc.c.  */
#line 117 "parser.tab.h"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;

