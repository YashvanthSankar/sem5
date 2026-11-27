# Compiler Design: exam lab solutions (Q6-Q10)

The revised solutions are installed in their original lab folders. There is one
`solution.c` per lab for Q6-Q9 and the required `calc.l`/`calc.y` pair for Q10.
This folder contains only the guide, sample data and verification script.

| Lab | File(s) | Remember the sequence |
| --- | --- | --- |
| Q6 | `../q6_first_follow/solution.c` | Add -> FIRST of a string -> repeat FIRST -> repeat FOLLOW -> print |
| Q7 | `../q7_ll1_table/solution.c` | Q6 -> collect columns -> FIRST(rhs) -> FOLLOW(lhs) if nullable -> table |
| Q8 | `../q8_lr0_items/solution.c` | Augment -> closure -> move dot -> closure -> reuse an old state |
| Q9 | `../q9_slr_parser/solution.c` | Q8 states + Q6 FOLLOW -> shift/reduce/accept table -> parse |
| Q10 | `../q10_bison_calculator/calc.l`, `../q10_bison_calculator/calc.y` | Tokens -> precedence -> grammar -> arithmetic actions |

These revisions start from your shorter `simple.c` approach. Q6 is 76 lines,
Q7 87, Q8 89, and Q9 241, including comments and blank lines. Q7 computes sets
instead of adding a separate set-input reader and generates cells directly
instead of storing another table. Q9 uses numeric actions to simplify table
construction and parsing.

Q9 is longer because it includes three real algorithms. Learn it in blocks rather
than as one long program. Q6's set functions are identical in Q7 and Q9; Q8's LR
functions are identical in Q9. Every C file is standalone: no shared header to copy.

## Compile and run

From the project root, compile and run each C solution in its own lab folder:

```sh
cd q6_first_follow
gcc -std=c99 solution.c -o solution
./solution < ../lab_support/samples/q6.in
```

Use the corresponding Q7, Q8 or Q9 folder and sample file for those labs.
Q6-Q8 finish after the productions. Q9 reads one test-string line after them.

For Q10, from the project root:

```sh
cd q10_bison_calculator
bison -d calc.y
flex calc.l
gcc calc.tab.c lex.yy.c -o calc
./calc < ../lab_support/samples/q10.in
```

`calc.tab.c`, `calc.tab.h`, and `lex.yy.c` are generated files. Write only `calc.l`
and `calc.y` in the lab. A newline ends each expression. Ctrl+D ends an interactive
session. The handout's `%union` gives the integer and variable index separate fields.

From the project root, run `python3 lab_support/verify.py` to check all labs.
Use `python3 lab_support/verify.py --sanitize` for memory/undefined-behavior checks.
The test script and guide are study aids, not code to write in exams.

## Input conventions

- For every grammar program, the first line is the number of productions.
- A nonterminal is one uppercase letter. A terminal is one ASCII character;
  use one line per alternative. Write `#` for epsilon and `$` for end of input.
- Q6/Q7: use `A=rhs`, with no spaces inside a production. The first LHS is the
  start symbol. For example, split `A=a|b` into `A=a` and `A=b` and count both.
- Q7 recomputes FIRST/FOLLOW using Q6 routines, so no separate sets need to be
  typed. If the sample input contains those sets after the grammar, they are
  left unread; the table uses the computed sets.
- Q8/Q9: use `A->rhs`. Q8 takes productions without spaces and uses single
  character symbols (write `i` for the token id). Q9 removes spaces and turns
  `id` into `i`, which is also how it displays the token. The dot `.` is reserved
  for LR items. An epsilon item is `A->.`; there is no transition on `#`.
- Q8/Q9 automatically add a fresh augmented production. Normally enter the
  original grammar without its augmented rule. If you also enter `S->E`,
  the program adds another start rule; the language is unchanged but rule and
  state numbers can differ from the handout. Rule 0 is the generated start rule; input rules are numbered 1 onward.
- Q9: put the test string on the next line. A blank line represents the empty
  string. A trailing `$` is optional. Only an SLR(1) grammar is parsed: conflicts
  are reported rather than silently resolved.
- Limits: 29 input productions, each at most 59 characters; Q8/Q9 allow 100
  stored states and 30 items per state and need an unused uppercase letter for
  augmentation. Q9 production lines including spaces must fit 62 characters. Q9 input is at most 252 characters including spaces; enter it
  on one line. Use valid grammar syntax and defined nonterminals.
- Q10 uses integer values and lowercase single-letter variables `a` to `z`.
  Unassigned variables start at zero. Arithmetic must fit a C `int`; floating
  point, multi-letter names, `%`, and `^` belong to the optional extension,
  which is available in `q10_bison_calculator/extension`. Build it there with
  `bison -d calc_ext.y`, `flex calc_ext.l`, and
  `gcc -o calc_ext calc_ext.tab.c lex.yy.c -lm`. Run `./calc_ext`.

## Samples and output

`samples/q6.in` through `samples/q10.in` contain ready-to-run inputs.
Their corresponding `.out` files contain stdout captured from these programs;
Q10's `.err` file contains the division-by-zero error written to stderr.

Q6 uses the question's expression grammar and prints its expected FIRST/FOLLOW
sets. Q7 uses the question's four-rule grammar and prints its expected table.
Q8 uses `S->(S)` and `S->a` and generates the six sample states.
Q9 uses the six expression productions (without the augmented rule) and accepts
`id + id * id`. Q10 prints 11, 14, assignments a=25 and b=20, then 0 and 5;
it reports division by zero for `b/0`, as the handout requires.

Equivalent FIRST/FOLLOW sets may print in a different order. Equivalent LR states
may have different numbers. Prompts, tabs, and a state-only parsing stack can also
differ from a handout; they do not change algorithmic correctness. If your marking
system compares output literally, follow its exact formatting requirements.

## Viva memory cues

**FIRST:** scan left to right. A terminal stops the scan. For a nonterminal,
copy its FIRST except `#`; continue only if it can vanish. If the entire RHS can
vanish, add `#` to the LHS's FIRST.

**FOLLOW:** the start symbol gets `$`. In `A->alpha B beta`, FOLLOW(B) gets
FIRST(beta) except `#`. If beta can vanish, it also gets FOLLOW(A).
Repeat until nothing changes.

**LL(1):** `A->rhs` goes under FIRST(rhs) except `#`. If rhs is nullable, it also
goes under FOLLOW(A). Two productions in a cell mean a conflict.

**LR(0):** closure expands a nonterminal immediately after a dot. GOTO moves the
dot over one symbol, then takes closure. Compare whole item sets, ignoring order.

**SLR:** terminal edge means shift; nonterminal edge means GOTO. A completed
`A->rhs.` means reduce on FOLLOW(A). The completed augmented rule means accept
on `$`. Shift pushes a state and consumes input; reduce pops the RHS length
and pushes GOTO. Epsilon has RHS length zero.

**Bison:** `$1`, `$2`, `$3` are RHS values; `$$` is the LHS value. Later precedence
declarations bind tighter. `%prec UMINUS` gives unary minus higher precedence.
`error '\n'` with `yyerrok` recovers at the next line. The lexer returns an
unexpected character to the parser so bad input cannot silently become valid.
