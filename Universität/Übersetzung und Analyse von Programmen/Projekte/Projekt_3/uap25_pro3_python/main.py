#Matthias Janßen
#1871808

# This is a sample Python script for testing your TRIPLA parser.

# In PyCharm press Umschalt+F10 to execute it.

import os
import argparse

from triplalex import lexer
import triplayacc

def run(input_path: str, dot_out: str | None = None):

    proj_dir = os.path.dirname(__file__)

    dot_dir = os.path.join(proj_dir, 'dotFiles')
    os.makedirs(dot_dir, exist_ok=True)

    if dot_out:
        if not os.path.isabs(dot_out):
            out_path = os.path.join(dot_dir, dot_out)
        else:
            out_path = dot_out
    else:
        base = os.path.splitext(os.path.basename(input_path))[0]
        out_path = os.path.join(dot_dir, base + '.ast.dot')

    with open(input_path, 'r', encoding='utf-8') as f:
        src = f.read()

    lexer.input(src)

    try:
        ast_root = triplayacc.parser.parse(src, lexer=lexer)
    except Exception as e:
        print('Parse failed:', e)
        return

    if ast_root is None:
        print('Parsing produced no AST (syntax error or empty input).')
        return

    # Export using the syntax node's built-in DOT export method
    try:
        ast_root.export_dot(out_path)
        print(f'AST exported to: {out_path}')
    except Exception as e:
        print(f'Failed to export DOT: {e}')
        return

def main(src):
    ap = argparse.ArgumentParser()
    ap.add_argument('input', nargs='?', default=src)
    ap.add_argument('--out', '-o')
    args = ap.parse_args()

    run(src, args.out)

def test_parser(name):
    source = "\n".join(open(name).readlines())
    ast = triplayacc.parser.parse(source)#, debug=True)
    print("AST:")
    print(ast)
    if ast is not None:
        # Also export the AST to DOT format
        proj_dir = os.path.dirname(__file__)
        dot_dir = os.path.join(proj_dir, 'dotFiles')
        os.makedirs(dot_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(name))[0]
        out_path = os.path.join(dot_dir, base + '.ast.dot')
        try:
            ast.export_dot(out_path)
            print(f'AST exported to: {out_path}')
        except Exception as e:
            print(f'Failed to export DOT: {e}')

if __name__ == '__main__':
    src='triplaprograms/condition.tripla'
    main(src)
    test_parser(src)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
