#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

/* Input: N, then N rules A->rhs without spaces; # = epsilon. */
int np, ns, count[101], go[100][128];
char P[30][64], items[101][30][64]; /* Extra slot is the GOTO scratch state. */

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
    char A = 'Z';
    for (int p = 1; p < np; p++)
        if (strchr(P[p], A)) { if (--A < 'A') exit(1); p = 0; }
    sprintf(P[0], "%c->%c", A, P[1][0]);
}

int main(void) {
    scanf("%d", &np);
    np++; /* Rule 0 is reserved for augmentation. */
    for (int p = 1; p < np; p++) {
        scanf("%59s", P[p]);
        if (!strcmp(P[p] + 3, "#")) P[p][3] = '\0';
    }
    augment();
    buildStates();
    for (int s = 0; s < ns; s++) {
        printf("I%d:\n", s);
        for (int i = 0; i < count[s]; i++) puts(items[s][i]);
        if (s + 1 < ns) puts("");
    }
    return 0;
}
