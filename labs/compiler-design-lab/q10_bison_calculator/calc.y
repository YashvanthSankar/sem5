/* Integer calculator: a-z variables, assignment, + - * /, unary minus.
   Build: bison -d calc.y
          flex calc.l
          gcc calc.tab.c lex.yy.c -o calc
   Run:   ./calc     (one expression per line; Ctrl+D to finish)
   Memory aid: declarations -> grammar -> actions -> main. */
%{
#include <stdio.h>
int sym[26];
int yylex(void);
void yyerror(const char *message);
%}

%union {
    int num;
    int id;
}

%token <num> NUMBER
%token <id> IDENTIFIER
%type <num> expr
%left '+' '-'
%left '*' '/'
%right UMINUS

%%
lines:
      /* empty */
    | lines line
    ;
line:
      '\n'
    | expr '\n'                { printf("Result = %d\n", $1); }
    | IDENTIFIER '=' expr '\n'   { sym[$1] = $3;
                                 printf("Assigned: %c = %d\n", 'a' + $1, $3); }
    | error '\n'               { yyerrok; }
    ;
expr:
      NUMBER                   { $$ = $1; }
    | IDENTIFIER                 { $$ = sym[$1]; }
    | expr '+' expr            { $$ = $1 + $3; }
    | expr '-' expr            { $$ = $1 - $3; }
    | expr '*' expr            { $$ = $1 * $3; }
    | expr '/' expr            { if ($3 == 0) {
                                     yyerror("Division by zero"); $$ = 0;
                                 } else $$ = $1 / $3; }
    | '-' expr %prec UMINUS    { $$ = -$2; }
    | '(' expr ')'             { $$ = $2; }
    ;
%%

void yyerror(const char *message) {
    fprintf(stderr, "Error: %s\n", message);
}

int main(void) {
    puts("=== Calculator Active (Input expressions / assignments, Ctrl+D to exit) ===");
    return yyparse();
}