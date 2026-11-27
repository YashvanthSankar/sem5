%{
/* Extensions A + B + C:
   A: % and right-associative ^
   B: floating-point numbers (double, atof)
   C: multi-character variable names                                   */
#include <stdlib.h>
#include <string.h>
#include "calc_ext.tab.h"
%}

%%

[ \t\r]+                      ;   /* Skip whitespace */
([0-9]+("."[0-9]*)?|"."[0-9]+)          { yylval.num = atof(yytext); return NUMBER; }
[a-zA-Z_][a-zA-Z0-9_]*      { yylval.name = malloc(yyleng + 1);
                               if (!yylval.name) exit(EXIT_FAILURE);
                               strcpy(yylval.name, yytext);
                               return IDENTIFIER; }

\n                          { return '\n'; }
[-+*/%^=()]                 { return yytext[0]; }
.                           { printf("Lexical Error: Unexpected character '%s'\n", yytext); return (unsigned char)yytext[0]; }

%%

int yywrap(void) {
    return 1;
}
