#include <stdio.h>
#include <string.h>

#define STATES 12
#define START 0
#define ACCEPT 11

/* Thompson NFA for (a+b)*abb. Each row is {from, symbol, to}. */
struct Edge {
    int from;
    char symbol;
    int to;
};
const struct Edge edges[] = {
    {0,'e',1}, {0,'e',7}, {1,'e',2}, {2,'e',3}, {2,'e',5},
    {3,'a',4}, {4,'e',7}, {5,'b',6}, {6,'e',7},
    {7,'e',1}, {7,'e',8}, {8,'a',9}, {9,'b',10}, {10,'b',11}
};
#define EDGES (sizeof edges / sizeof edges[0])

void closure(int set[]) {
    int changed;
    do {
        changed = 0;
        for (size_t i = 0; i < EDGES; i++) {
            struct Edge edge = edges[i];
            if (edge.symbol == 'e' && set[edge.from] && !set[edge.to]) {
                set[edge.to] = 1;
                changed = 1;
            }
        }
    } while (changed);
}

int accepts(const char *word) {
    int current[STATES] = {0};
    if (strlen(word) > 100) return 0;
    current[START] = 1;
    closure(current);

    for (int j = 0; word[j]; j++) {
        if (word[j] != 'a' && word[j] != 'b') return 0;
        int next[STATES] = {0};
        for (size_t i = 0; i < EDGES; i++) {
            struct Edge edge = edges[i];
            if (edge.symbol == word[j] && current[edge.from])
                next[edge.to] = 1;
        }
        closure(next);
        memcpy(current, next, sizeof current);
    }
    return current[ACCEPT];
}

int main(void) {
    char word[102];
    printf("Enter input string: ");
    if (!fgets(word, sizeof word, stdin)) return 0;
    word[strcspn(word, "\r\n")] = '\0';
    puts(accepts(word) ? "ACCEPTED" : "REJECTED");
    return 0;
}
