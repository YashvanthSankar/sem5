#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

/* Q9 = Q6 FOLLOW + Q8 states + SLR table + parser. */
#define OFFSET 3
int np, ns, count[101], go[100][128];
char P[30][64], items[101][30][64]; /* Extra slot is the GOTO scratch state. */

char first[26][128], follow[26][128], terminals[128], nonterminals[27];
int action[100][128], conflict; /* 0=error, next+1=shift, -rule=reduce, 999=accept */

void add(char *set, char c) {
    if (!strchr(set, c)) strncat(set, &c, 1);
}
void addAll(char *to, char *from) {
    for (int i = 0; from[i]; i++)
        if (from[i] != '#') add(to, from[i]);
}
/* Add FIRST(s) to out. Return 1 if s can vanish. */
int firstOf(char *s, char *out) {
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '#') continue;
        if (!isupper(c)) { add(out, c); return 0; }
        addAll(out, first[c - 'A']);
        if (!strchr(first[c - 'A'], '#')) return 0;
    }
    return 1;
}
void firstFollow(void) {
    int changed;
    do {
        changed = 0;
        for (int p = 0; p < np; p++) {
            char *set = first[P[p][0] - 'A'];
            int before = strlen(set);
            if (firstOf(P[p] + OFFSET, set)) add(set, '#');
            if ((int)strlen(set) != before) changed = 1;
        }
    } while (changed);
    add(follow[P[0][0] - 'A'], '$');
    do {
        changed = 0;
        for (int p = 0; p < np; p++) {
            char *rhs = P[p] + OFFSET;
            for (int i = 0; rhs[i]; i++) {
                if (!isupper(rhs[i])) continue;
                char *set = follow[rhs[i] - 'A'];
                int before = strlen(set);
                if (firstOf(rhs + i + 1, set)) addAll(set, follow[P[p][0] - 'A']);
                if ((int)strlen(set) != before) changed = 1;
            }
        }
    } while (changed);
}

int hasItem(int s, char *item) {
    for (int i = 0; i < count[s]; i++)
        if (!strcmp(items[s][i], item)) return 1;
    return 0;
}
void addItem(int s, char *item) {
    if (!hasItem(s, item)) strcpy(items[s][count[s]++], item);
}
/* CLOSURE: dot before B -> add every B->.rhs. */
void closure(int s) {
    for (int i = 0; i < count[s]; i++) {
        char B = strchr(items[s][i], '.')[1];
        if (!isupper(B)) continue;
        for (int p = 0; p < np; p++)
            if (P[p][0] == B) {
                char item[64];
                sprintf(item, "%c->.%s", B, P[p] + 3);
                addItem(s, item);
            }
    }
}
int oldState(int s) {
    for (int old = 0; old < s; old++) {
        if (count[old] != count[s]) continue;
        int same = 1;
        for (int i = 0; i < count[s]; i++)
            if (!hasItem(old, items[s][i])) same = 0;
        if (same) return old;
    }
    return -1;
}
void buildStates(void) {
    char item[64];
    sprintf(item, "%c->.%s", P[0][0], P[0] + 3);
    addItem(0, item);
    closure(0);
    ns = 1;
    for (int s = 0; s < 100; s++)
        for (int c = 0; c < 128; c++) go[s][c] = -1;
    for (int s = 0; s < ns; s++)
        for (int i = 0; i < count[s]; i++) {
            char X = strchr(items[s][i], '.')[1];
            if (!X || go[s][(int)X] != -1) continue;
            count[ns] = 0;
            /* GOTO: move matching dots over X, then take closure. */
            for (int j = 0; j < count[s]; j++) {
                strcpy(item, items[s][j]);
                char *dot = strchr(item, '.');
                if (dot[1] == X) { dot[0] = X; dot[1] = '.'; addItem(ns, item); }
            }
            closure(ns);
            int old = oldState(ns);
            if (old == -1 && ns == 100) { puts("Too many states."); exit(1); }
            go[s][(int)X] = old == -1 ? ns++ : old;
        }
}
/* Add a new start rule using an unused uppercase letter. */
void augment(void) {
    /* Already augmented, like the docx (rule 0 is S->E and S is used nowhere
       else)? Then keep it as rule 0 so the numbering matches the textbook. */
    int used = 0;
    for (int p = 2; p < np; p++)
        if (strchr(P[p], P[1][0])) used = 1;
    if (!used && strlen(P[1]) == 4 && isupper(P[1][3]) && P[1][3] != P[1][0]) {
        for (int p = 0; p + 1 < np; p++) strcpy(P[p], P[p + 1]);
        np--;
        return;
    }
    char A = 'Z';
    for (int p = 1; p < np; p++)
        if (strchr(P[p], A)) { if (--A < 'A') exit(1); p = 0; }
    sprintf(P[0], "%c->%c", A, P[1][0]);
}

void setAction(int s, int c, int value) {
    if (action[s][c] && action[s][c] != value) conflict = 1;
    action[s][c] = value;
}
void buildTable(void) {
    for (int s = 0; s < ns; s++) {
        for (int t = 0; terminals[t]; t++) {
            int c = terminals[t];
            if (go[s][c] != -1) setAction(s, c, go[s][c] + 1);
        }
        for (int i = 0; i < count[s]; i++) {
            char item[64];
            strcpy(item, items[s][i]);
            int length = strlen(item);
            if (item[length - 1] != '.') continue;
            item[length - 1] = '\0';
            for (int p = 0; p < np; p++)
                if (!strcmp(P[p], item)) {
                    if (p == 0) setAction(s, '$', 999);
                    else {
                        char *set = follow[P[p][0] - 'A'];
                        for (int f = 0; set[f]; f++) setAction(s, set[f], -p);
                    }
                }
        }
    }
}
void printTable(void) {
    puts("--- FOLLOW SETS ---");
    for (int a = 0; nonterminals[a]; a++) {
        char A = nonterminals[a], *set = follow[A - 'A'];
        printf("FOLLOW(%c) = { ", A);
        for (int f = 0; set[f]; f++) printf("%c ", set[f]);
        puts("}");
    }
    puts("\n--- ACTION / GOTO TABLE ---");
    printf("State");
    for (int t = 0; terminals[t]; t++) printf("\t%c", terminals[t]);
    printf("\t|");
    for (int a = 0; nonterminals[a]; a++) printf("\t%c", nonterminals[a]);
    puts("");
    for (int s = 0; s < ns; s++) {
        printf("%d", s);
        for (int t = 0; terminals[t]; t++) {
            int value = action[s][(int)terminals[t]];
            if (value == 999) printf("\tacc");
            else if (value > 0) printf("\ts%d", value - 1);
            else if (value < 0) printf("\tr%d", -value);
            else printf("\t");
        }
        printf("\t|");
        for (int a = 0; nonterminals[a]; a++) {
            int next = go[s][(int)nonterminals[a]];
            if (next == -1) printf("\t"); else printf("\t%d", next);
        }
        puts("");
    }
}
/* Remove spaces, "0:" numbering and turn "->"-arrow / "id" into our form. */
void clean(char *text) {
    char *from = strchr(text, ':') ? strchr(text, ':') + 1 : text;
    int k = 0;
    for (int i = 0; from[i]; i++) {
        unsigned char c = from[i];
        if (isspace(c)) continue;
        if (c == 0xE2) { text[k++] = '-'; text[k++] = '>'; i += 2; continue; } /* arrow */
        if (c >= 128) continue;                                   /* other non-ASCII */
        text[k++] = c;
        if (c == 'i' && from[i + 1] == 'd') i++;                  /* "id" -> i */
    }
    text[k] = '\0';
}
void parse(char *word) {
    int stack[256] = {0}, top = 0, position = 0;
    strcat(word, "$");
    puts("\n--- PARSING ---\nSTACK\t| INPUT\t| ACTION");
    while (1) {
        for (int i = 0; i <= top; i++) printf("%d ", stack[i]);
        printf("\t| %s\t| ", word + position);
        int step = action[stack[top]][(int)word[position]];
        if (step == 999 && !word[position + 1]) {
            puts("accept\n\nInput string is accepted."); return;
        } else if (step > 0 && step != 999) {
            printf("shift %d\n", step - 1);
            stack[++top] = step - 1;
            position++;
        } else if (step < 0) {
            int p = -step;
            printf("reduce %s%s\n", P[p], P[p][3] ? "" : "#");
            top -= strlen(P[p] + 3); /* Epsilon pops zero states. */
            int next = go[stack[top]][(int)P[p][0]];
            stack[++top] = next;
        } else { puts("error\n\nInput string is rejected."); return; }
        if (top >= 255) { puts("Stack limit reached."); return; }
    }
}
int main(void) {
    char word[256] = "";
    fgets(word, sizeof word, stdin);
    np = atoi(word) + 1;
    for (int p = 1; p < np; p++) {
        fgets(P[p], 64, stdin);
        clean(P[p]);
        if (!strcmp(P[p] + 3, "#")) P[p][3] = '\0';
        add(nonterminals, P[p][0]);
        for (int i = 3; P[p][i]; i++)
            if (!isupper(P[p][i])) add(terminals, P[p][i]);
    }
    add(terminals, '$');
    augment();
    firstFollow();
    buildStates();
    buildTable();
    printTable();
    if (conflict) { puts("Grammar is not SLR(1)."); return 0; }
    if (fgets(word, sizeof word, stdin)) {
        if (strcspn(word, "\r\n") > 252) { puts("Input string is rejected."); return 0; }
        clean(word);
    } else word[0] = '\0';
    int length = strlen(word);
    if (length && word[length - 1] == '$') word[length - 1] = '\0';
    parse(word);
    return 0;
}
