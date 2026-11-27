
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main() {
    char line[500];
    char *keywords[] = {"int", "char", "float", "double", "if", "else",
                        "for", "while", "do", "return", "void"};

    while (fgets(line, sizeof(line), stdin)) {
        if (strncmp(line, "end", 3) == 0) break;

        int i = 0;

        while (line[i]) {
            if (isspace(line[i])) {
                i++;
                continue;
            }

            if (isalpha(line[i]) || line[i] == '_') {
                char word[50];
                int j = 0;

                while (isalnum(line[i]) || line[i] == '_')
                    word[j++] = line[i++];

                word[j] = '\0';

                int k, flag = 0;
                for (k = 0; k < 11; k++)
                    if (strcmp(word, keywords[k]) == 0)
                        flag = 1;

                printf("%-12s: %s\n", flag ? "Keyword" : "Identifier", word);
            }
            else if (isdigit(line[i])) {
                printf("%-12s: ", "Literal");
                while (isdigit(line[i]) || line[i] == '.')
                    putchar(line[i++]);
                printf("\n");
            }
            else if (strchr("+-*/%=<>!&|^~?", line[i])) {
                printf("%-12s: %c\n", "Operator", line[i++]);
            }
            else if (strchr("{}()[];,:.", line[i])) {
                printf("%-12s: %c\n", "Punctuation", line[i++]);
            }
            else {
                i++;
            }
        }
    }

    return 0;
}
