#include <stdio.h>
#include <string.h>

#define MAX 100

int trans[MAX][3][MAX], count[MAX][3];
int states = 0, start, accept;

typedef struct {
    int s, e;
} Frag;

Frag st[MAX];
int top = -1;

void add(int from, int sym, int to) {
    trans[from][sym][count[from][sym]++] = to;
}

int isalpha_(char c) {
    return c >= 'a' && c <= 'b';
}

int prec(char c) {
    if(c == '*') return 3;
    if(c == '.') return 2;
    if(c == '+') return 1;
    return 0;
}

void add_concat(char *re, char *out) {
    int n = 0;

    for(int i = 0; re[i]; i++) {
        char c = re[i];

        if(i > 0) {
            char p = re[i-1];

            if((isalpha_(p) || p == ')' || p == '*') &&
               (isalpha_(c) || c == '('))
                out[n++] = '.';
        }

        out[n++] = c;
    }

    out[n] = '\0';
}

void postfix(char *re, char *out) {
    char op[MAX];
    int t = -1, n = 0;

    for(int i = 0; re[i]; i++) {
        char c = re[i];

        if(isalpha_(c))
            out[n++] = c;

        else if(c == '(')
            op[++t] = c;

        else if(c == ')') {
            while(t >= 0 && op[t] != '(')
                out[n++] = op[t--];
            t--;
        }

        else {
            while(t >= 0 && op[t] != '(' &&
                  prec(op[t]) >= prec(c))
                out[n++] = op[t--];

            op[++t] = c;
        }
    }

    while(t >= 0)
        out[n++] = op[t--];

    out[n] = '\0';
}

void build(char *post) {
    for(int i = 0; post[i]; i++) {
        char c = post[i];

        if(isalpha_(c)) {
            int s = states++, e = states++;
            add(s, c == 'a' ? 1 : 2, e);
            st[++top] = (Frag){s, e};
        }

        else if(c == '.') {
            Frag b = st[top--];
            Frag a = st[top--];

            add(a.e, 0, b.s);
            st[++top] = (Frag){a.s, b.e};
        }

        else if(c == '+') {
            Frag b = st[top--];
            Frag a = st[top--];

            int s = states++, e = states++;

            add(s, 0, a.s);
            add(s, 0, b.s);
            add(a.e, 0, e);
            add(b.e, 0, e);

            st[++top] = (Frag){s, e};
        }

        else if(c == '*') {
            Frag a = st[top--];

            int s = states++, e = states++;

            add(s, 0, a.s);
            add(s, 0, e);
            add(a.e, 0, a.s);
            add(a.e, 0, e);

            st[++top] = (Frag){s, e};
        }
    }

    start = st[top].s;
    accept = st[top].e;
}

void closure(int set[]) {
    int changed = 1;

    while(changed) {
        changed = 0;

        for(int i = 0; i < states; i++) {
            if(!set[i]) continue;

            for(int j = 0; j < count[i][0]; j++) {
                int t = trans[i][0][j];

                if(!set[t]) {
                    set[t] = 1;
                    changed = 1;
                }
            }
        }
    }
}

int main() {
    char re[MAX], r2[MAX], post[MAX];
    char input[MAX];
    int current[MAX] = {0};

    printf("Enter regular expression: ");
    scanf("%99s", re);

    add_concat(re, r2);
    postfix(r2, post);
    build(post);

    printf("Enter input string: ");
    scanf("%99s", input);

    current[start] = 1;
    closure(current);

    for(int i = 0; input[i]; i++) {
        if(input[i] != 'a' && input[i] != 'b') {
            printf("REJECTED\n");
            return 0;
        }

        int next[MAX] = {0};
        int sym = input[i] == 'a' ? 1 : 2;

        for(int j = 0; j < states; j++) {
            if(!current[j]) continue;

            for(int k = 0; k < count[j][sym]; k++)
                next[trans[j][sym][k]] = 1;
        }

        closure(next);
        memcpy(current, next, sizeof(current));
    }

    if(current[accept])
        printf("ACCEPTED\n");
    else
        printf("REJECTED\n");

    return 0;
}