#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 50
#define WIDTH 128

char name[MAX][20], rhs[MAX][MAX][WIDTH];
int count[MAX], total = 1;

void printRule(int r) {
    printf("%s -> ", name[r]);
    for (int i = 0; i < count[r]; i++)
        printf("%s%s", i ? " | " : "", rhs[r][i][0] ? rhs[r][i] : "e");
    puts("");
}

int findPrefix(int r, char *prefix) {
    int best = 0;
    for (int i = 0; i < count[r]; i++) {
        for (int j = i + 1; j < count[r]; j++) {
            int k = 0;
            while (rhs[r][i][k] && rhs[r][i][k] == rhs[r][j][k]) k++;
            if (k > best) {
                best = k;
                memcpy(prefix, rhs[r][i], k);
                prefix[k] = '\0';
            }
        }
    }
    return best;
}

void factor(int r) {
    char prefix[WIDTH];
    int len;
    while ((len = findPrefix(r, prefix)) > 0) {
        int child = total++;
        sprintf(name[child], "A%d", child);
        int kept = 0;

        for (int i = 0; i < count[r]; i++) {
            char *alt = rhs[r][i];
            if (strncmp(alt, prefix, len) != 0) {
                memmove(rhs[r][kept++], alt, strlen(alt) + 1);
                continue;
            }

            /* Move the suffix to the new rule. */
            strcpy(rhs[child][count[child]++], alt + len);
            if (count[child] == 1)
                sprintf(rhs[r][kept++], "%s%s", prefix, name[child]);
        }
        count[r] = kept;
    }
}

int main(void) {
    char line[500], rule[500];
    int n = 0;
    puts("Enter a grammar rule:");
    if (!fgets(line, sizeof line, stdin)) return 1;

    for (int i = 0; line[i]; i++)
        if (!isspace((unsigned char)line[i])) rule[n++] = line[i];
    rule[n] = '\0';

    char *arrow = strstr(rule, "->");
    if (!arrow || arrow - rule >= (int)sizeof name[0]) return 1;
    *arrow = '\0';
    strcpy(name[0], rule);
    for (char *alt = strtok(arrow + 2, "|"); alt; alt = strtok(NULL, "|")) {
        if (count[0] == MAX || strlen(alt) > 99) return 1;
        strcpy(rhs[0][count[0]++], strcmp(alt, "#") == 0 ? "" : alt);
    }

    printf("\nOriginal grammar rule: ");
    printRule(0);
    puts("\nLeft-factored grammar rules:\n");
    for (int r = 0; r < total; r++) {
        factor(r);
        printRule(r);
    }
    return 0;
}
