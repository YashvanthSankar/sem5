#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

/* Input: N rules, A=rhs (no spaces); # = epsilon. */
#define OFFSET 2
int np;
char P[30][64], first[26][128], follow[26][128];

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

int main(void) {
    char terminals[128] = "", nonterminals[27] = "";
    scanf("%d", &np);
    for (int p = 0; p < np; p++) {
        scanf("%59s", P[p]);
        add(nonterminals, P[p][0]);
        for (int i = 2; P[p][i]; i++)
            if (!isupper(P[p][i]) && P[p][i] != '#') add(terminals, P[p][i]);
    }
    add(terminals, '$');
    firstFollow(); /* Recompute Q6 sets; supplied sets need not be typed. */
    puts("--- LL(1) PARSING TABLE ---\n");
    for (int t = 0; terminals[t]; t++) printf("\t%c", terminals[t]);
    puts("");
    for (int a = 0; nonterminals[a]; a++) {
        printf("%c", nonterminals[a]);
        for (int t = 0; terminals[t]; t++) {
            int found = -1;
            for (int p = 0; p < np; p++) {
                if (P[p][0] != nonterminals[a]) continue;
                char choices[128] = "";
                if (firstOf(P[p] + 2, choices)) addAll(choices, follow[P[p][0] - 'A']);
                if (!strchr(choices, terminals[t])) continue;
                if (found != -1) { puts("\nGrammar is not LL(1)."); return 0; }
                found = p;
            }
            printf("\t%s", found == -1 ? "error" : P[found]);
        }
        puts("");
    }
    return 0;
}
