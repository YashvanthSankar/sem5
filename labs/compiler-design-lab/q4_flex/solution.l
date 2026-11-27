%option noyywrap noinput nounput
%{
#include <stdio.h>
%}

%x COMMENT

%%

"//"[^\n]*          { /* single-line comment: ignore */ }
"/*"                { BEGIN(COMMENT); }
<COMMENT>"*/"       { BEGIN(INITIAL); }
<COMMENT>(.|\n)       { /* multi-line comment body: ignore */ }

"int"|"float"|"char"|"if"|"else"|"while"|"return"   { printf("KEYWORD       : %s\n", yytext); }

[0-9]+\.[0-9]+      { printf("FLOAT         : %s\n", yytext); }
[0-9]+              { printf("INTEGER       : %s\n", yytext); }

[a-zA-Z_][a-zA-Z0-9_]*  { printf("IDENTIFIER    : %s\n", yytext); }

[<>]=?|[!=]=        { printf("RELATIONAL_OP : %s\n", yytext); }
[-+*/%]             { printf("ARITHMETIC_OP : %s\n", yytext); }
"="                 { printf("ASSIGNMENT    : %s\n", yytext); }
[][(){},;]          { printf("DELIMITER     : %s\n", yytext); }
\"([^\"\\\n]|\\.)*\"  { printf("STRING        : %s\n", yytext); }
'([^'\\\n]|\\.)'    { printf("CHARACTER     : %s\n", yytext); }
[ \t\r\n]+          ;
.                   { printf("INVALID       : %s\n", yytext); }

%%

int main(void) {
    yylex();
    return 0;
}
