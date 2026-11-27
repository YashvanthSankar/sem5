# Compiler Design - Endsem Portions

Prepared from the material in `midsem/`, `after-midsem/`, and `b1/` on 23 November 2026.

This is a consolidated study checklist of the supplied material, including pre-midsem topics. No separate endsem exclusion notice or marks distribution was supplied, so this document does not assume that earlier topics are excluded. Repeated material is merged. Suggested practice order is guidance, not a prediction of exam weightage.

## 1. Compiler fundamentals

- [ ] Definition and purpose of a compiler; translation while preserving program meaning.
- [ ] Compiler vs interpreter vs hybrid/bytecode/JIT execution.
- [ ] Language-processing system: preprocessor, compiler, assembler, linker, loader; source, assembly, relocatable object, and executable code.
- [ ] Analysis and synthesis; front end, intermediate representation, and back end.
- [ ] All compiler phases: lexical analysis, syntax analysis, semantic analysis, intermediate code generation, optimization, and target code generation.
- [ ] Input and output of each phase; symbol-table management and error handling across phases.
- [ ] Trace `position = initial + rate * 60` through tokens, syntax tree, type conversion, TAC, optimized TAC, and target instructions.
- [ ] Symbol-table information: identifier, type, scope, storage/offset; procedure parameters and return type.
- [ ] Cross compilation, host and target machines, retargeting, and portability.
- [ ] Introductory history and motivation: A-0, FORTRAN, LISP, COBOL, ALGOL, C, Yacc, GCC, LLVM, and JIT compilation.

**Sources:** M1, M2, M3, M4.

## 2. Lexical analysis, regular languages, and automata

### 2.1 Scanner and token recognition

- [ ] Scanner's role and interaction with the parser through token requests.
- [ ] Token, token name, pattern, lexeme, and attribute value; identify each in sample source code.
- [ ] Keywords, identifiers, numeric constants, string literals, operators, and delimiters.
- [ ] Whitespace/comment handling and symbol-table interaction.
- [ ] Reasons for separating lexical analysis from parsing: simplicity, efficiency, and portability.
- [ ] Lexical errors and recovery by deletion, insertion, replacement, or transposition.
- [ ] Transition diagrams for relational operators, identifiers/keywords, unsigned numbers with fractions/exponents, and whitespace.
- [ ] Retracting an extra character after recognizing a token; longest-match recognition and rule priority.

### 2.2 Regular expressions and construction of recognizers

- [ ] Alphabet, string, empty string, string length, language, empty language, prefix, suffix, substring, subsequence, and proper variants.
- [ ] Union, concatenation, Kleene closure, and positive closure of languages.
- [ ] RE base cases, formation rules, represented languages, algebraic laws, and precedence: repetition before concatenation before union.
- [ ] Regular definitions/macros for identifiers, whitespace, unsigned integers, floating-point numbers, and exponents.
- [ ] RE extensions: `+`, `?`, character classes, and ranges.
- [ ] DFA, NFA, epsilon transitions, accepting states, transition tables, and recognition of strings.
- [ ] Thompson construction: base cases, union, concatenation, and Kleene star; construct an epsilon-NFA for an RE.
- [ ] Epsilon-closure and move; NFA-to-DFA subset construction, including accepting subsets.
- [ ] Combine token NFAs through a common start state; convert to a DFA and associate accepting states with token actions.
- [ ] Complete scanner-generation sequence: RE -> NFA -> DFA -> minimized DFA -> transition table and driver.

### 2.3 DFA minimization

- [ ] Equivalent vs distinguishable states; distinguishing suffixes/strings.
- [ ] Remove unreachable states before minimization.
- [ ] Partition refinement: final/nonfinal partition, repeated splitting, stable partition, quotient DFA.
- [ ] Table filling: mark final/nonfinal pairs, propagate distinguishability, merge unmarked pairs.
- [ ] Construct the minimized transition table and diagram, with correct start and accepting blocks.
- [ ] Work all three DFA examples in M6; explain why both minimization methods agree.

**Sources:** M5, M6, M7, M8.

## 3. Pumping lemma and limitations of lexical analyzers

- [ ] State the pumping lemma for regular languages, including `w = xyz`, `|xy| <= p`, `|y| >= 1`, and `xy^i z` in the language for every `i >= 0`.
- [ ] Understand repeated DFA states, loops, and the pigeonhole principle.
- [ ] Quantifier order and contradiction-proof template: choose a witness after obtaining `p`; handle every valid decomposition.
- [ ] Why checking one decomposition or choosing a convenient `y` is insufficient.
- [ ] Why the pumping lemma cannot establish regularity.
- [ ] Worked nonregular languages: equal counts `a^n b^n`, repeated strings `ww`, prime unary lengths, and `a^n b^(2n)`.
- [ ] Exercises: `0^n1^n`, `a^n b^n c^n`, unequal counts `a^n b^m` with `n != m`, and perfect-square unary lengths.
- [ ] Finite-memory limitations: balanced parentheses, arbitrary nesting, and unbounded counting.
- [ ] Separate token recognition, syntactic nesting, and semantic checks such as declarations, scope, and types.

**Source:** M7. The unequal-count exercise is a question to solve; do not assume the language is regular.

## 4. Flex / Lex

- [ ] Purpose of a lexical-analyzer generator and its DFA-based implementation.
- [ ] Three sections of a `.l` file: definitions, rules, user subroutines; `%%` separators and `%{ ... %}` C declarations.
- [ ] RE macros and `pattern { action }` rules; discarding whitespace and handling unmatched characters.
- [ ] `yylex()`, `yytext`, `yyleng`, `yylval`, `yylineno`, `yywrap()`, and `%option noyywrap`.
- [ ] Longest match first; earliest rule wins only when match lengths tie; keywords before the general identifier rule.
- [ ] Workflow: `lexer.l` -> `flex` -> `lex.yy.c` -> C compiler -> scanner; purpose of `-lfl` when required.
- [ ] Write/trace the numeric and word counter example and simple token-recognition rules.
- [ ] Start conditions: inclusive `%s`, exclusive `%x`, `BEGIN`, `INITIAL`, and state-prefixed rules such as `<COMMENT>`.
- [ ] State-based handling of comments; debugging with `flex -d`; rule-order and scanner-progress pitfalls.

**Source:** M8.

## 5. CFGs and grammar preparation

- [ ] Role of the parser: structural checking, parse-tree construction, syntax-error reporting/recovery.
- [ ] CFG four-tuple, terminals, nonterminals, productions, start symbol, sentences, and sentential forms.
- [ ] Leftmost and rightmost derivations; construct parse trees and recover derivations from them.
- [ ] Multiple arbitrary derivation orders can represent one tree; two distinct parse trees establish ambiguity.
- [ ] Recursive/nonrecursive grammar; direct/indirect recursion; left/right recursion.
- [ ] Ambiguity in arithmetic expressions; encode precedence and associativity with layered nonterminals.
- [ ] Infer precedence/associativity from grammars, including right-associative exponentiation.
- [ ] Dangling else; nearest-unmatched-if convention; matched/unmatched statement grammar.
- [ ] Ambiguous grammar vs inherently ambiguous language; undecidability of general CFG ambiguity.
- [ ] Eliminate immediate left recursion with one or multiple recursive/nonrecursive alternatives.
- [ ] Eliminate indirect left recursion through ordered substitution followed by immediate-recursion removal (Algorithm 4.19); understand epsilon/cycle caveats.
- [ ] Left factoring of common prefixes, including epsilon suffixes and repeated factoring.
- [ ] Distinguish ambiguity removal, left-recursion removal, and left factoring; none alone guarantees LL(1).
- [ ] Effect of grammar transformation on parse-tree shape and preservation of intended associativity through semantic actions.

**Sources:** M9, M10, B1.

## 6. FIRST, FOLLOW, and top-down parsing

- [ ] Nullable symbols and nullable strings.
- [ ] FIRST of a terminal, nonterminal, epsilon, and a complete RHS; continue across nullable prefixes.
- [ ] FOLLOW rules: `$` for start symbol, `FIRST(beta) - {epsilon}` after a symbol, and propagation of the LHS FOLLOW when the suffix is nullable.
- [ ] Iterate set computation until no changes; FOLLOW never contains epsilon.
- [ ] LL(1) meaning and exact conflict tests using production prediction sets; FIRST/FIRST and FIRST/FOLLOW conflicts.
- [ ] Construct the predictive table from `FIRST(RHS)` and, for nullable RHSs, `FOLLOW(LHS)`; unused cells are errors.
- [ ] Recursive descent with backtracking vs predictive recursive descent without backtracking.
- [ ] One procedure per nonterminal; `lookahead`, `match()`, token advancement, epsilon branches, and errors.
- [ ] Write expression-parser procedures `E`, `E'`, `T`, `T'`, and `F`.
- [ ] Nonrecursive predictive parsing: input buffer, explicit stack, parse table, and output productions.
- [ ] Driver actions: expand, push RHS in reverse, match, epsilon/pop, accept, or report error.
- [ ] Full stack/input/action traces; corresponding leftmost derivation and matched-input/stack invariant.
- [ ] Panic-mode recovery using synchronizing tokens/FOLLOW sets; phrase-level recovery.
- [ ] LL vs LR: derivation direction, left-recursion support, grammar coverage, manual vs generated parsers.

**Practice:** standard expression grammar on `id+id*id` and `(id+id)*id`; list grammar `S -> (L) | a`, `L -> L,S | S`; nullable chains; left-factor `S -> 0S1 | 01`; diagnose dangling-else conflict after factoring. Also attempt the FIRST/FOLLOW and LL(1) exercises in B1.

**Sources:** M9, M10, M11, M12, B1.

## 7. Bottom-up parsing and LR parsers

### 7.1 Shift-reduce foundations and LR(0)

- [ ] Bottom-up construction and rightmost derivation in reverse.
- [ ] Handle, handle pruning, shift, reduce, accept, and error; identify the correct handle rather than any matching RHS substring.
- [ ] Shift-reduce traces for arithmetic, nested-list, and recursive grammars.
- [ ] Augment a grammar and number productions; interpret dotted LR(0) items and completed items, including epsilon items.
- [ ] CLOSURE and GOTO; construct the entire canonical collection and item-set DFA until no new states/transitions remain.
- [ ] ACTION terminal columns and GOTO nonterminal columns.
- [ ] LR(0) table rules: shifts from terminal transitions, reductions on all terminal/endmarker columns, accept for completed augmented start item on `$`.
- [ ] LR parsing stack operation, state transitions after reduction, and epsilon reductions.
- [ ] Identify shift/reduce and reduce/reduce conflicts and decide whether a grammar is LR(0).

**Practice:** `A -> aA | b` on `aab`; `S -> AA`, `A -> aA | b` on `aabb`, `abb`, `abab`, and an invalid input; contrast LR(0) and SLR for `E -> T+E | T`, `T -> a`.

### 7.2 SLR(1)

- [ ] Reuse the LR(0) item DFA and compute FOLLOW sets.
- [ ] Enter `A -> alpha` reductions only under `FOLLOW(A)`.
- [ ] Construct ACTION/GOTO, trace inputs, and show which LR(0) conflicts disappear.
- [ ] S/R conflict: a shift terminal overlaps the reduction's FOLLOW set.
- [ ] R/R conflict: FOLLOW sets of completed productions overlap in one state.
- [ ] SLR limitations: global FOLLOW sets may allow reductions in inappropriate contexts.

### 7.3 Canonical LR(1) / CLR(1)

- [ ] LR(1) item `[A -> alpha . beta, a]`: distinguish dot position from reduction lookahead.
- [ ] LR(1) closure: from `[A -> alpha . B beta, a]`, add `[B -> . gamma, b]` for terminals `b` in `FIRST(beta a)`.
- [ ] GOTO moves the dot and preserves item lookaheads before closure.
- [ ] Construct canonical LR(1) states; equal LR(0) cores with different lookaheads may be separate states.
- [ ] Reductions only under the completed item's lookahead; table construction and full parsing traces.
- [ ] Pointer-assignment grammar: `S -> L=R | R`, `L -> *R | id`, `R -> L`; explain SLR's conflict on `=` and how CLR resolves it.
- [ ] Work the 14-state CLR example and trace `id=*id`.

### 7.4 LALR(1) and comparison

- [ ] Identify CLR states with identical LR(0) cores; merge corresponding lookahead sets by union.
- [ ] Redirect transitions to merged states; build the LALR table and trace an input.
- [ ] Pointer-assignment example: CLR's 14 states become 10 LALR states; trace `id=id`.
- [ ] Merging conflict-free CLR states can introduce R/R conflicts; it cannot introduce a new S/R conflict.
- [ ] Reproduce the conflict workout: `S -> aAd | bBd | aBc | bAc`, `A -> e`, `B -> e`; here `e` is a terminal, not epsilon.
- [ ] Explain how separate reductions on `c` and `d` become conflicting after union of lookaheads.
- [ ] Attempt additional CLR/LALR conflict grammars in B1, especially slides 168-181.
- [ ] Compare LR(0), SLR(1), LALR(1), CLR(1): item types, reduction conditions, state count, power, conflicts, and practical parser generators.

| Parser | Condition for reducing a completed non-start item |
|---|---|
| LR(0) | Every terminal/endmarker column |
| SLR(1) | Terminals/endmarker in FOLLOW of its LHS |
| CLR(1) | Explicit lookaheads of that item in that state |
| LALR(1) | Lookaheads after merging states with identical LR(0) cores |

For grammar classes, remember `LR(0) ⊆ SLR(1) ⊆ LALR(1) ⊆ LR(1)`. LL(1) is also contained in LR(1); do not insert LL(1) into that chain without qualification.

**Sources:** A1, A2, A3, A4, A5, B1.

## 8. Operator-precedence parsing

- [ ] Operator-grammar restrictions: no epsilon productions and no adjacent nonterminals in a RHS.
- [ ] Operator grammar vs operator-precedence grammar; conflicting precedence relations.
- [ ] Relations: yields precedence `<.`, equal precedence `=.`, takes precedence `.>`.
- [ ] Establish relations from intended precedence/associativity and, where required, LEADING/TRAILING (FIRSTVT/LASTVT) sets.
- [ ] Build precedence tables including parentheses and `$`; distinguish these sets from ordinary FIRST/FOLLOW.
- [ ] Parser algorithm: compare topmost stack terminal with next input terminal; shift for `<.`/`=.`, find and reduce a handle for `.>`, detect errors/acceptance.
- [ ] Trace `id+id*id` with multiplication before addition and left associativity.
- [ ] B1 list example: `S -> a | ^ | (T)`, `T -> T,S | S`; build LEADING/TRAILING and the relation table (`^` is the listed terminal).
- [ ] Precedence functions `f` and `g`: equality groups, constraint graph, longest-path values, and cycle/nonexistence test.
- [ ] Relation-table storage `O(n^2)` vs two function arrays `O(n)`; blank/error relations need care when replacing a table with functions.

**Sources:** A2, B1 (slides 183-224).

## 9. Semantic analysis and syntax-directed translation

### 9.1 SDDs, attributes, and evaluation

- [ ] Semantic analysis: type compatibility, declaration/scope checks, symbol-table updates, and typed AST/IR output.
- [ ] Syntax-directed definition (SDD): CFG plus attributes and semantic rules.
- [ ] Synthesized vs inherited attributes; lexer-supplied token attributes such as `digit.lexval` and `id.entry`.
- [ ] Annotated/decorated parse trees; evaluate all attribute instances in a worked expression.
- [ ] Desk calculator: `3*5+4`, `(3+4)*(5+6)`, and other B2 arithmetic exercises.
- [ ] Inherited accumulator example for `3*5` after removing left recursion: values flow down/across, final value flows up.
- [ ] Dependency graph: one node per attribute instance, edges from prerequisite to dependent attribute.
- [ ] Construct graphs, find valid topological evaluation orders, and detect circular dependencies.
- [ ] S-attributed definitions: synthesized attributes only; postorder evaluation and LR reductions.
- [ ] L-attributed definitions: inherited dependencies from the head's inherited attributes and left siblings, plus permitted noncyclic same-symbol dependencies.
- [ ] Classify supplied rules as S-attributed, L-attributed, or neither; recognize right-sibling violations.
- [ ] Every S-attributed SDD is L-attributed; compare evaluation order and implementation.
- [ ] Controlled side effects: printing, code emission, and symbol-table updates; consistent ordering of effects.
- [ ] Declaration-list example: pass `int`, `real`, or `float` to all identifiers through inherited attributes and `addType`.

### 9.2 Applications and syntax trees

- [ ] Parse tree vs AST; operator nodes, identifier leaves, numeric leaves, and pointer-valued attributes.
- [ ] Construct ASTs using `mknode/new Node` and `mkleaf/new Leaf` semantic rules.
- [ ] S-attributed bottom-up AST construction and L-attributed top-down construction preserving left associativity.
- [ ] Work `a+b*c` and `a-4+c`; distinguish pointer propagation from allocating a new node.
- [ ] Array type expressions and annotated trees: `int[2][3]` becomes `array(2,array(3,integer))`.
- [ ] Applications listed in B2: expression evaluation, infix-to-postfix/prefix, binary-to-decimal, reduction counting, intermediate code, type checking, and storing type information. Some are listed applications rather than fully worked examples.

### 9.3 Translation schemes and implementations

- [ ] SDD vs SDT/translation scheme: semantic equations vs explicitly positioned executable actions.
- [ ] Action execution order as a depth-first, left-to-right traversal with action leaves.
- [ ] Postfix SDTs: actions at production ends, executed on reduction.
- [ ] LR parser semantic-value stack; access RHS values and install the synthesized LHS value after reduction.
- [ ] Convert an L-attributed SDD to an SDT: inherited computation before the relevant symbol, synthesized head computation at the end.
- [ ] Recursive-descent implementation: inherited values as parameters; synthesized values as return values.
- [ ] Preserve computations when eliminating left recursion by carrying an inherited accumulator.
- [ ] Embedded actions in LR parsing via epsilon-marker nonterminals; possible new parsing conflicts.
- [ ] Work infix-to-postfix on `a+b*c` and `9-5+2`; accumulator evaluation on `3+5`; declaration and while-code examples.

**Sources:** A6, A7, B2. A6 also lists Dragon Book exercises 5.1.1, 5.2.2, and 5.4.1.

## 10. Intermediate code, declarations, and expressions

- [ ] Purpose of IR: portability, modular front/back ends, easier analysis/optimization, and simplified code generation; `M+N` front/back ends vs `M*N` complete translators.
- [ ] Forms: AST, DAG, postfix notation, three-address code, and SSA.
- [ ] AST vs DAG: share common subexpressions; construct DAGs and identify value numbers as in B3.
- [ ] TAC instructions: binary/unary assignment, copies, conditional/unconditional jumps, indexed loads/stores, address/pointer operations, parameter passing, calls, and returns.
- [ ] Translate arithmetic expressions, unary minus, assignments, array accesses, pointer accesses, loops, and procedure calls into TAC.
- [ ] Quadruples `(op,arg1,arg2,result)`, triples `(op,arg1,arg2)`, and indirect triples with a pointer/order table.
- [ ] Convert the same expression into all representations; compare temporaries, positional references, space, and reordering during optimization.
- [ ] Practice repeated subexpressions such as `a=b*-c+b*-c` and `x=-a*b+-a*b`; distinguish direct translation from common-subexpression sharing.
- [ ] B3 exercises: `a+-(b+c)`, `a=b[i]+c[j]`, `a[i]=b*c-b*d`, and `x=f(y+1)+2`.
- [ ] B3 worked source examples: array dot product, pointer-based dot product, procedure version, and recursive factorial.
- [ ] SSA basics: versions for assignments, definition/use relationship, and phi-functions at control-flow joins; convert a simple if/else assignment.
- [ ] Type constructors, base types/widths, nested array types, and relative offsets for declarations.
- [ ] Semantic actions using `enter`, type, width, and offset; inherited base type/width and synthesized array type/size.
- [ ] Trace `int[2][3] x; float y;` using the handout's sizes (int 4 bytes, float 8 bytes): x width 24 at offset 0; y at offset 24; final offset 32, under its simplified layout.
- [ ] Expression translation using `.addr`/`.place`, `newtemp()`, and `emit()`.

**Sources:** A8, A9, B3; AST/type foundations also in A6 and B2.

## 11. Boolean expressions, control flow, and backpatching

- [ ] Boolean expressions as numerical values vs control-flow conditions.
- [ ] Numerical true/false representation and TAC for relational/logical operators.
- [ ] Short-circuit translation for AND, OR, NOT, relational tests, `true`, and `false`.
- [ ] Inherited labels `B.true`, `B.false`, and `S.next`; generate control-flow code without materializing Boolean values.
- [ ] TAC templates for if, if/else, while, do/while, and for; body, condition, update, and exit labels.
- [ ] Why forward jump targets are initially unknown; label resolution vs list-based backpatching.
- [ ] `nextinstr`/`nextquad`, `makelist(i)`, `merge(p1,p2)`, `backpatch(p,i)`.
- [ ] `B.truelist`, `B.falselist`, and `S.nextlist`; epsilon marker `M` records the next instruction address.
- [ ] OR: patch the left operand's false exits to the right operand; merge true lists.
- [ ] AND: patch the left operand's true exits to the right operand; merge false lists.
- [ ] NOT: swap true/false lists; relational tests emit a conditional jump plus an unresolved unconditional jump.
- [ ] Statement sequencing, if, if/else, and while: maintain pending exits and patch at the correct marker.
- [ ] `breaklist` and `continuelist`; propagation through statement lists, loop handling, and detection of use outside loops.
- [ ] Continue target: while -> condition; C-style for -> update/increment.
- [ ] Full trace with emitted instruction numbers, intermediate lists, patch operations, and final targets.

**Required worked practice from the supplied notes:**

1. `if (x<100 || x>200 && x!=y) x=0;`, beginning at instruction 100.
2. `if (a<b or c<d) then x=1`, including the unresolved enclosing nextlist.
3. `while (x<10) { if (x==5) break; x=x+1; }`.
4. A for loop with continue; explain why it must execute the update step.

**Sources:** A8, A9, A10; loop/TAC examples also in A6 and B3.

## 12. Procedures and runtime environments

### 12.1 Procedure translation

- [ ] TAC: `param x`, `call p,n`, `t=call p,n`, `return x`, and void return.
- [ ] Evaluate arguments and collect addresses in an ordered argument list before emitting parameters for the enclosing call.
- [ ] Translate `x=f(a,g(b+1,c),d)` without interleaving inner/outer parameter sets.
- [ ] Purpose of parameter count, including stack cleanup and variable-argument calls.
- [ ] Scoped symbol-table/environment stack for procedure declarations: enter procedure, create local table, reset/update offsets, emit body/return, restore parent environment.
- [ ] Call by value, reference, and result; effects on caller variables and address/value passing.

### 12.2 Runtime storage and activation records

- [ ] Runtime support and virtual address space.
- [ ] Process memory organization: text/code, initialized data, BSS, heap, stack, and free space; identify each variable's storage region.
- [ ] Static, stack, and heap allocation: allocation time, lifetime, recursion support, and dynamic structures.
- [ ] Procedure activation and lifetime; activation records and runtime call stack.
- [ ] Frame fields: actual parameters, return value, control/dynamic link, access/static link, saved machine status/return address, locals, and temporaries.
- [ ] Dynamic link -> caller; static link -> lexical enclosing activation for nonlocal access.
- [ ] Stack pointer vs frame pointer; parameter/local offsets under the illustrated x86 convention.
- [ ] Calling sequence, callee prologue, epilogue, and return sequence; caller-saved vs callee-saved registers.
- [ ] Trace recursive `fact(2)` -> `fact(1)`, draw simultaneous frames, and explain restoration after return.
- [ ] Understand the handout's `push`, frame setup, local allocation, `call`, return register, `leave`, and `ret` example. Exact layout/register rules depend on the calling convention.

**Sources:** A10, A11; procedure TAC examples also in B3.

## 13. Supplementary / outline-only coverage

These topics occur in introductions, contents lists, or short references. They are retained here so they are visible, but the supplied material does not establish a full taught endsem unit for each.

| Topic | What the supplied files support |
|---|---|
| Switch/case translation | Listed in B3's contents; no comparable worked switch translation section in that deck |
| Code optimization | Phase overview, small optimized expression example, DAG sharing, SSA motivation, and named optimizations such as dead-code elimination/constant folding/loop optimization |
| Detailed data-flow algorithms | Course roadmap mention; no dedicated detailed lecture supplied |
| Register allocation/instruction selection | Roadmap and GCC RTL references; no dedicated construction algorithm supplied |
| Garbage collection | Historical/runtime/heap mention; no dedicated collector algorithm supplied |
| LLVM / modern backends | Introductory and optional-roadmap mentions |
| CYK / Earley | Parsing taxonomy overview; no full algorithm walkthrough supplied |
| GCC inspection commands | Dedicated reference M4; useful for phase/tool questions |

For GCC, revise `-E`, `-S`, `-c`, `-o`, `-save-temps`, GIMPLE/tree dumps, SSA/CFG dumps, RTL dumps, optimization reports, and original-vs-optimized output. M4 also includes IPA/call-graph/language dumps, pass listings, dump modifiers/names, and GraphViz recipes. Treat command recipes as supplied reference material rather than inferring a separate optimization syllabus.

## 14. Corrections to keep in mind while revising

- FIRST/FOLLOW computation works on general CFGs, including left-recursive ones. Grammar transformation is needed for predictive parsing, not to make these set definitions exist.
- Unambiguous + no left recursion + left factoring is not a sufficient LL(1) test. Production prediction sets must be pairwise disjoint; checking only the intersection of all alternatives is insufficient.
- Left factoring does not remove ambiguity; the factored dangling-else grammar still has a conflict.
- A recursive production does not automatically imply an infinite language; it must support productive repeated derivations. A grammar with only one alternative per nonterminal is not automatically a usable LL(1) grammar.
- LALR does not preserve every CLR grammar's conflict-free behavior: equal-core merging can create R/R conflicts. The unconditional claim on the LALR lecture's summary slide is too strong.
- In M6's third DFA example, the final blocks are `{0}`, `{1}`, `{2}`, `{3,4,5}`; the later claim that `{0,2}` is an equivalent pair is inconsistent with its own distinguishing transition.
- S-attributed attributes can also be evaluated recursively over a tree; bottom-up LR parsing is a natural implementation, not the only possible evaluator.
- A DAG and TAC are distinct IR forms. A DAG is not itself a three-address-code instruction sequence.
- Place an inherited-attribute action only after its inputs exist. In A9's type-declaration scheme, evaluate `B` before assigning `C.b=B.type` and `C.w=B.width`, then parse `C`.
- Use stated type sizes and conventions in a numerical problem. The handout's float width, alignment simplifications, x86 offsets, and stack-growth illustration are not universal language/machine rules.

## 15. Suggested practice order

This order follows the dependencies and amount of worked material, without assuming exam marks.

1. Grammar transformations -> FIRST/FOLLOW -> LL(1) tables and parsing traces.
2. Handles/shift-reduce -> LR(0) -> SLR -> CLR -> LALR; build tables and diagnose conflicts.
3. Operator-precedence tables, traces, and precedence functions.
4. SDD attributes, annotated trees, dependency graphs, S/L classification, and SDT implementations.
5. AST/DAG, TAC, quadruples/triples/indirect triples, and declaration types/offsets.
6. Boolean short circuit, backpatching, loops, break/continue, and nested calls.
7. Runtime layout, activation records, calling sequences, and parameter passing.
8. RE/NFA/DFA construction, minimization, pumping-lemma proofs, Flex, and compiler-phase revision.

For each construction topic, complete at least one example from an empty page and one example that contains a conflict, invalid input, epsilon production, or nested construct where applicable.

## 16. Source inventory

The 26 teaching files below were used for this consolidation. `Archive.zip` contains byte-identical copies of these same files, so it contributes no additional unique teaching document. Page/slide counts include covers, references, and closing pages.

### Midsem folder

| ID | File | Slides/pages | Main coverage |
|---|---|---:|---|
| M1 | `midsem/Compiler_Design_Lecture_01.pptx` | 16 | Introduction, history, phases, course/lab roadmap |
| M2 | `midsem/Compiler Design_lecture_2.pptx` | 18 | Language processing, phases, cross compiler, symbol table |
| M3 | `midsem/Compiler design.pdf` | 7 | Handwritten introduction and photographs of introductory/GCC slides |
| M4 | `midsem/GCC_Compiler_Phases_Reference.pdf` | 5 | GCC intermediate outputs and inspection commands |
| M5 | `midsem/Lexical Analysis_Lecture4.pptx` | 34 | Tokens, REs, transition diagrams, Thompson construction, scanner generation |
| M6 | `midsem/DFA_Minimization_Lecture_5.pptx` | 19 | Partition refinement and table filling |
| M7 | `midsem/Pumping_Lemma_and_Lexical_Analyzer_Limitations.pptx` | 24 | Pumping lemma, proofs, scanner limits |
| M8 | `midsem/Flex_ The Lexical Analyzer Generator.pptx` | 13 | Flex specification, APIs, priority, start conditions |
| M9 | `midsem/Syntax Analysis - Chapter 4_lect_1.pptx.pdf` | 16 | CFG, derivations, trees, parser families |
| M10 | `midsem/Ambiguity_LeftRecursion_LeftFactoring.pptx` | 20 | Ambiguity, dangling else, grammar transformations |
| M11 | `midsem/FIRST_FOLLOW_Compiler_Design.pptx` | 20 | FIRST/FOLLOW, LL(1) table, conflicts |
| M12 | `midsem/Recursive_Descent_TopDown_Parsing.pptx` | 20 | Recursive descent, predictive parser, traces, recovery |

### After-midsem folder

| ID | File | Pages | Main coverage |
|---|---|---:|---|
| A1 | `after-midsem/lr0_parsing_tutorial.pptx.pdf` | 10 | LR(0) items, automaton, table, trace |
| A2 | `after-midsem/Syntax Analysis_ OPP and SLR(1) Parsing.pdf` | 14 | Operator precedence and SLR construction/traces |
| A3 | `after-midsem/Canonical LR(1) Parsing.pdf` | 13 | LR(1) closure, pointer grammar, CLR table/trace |
| A4 | `after-midsem/LALR Parsing Full Lecture.pdf` | 14 | Equal-core merging, LALR table, comparison |
| A5 | `after-midsem/LALR_Parsing_Conflict_Workout.pdf` | 7 | R/R conflict introduced by merging |
| A6 | `after-midsem/CS-304 Compiler Design_ Syntax-Directed Translation (Dragon Book Ch. 5).pdf` | 42 | Attributes, dependency graphs, S/L definitions, ASTs, array types, SDT implementations |
| A7 | `after-midsem/Compiler Design_ Syntax-Directed Translation Schemes (SDTs).pdf` | 5 | SDD vs SDT, parser-stack and recursive-descent implementations |
| A8 | `after-midsem/Compiler Design_ Intermediate Code Generation.pdf` | 6 | TAC representations, SSA, declarations, arithmetic/Boolean translation |
| A9 | `after-midsem/type_declaration_boolean_expression.pdf` | 6 | Type/width/offset, Boolean values, short circuit, backpatching |
| A10 | `after-midsem/backpatching.pdf` | 7 | Backpatching, loops, break/continue, procedure calls/scopes/parameters |
| A11 | `after-midsem/run_time_environment.pdf` | 5 | Memory layout, activation records, call/return, allocation strategies |

### B1 folder

| ID | File | Slides | Main coverage |
|---|---|---:|---|
| B1 | `b1/Module2.pptx` | 224 | Broad syntax analysis: grammar preparation, FIRST/FOLLOW, LL(1), LR family, OPP and precedence functions |
| B2 | `b1/Semantic Analysis.pptx` | 47 | SDD/SDT, annotated trees, dependencies, S/L definitions, translation applications |
| B3 | `b1/ICG_updated.pptx` | 58 | AST/DAG/postfix, TAC, quadruples/triples/indirect triples, array/pointer/call examples |

B1 explicitly says “refer to class notes” for some brute-force/general recursive-descent explanations and construction steps. Those separate class notes were not present; the overlapping supplied lectures cover the main methods listed above.
