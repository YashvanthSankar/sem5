#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define STATES 20
#define SYMBOLS 10
#define SUBSETS 100
#define EPSILON SYMBOLS

int n, start, final[STATES];
char alphabet[SYMBOLS + 1];
int edge[SYMBOLS + 1][STATES][STATES];
int subsets[SUBSETS][STATES], next[SUBSETS][SYMBOLS], total;

/* Accept plain lines and the labels shown in the question. */
int readLine(char line[200]) {
    while (fgets(line, 200, stdin)) {
        char *colon = strchr(line, ':');
        if (colon) memmove(line, colon + 1, strlen(colon + 1) + 1);
        if (line[strspn(line, " \t\r\n")]) return 1;
    }
    return 0;
}

int readNFA(void) {
    char line[200];
    if (!readLine(line) || sscanf(line, "%d", &n) != 1 || n < 1 || n > STATES)
        return 0;
    if (!readLine(line) || !readLine(line)) return 0; /* State list, then alphabet */
    int m = 0;
    for (int i = 0; line[i]; i++)
        if (!strchr(" ,\t\r\n", line[i]) && !strchr(alphabet, line[i])) {
            if (m == SYMBOLS) return 0;
            alphabet[m++] = line[i];
        }
    if (!readLine(line) || sscanf(line, "%d", &start) != 1 || start < 0 || start >= n)
        return 0;

    if (!readLine(line)) return 0;
    int state, used;
    for (char *p = line; sscanf(p, "%d%n", &state, &used) == 1; p += used) {
        if (state < 0 || state >= n) return 0;
        final[state] = 1;
    }

    int from, to;
    char symbol;
    while (readLine(line)) {
        if (sscanf(line, "%d %c %d", &from, &symbol, &to) != 3) continue;
        if (from < 0 || from >= n || to < 0 || to >= n) return 0;
        char *column = strchr(alphabet, symbol);
        if (strchr("eE#", symbol)) edge[EPSILON][from][to] = 1;
        else if (column) edge[column - alphabet][from][to] = 1;
    }
    return 1;
}

void closure(int set[]) {
    int changed;
    do {
        changed = 0;
        for (int from = 0; from < n; from++)
            for (int to = 0; to < n; to++)
                if (set[from] && edge[EPSILON][from][to] && !set[to]) {
                    set[to] = 1;
                    changed = 1;
                }
    } while (changed);
}

int findOrAdd(int set[]) {
    for (int s = 0; s < total; s++)
        if (memcmp(subsets[s], set, sizeof subsets[s]) == 0) return s;
    if (total == SUBSETS) {
        puts("Too many DFA states.");
        exit(1);
    }
    memcpy(subsets[total], set, sizeof subsets[total]);
    return total++;
}

void buildDFA(void) {
    int initial[STATES] = {0};
    initial[start] = 1;
    closure(initial);
    findOrAdd(initial);

    for (int s = 0; s < total; s++)
        for (int c = 0; alphabet[c]; c++) {
            int moved[STATES] = {0};
            for (int from = 0; from < n; from++)
                for (int to = 0; to < n; to++)
                    if (subsets[s][from] && edge[c][from][to]) moved[to] = 1;
            closure(moved);
            next[s][c] = findOrAdd(moved);
        }
}

int isFinal(int s) {
    for (int i = 0; i < n; i++)
        if (subsets[s][i] && final[i]) return 1;
    return 0;
}

void printDFA(void) {
    printf("\nNumber of DFA states: %d\nDFA initial state: 0\n", total);
    printf("DFA final states:");
    for (int s = 0; s < total; s++)
        if (isFinal(s)) printf(" %d", s);
    puts("\n\nDFA states (subsets of NFA states):");
    for (int s = 0; s < total; s++) {
        printf("D%d = {", s);
        const char *separator = "";
        for (int i = 0; i < n; i++)
            if (subsets[s][i]) {
                printf("%s%d", separator, i);
                separator = ",";
            }
        puts(*separator ? "}" : "}  (dead state)");
    }

    printf("\nDFA transition table:\nState");
    for (int c = 0; alphabet[c]; c++) printf("\t%c", alphabet[c]);
    puts("");
    for (int s = 0; s < total; s++) {
        printf("%d", s);
        for (int c = 0; alphabet[c]; c++) printf("\t%d", next[s][c]);
        puts("");
    }
}

int main(void) {
    puts("Enter NFA in the question's format. End transitions with EOF.");
    if (!readNFA()) {
        puts("Invalid NFA input.");
        return 1;
    }
    buildDFA();
    printDFA();
    return 0;
}
