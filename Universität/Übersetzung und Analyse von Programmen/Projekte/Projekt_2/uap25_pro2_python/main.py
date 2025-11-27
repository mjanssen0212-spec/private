#Matthias Janßen
#1871808

# This is a sample Python script for testing your TRIPLA parser.

# In PyCharm press Umschalt+F10 to execute it.

import os
import argparse
import html

from triplalex import lexer
import triplayacc

def _escape_label(s: str) -> str:
    return html.escape(s).replace('\n', '\\n').replace('"', '\\"')

def export_dot_from_node(root, filename: str):
    """
    Export simple Node AST (Node.type, Node.children, Node.leaf) to DOT file.
    """
    lines = ['digraph AST {', '  node [shape=box, fontname="Arial"];']
    idmap = {}
    counter = [0]

    def newid():
        i = counter[0]; counter[0] += 1
        return f'n{i}'

    def emit(node):
        nid = newid()
        idmap[id(node)] = nid
        # build label: type + optional leaf
        label = getattr(node, 'type', repr(node))
        if hasattr(node, 'leaf') and node.leaf is not None:
            lf = node.leaf
            if isinstance(lf, (list, tuple)):
                lf_s = ', '.join(map(repr, lf))
            else:
                lf_s = repr(lf)
            label = f"{label}\\n{lf_s}"
        label = _escape_label(str(label))
        lines.append(f'  {nid} [label="{label}"];')
        # children
        for c in getattr(node, 'children', []) or []:
            if c is None:
                continue
            cid = emit(c)
            lines.append(f'  {nid} -> {cid};')
        return nid

    emit(root)
    lines.append('}')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

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

    if hasattr(triplayacc, 'parse_and_export_dot'):
        try:
            triplayacc.parse_and_export_dot(src, out_path)
            print(f'AST exported to: {out_path}')
            return
        except Exception as e:
            print('parse_and_export_dot failed:', e)
            return

    try:
        ast_root = triplayacc.parser.parse(src, lexer=lexer)
    except Exception as e:
        print('Parse failed:', e)
        return

    if ast_root is None:
        print('Parsing produced no AST (syntax error or empty input).')
        return

    export_dot_from_node(ast_root, out_path)
    print(f'AST exported to: {out_path}')

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

if __name__ == '__main__':
    src='triplaprograms/condition.tripla'
    main(src)
    test_parser(src)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
