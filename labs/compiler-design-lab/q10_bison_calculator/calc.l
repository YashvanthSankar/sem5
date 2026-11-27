/* Build commands are in calc.y. */
%option noyywrap noinput nounput
%{
#include <stdio.h>
#include <stdlib.h>
#include "calc.tab.h"
%}

%%
[ \t\r]+    ;
[0-9]+      { yylval.num = atoi(yytext); return NUMBER; }
[a-z]       { yylval.id = yytext[0] - 'a'; return IDENTIFIER; }
\n          { return '\n'; }
[-+*/=()]   { return yytext[0]; }
.           { printf("Lexical Error: Unexpected character '%s'\n", yytext);
              return (unsigned char)yytext[0]; }
%%
