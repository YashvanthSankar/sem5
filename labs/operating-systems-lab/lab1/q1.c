/*Write a program that reads a text file and prints:
Total number of lines
Total number of words
Total number of characters
The longest line in the file*/

#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main() {
    FILE *fp = fopen("input.txt", "r");
    char line[1000], longest[1000] = "";
    int lines = 0, words = 0, chars = 0, len;

    if (!fp) {
        printf("File not found\n");
        return 1;
    }

    while (fgets(line, sizeof(line), fp)) {
        lines++;
        chars += strlen(line);

        len = strlen(line);
        if (len > strlen(longest))
            strcpy(longest, line);

        for (int i = 0; line[i]; i++)
            if (!isspace(line[i]) &&
                (i == 0 || isspace(line[i - 1])))
                words++;
    }

    fclose(fp);

    printf("Lines: %d\n", lines);
    printf("Words: %d\n", words);
    printf("Characters: %d\n", chars);
    printf("Longest line: %s", longest);

    return 0;
}