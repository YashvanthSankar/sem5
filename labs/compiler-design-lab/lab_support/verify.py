"""Compile in a temporary directory and check lab outputs: python3 verify.py."""
from pathlib import Path
import itertools
import re
import shutil
import sys
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
checks = 0
flags = ['-std=c99', '-D_POSIX_C_SOURCE=200809L', '-Wall', '-Wextra', '-Werror']
if '--sanitize' in sys.argv:
    flags += ['-fsanitize=address,undefined']

def check(ok, message):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(message)

def run(name, data):
    result = subprocess.run([str(build / name)], input=data, text=True,
                            capture_output=True, timeout=5)
    check(result.returncode == 0, name + ': ' + result.stderr)
    return result.stdout, result.stderr

def sets(output):
    return {name: set(body.split()) for name, body in
            re.findall(r'((?:FIRST|FOLLOW)\([A-Z]\)) = \{([^}]*)\}', output)}

with tempfile.TemporaryDirectory(prefix='exam-labs-') as tmp:
    build = Path(tmp)
    for q, folder in [(6, 'q6_first_follow'), (7, 'q7_ll1_table'),
                      (8, 'q8_lr0_items'), (9, 'q9_slr_parser')]:
        src = ROOT.parent / folder / 'solution.c'
        subprocess.run(['gcc', *flags, str(src),
                        '-o', str(build / f'q{q}')], check=True, capture_output=True)

    # Losing nullable propagation must break these hand-derived sets.
    sample = '8\nE=TX\nX=+TX\nX=#\nT=FY\nY=*FY\nY=#\nF=(E)\nF=i\n'
    actual = sets(run('q6', sample)[0])
    expected = {'FIRST(E)': {'(', 'i'}, 'FIRST(X)': {'+', '#'},
                'FIRST(T)': {'(', 'i'}, 'FIRST(Y)': {'*', '#'},
                'FIRST(F)': {'(', 'i'}, 'FOLLOW(E)': {'$', ')'},
                'FOLLOW(X)': {'$', ')'}, 'FOLLOW(T)': {'+', '$', ')'},
                'FOLLOW(Y)': {'+', '$', ')'}, 'FOLLOW(F)': {'*', '+', '$', ')'}}
    check(actual == expected, 'Q6 expression sets')
    actual = sets(run('q6', '5\nS=AB\nA=a\nA=#\nB=b\nB=#\n')[0])
    check(actual['FIRST(S)'] == {'a', 'b', '#'}, 'Q6 nullable FIRST')
    check(actual['FOLLOW(A)'] == {'b', '$'}, 'Q6 nullable FOLLOW')
    actual = sets(run('q6', '3\nS=A\nA=B\nB=c\n')[0])
    check(actual['FIRST(S)'] == {'c'}, 'Q6 repeated propagation')

    output = run('q7', '4\nS=aA\nA=bA\nA=#\nA=c\n')[0]
    check('S\tS=aA\terror\terror\terror' in output, 'Q7 start row')
    check('A\terror\tA=bA\tA=c\tA=#' in output, 'Q7 nullable row')
    output = run('q7', '5\nS=AB\nA=a\nA=#\nB=b\nB=#\n')[0]
    check('S\tS=AB\tS=AB\tS=AB' in output, 'Q7 nullable RHS table')

    output = run('q7', '3\nS=aA\nS=aB\nA=b\n')[0]
    check('not LL(1)' in output, 'Q7 FIRST/FIRST conflict')
    given = ('4\nS=aA\nA=bA\nA=#\nA=c\nFIRST(S) = { a }\n'
             'FIRST(A) = { b c # }\nFOLLOW(S) = { $ }\nFOLLOW(A) = { $ }\n')
    check('A\terror\tA=bA\tA=c\tA=#' in run('q7', given)[0], 'Q7 supplied sets')

    output = run('q8', '2\nS->(S)\nS->a\n')[0]
    check(output.count('I0:') == 1 and 'S->(S).' in output, 'Q8 closure/goto')
    check(len(re.findall(r'^I\d+:', output, re.M)) == 6, 'Q8 deduplicated states')
    output = run('q8', '1\nS->#\n')[0]
    check('S->.\n' in output and '#' not in output, 'Q8 epsilon must be an empty RHS')

    output = run('q8', '2\nZ->A\nA->a\n')[0]
    check('Y->.Z' in output and 'A->a.' in output, 'Q8 fresh augmented symbol')

    output = run('q9', '2\nS->A\nA->#\n\n')[0]
    check('Input string is accepted.' in output, 'Q9 epsilon acceptance')
    grammar = '7\nS->E\nE->E+T\nE->T\nT->T*F\nT->F\nF->(E)\nF->id\n'
    for word, accepted in [('id+id*id', True), ('(id+id)*id', True),
                           ('id+*id', False), ('(id', False), ('x', False)]:
        output = run('q9', grammar + word + '\n')[0]
        verdict = 'accepted' if accepted else 'rejected'
        check(f'Input string is {verdict}.' in output, 'Q9 ' + word)
    output = run('q9', '3\nS->AB\nA->#\nB->b\nb\n')[0]
    check('Input string is accepted.' in output, 'Q9 nullable prefix')
    output = run('q9', '2\nE->E+E\nE->i\ni+i+i\n')[0]
    check('not SLR(1)' in output, 'Q9 conflicts must not silently overwrite actions')

    # Independent language oracle: S -> a S b | epsilon accepts a^n b^n.
    grammar = '2\nS->aSb\nS->#\n'
    for length in range(6):
        for symbols in itertools.product('ab', repeat=length):
            word = ''.join(symbols)
            accepted = any(word == 'a' * n + 'b' * n for n in range(3))
            output = run('q9', grammar + word + '\n')[0]
            check(('Input string is accepted.' in output) == accepted,
                  'Q9 a^n b^n language: ' + repr(word))
    output = run('q9', grammar + 'aabb$\n')[0]
    check('Input string is accepted.' in output, 'Q9 optional final dollar')

    # Acceptance must consume the whole word, not stop at an interior '$'.
    for word in ['a$garbage', 'a$$', 'a' + ' ' * 252 + 'x']:
        output = run('q9', '1\nS->a\n' + word + '\n')[0]
        check('Input string is accepted.' not in output, 'Q9 whole input: ' + repr(word))
    # 1 initial + 42 a-prefix + 55 b-prefix + S-goto + d = 100 states.
    hundred = '3\nS->' + 'a' * 42 + '\nS->' + 'b' * 54 + 'S\nS->d\n'
    output = run('q8', hundred)[0]
    check(len(re.findall(r'^I\d+:', output, re.M)) == 100, 'Q8 full state capacity')
    output = run('q9', hundred + 'd\n')[0]
    check('Input string is accepted.' in output, 'Q9 full state capacity')

    for name in ['calc.l', 'calc.y']:
        shutil.copy(ROOT.parent / 'q10_bison_calculator' / name, build)
    subprocess.run(['bison', '-d', 'calc.y'], cwd=build, check=True, capture_output=True)
    subprocess.run(['flex', 'calc.l'], cwd=build, check=True, capture_output=True)
    subprocess.run(['gcc', *flags, 'calc.tab.c', 'lex.yy.c', '-o', 'q10'],
                   cwd=build, check=True, capture_output=True)
    output, errors = run('q10', '3+4*2\n(3+4)*2\na=25\nb=a-5\nb/0\nb/4\n-2*3\n')
    check(re.findall(r'Result = (-?\d+)', output) == ['11', '14', '0', '5', '-6'],
          'Q10 precedence and integer arithmetic')
    check('Assigned: a = 25' in output and 'Assigned: b = 20' in output, 'Q10 variables')
    check('Division by zero' in errors, 'Q10 zero divisor')
    output, errors = run('q10', '2+\n3+4\n')
    check('syntax error' in errors and 'Result = 7' in output, 'Q10 line recovery')
    output, errors = run('q10', '2@+3\n4+5\n')
    check('Result = 5' not in output and 'Result = 9' in output and errors,
          'Q10 invalid characters cannot silently disappear')

    for q in range(6, 11):
        sample = ROOT / 'samples' / f'q{q}'
        output, errors = run(f'q{q}', sample.with_suffix('.in').read_text())
        check(output == sample.with_suffix('.out').read_text(), f'Q{q} saved output')
        error_file = sample.with_suffix('.err')
        check(errors == (error_file.read_text() if error_file.exists() else ''),
              f'Q{q} saved errors')

print(f'PASS: {checks} checks; Q6-Q10 compiled and tested in a temporary directory.')
