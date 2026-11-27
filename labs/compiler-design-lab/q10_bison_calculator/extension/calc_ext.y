%{
/* Extensions A + B + C:
   A: % (same precedence as * /) and right-associative ^
   B: floating-point values (double)
   C: multi-character identifiers (simple symbol table array)          */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* Exercise C: grow the symbol table as new names appear. */
struct Variable {
    char *name;
    double value;
};
struct Variable *table;
size_t nvars;

/* Take ownership of the name passed by Flex. */
struct Variable *lookup(char *name) {
    for (size_t i = 0; i < nvars; i++) {
        if (strcmp(table[i].name, name) == 0) {
            free(name);
            return &table[i];
        }
    }

    struct Variable *grown = realloc(table, (nvars + 1) * sizeof *table);
    if (!grown) {
        fprintf(stderr, "Error: Out of memory\n");
        exit(EXIT_FAILURE);
    }
    table = grown;
    table[nvars] = (struct Variable){name, 0};
    return &table[nvars++];
}

int yylex(void);
void yyerror(const char *s);
%}

%union {
    double num;        /* Exercise B: double instead of int */
    char  *name;       /* Exercise C: variable name */
}

%token <num>  NUMBER
%token <name> IDENTIFIER
%type  <num>  expr
%destructor { free($$); } IDENTIFIER

/* lowest to highest */
%left  '+' '-'
%left  '*' '/' '%'     /* Exercise A: % same level as * and / */
%right UMINUS
%right '^'             /* Exercise A: right-associative power */

%%

lines:
      /* empty */
    | lines line
    ;

line:
      '\n'
    | expr '\n'                  { printf("Result = %g\n", $1); }
    | IDENTIFIER '=' expr '\n'   {
          struct Variable *var = lookup($1);
          var->value = $3;
          printf("Assigned: %s = %g\n", var->name, var->value);
      }
    | error '\n'                 { yyerrok; }
    ;

expr:
      NUMBER                     { $$ = $1; }
    | IDENTIFIER                 { $$ = lookup($1)->value; }
    | expr '+' expr              { $$ = $1 + $3; }
    | expr '-' expr              { $$ = $1 - $3; }
    | expr '*' expr              { $$ = $1 * $3; }
    | expr '/' expr              {
                                     if ($3 == 0) { yyerror("Division by zero"); $$ = 0; }
                                     else $$ = $1 / $3;
                                 }
    | expr '%' expr              {
                                     if ($3 == 0) { yyerror("Modulo by zero"); $$ = 0; }
                                     else $$ = fmod($1, $3);
                                 }
    | expr '^' expr              { $$ = pow($1, $3); }
    | '-' expr %prec UMINUS      { $$ = -$2; }
    | '(' expr ')'               { $$ = $2; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    printf("=== Calculator Active (Input expressions / assignments, Ctrl+D to exit) ===\n");
    int result = yyparse();
    for (size_t i = 0; i < nvars; i++) free(table[i].name);
    free(table);
    return result;
}
