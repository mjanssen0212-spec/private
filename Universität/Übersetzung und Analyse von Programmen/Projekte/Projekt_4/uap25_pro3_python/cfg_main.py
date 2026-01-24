# Matthias Janßen
# 1871808
# Control Flow Graph Generator for TRIPLA

import os
import sys
import argparse

# Switch compiler module to graphbuilder for CFG support
sys.modules['compiler'] = __import__('graphbuilder')

from triplalex import lexer
import triplayacc
import graphbuilder

def generate_cfg(input_path: str, output_path: str = None):
    """
    Generate Control Flow Graph from TRIPLA source file.
    
    Args:
        input_path: Path to TRIPLA source file
        output_path: Optional output path for DOT file
    """
    
    proj_dir = os.path.dirname(__file__)
    cfg_dir = os.path.join(proj_dir, 'cfg_examples')
    os.makedirs(cfg_dir, exist_ok=True)
    
    # Determine output path
    base = os.path.splitext(os.path.basename(input_path))[0]
    if output_path:
        if not os.path.isabs(output_path):
            output_path = os.path.join(cfg_dir, output_path)
    else:
        output_path = os.path.join(cfg_dir, f'{base}.cfg.dot')
    
    # Read source file
    print(f'Parsing: {input_path}')
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    print('Source:')
    print(source)
    print()
    
    # Parse source
    lexer.input(source)
    try:
        ast_root = triplayacc.parser.parse(source, lexer=lexer)
    except Exception as e:
        print(f'Parse failed: {e}')
        return False
    
    if ast_root is None:
        print('Parsing produced no AST.')
        return False
    
    print(f'AST Type: {ast_root.__class__.__name__}')
    print(f'AST Module: {ast_root.__class__.__module__}')
    print()
    
    # Generate CFG
    print('Building CFG...')
    try:
        vertices, edges, in_node, out_node = ast_root.cfg({})
        print(f'Vertices: {len(vertices)}')
        print(f'Edges: {len(edges)}')
        print(f'In: {in_node.__class__.__name__}')
        print(f'Out: {out_node.__class__.__name__}')
        print()
    except Exception as e:
        print(f'CFG generation failed: {e}')
        import traceback
        traceback.print_exc()
        return False
    
    # Export CFG to DOT
    try:
        graphbuilder.export_cfg_to_dot(vertices, edges, in_node, out_node, output_path)
        print(f'CFG exported to: {output_path}')
        print()
        print('To visualize, run:')
        png_path = output_path.replace('.dot', '.png')
        print(f'  dot -Tpng {output_path} -o {png_path}')
        return True
    except Exception as e:
        print(f'Failed to export CFG: {e}')
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Generate Control Flow Graph for TRIPLA programs'
    )
    parser.add_argument('input', help='Input TRIPLA source file')
    parser.add_argument('--out', '-o', help='Output DOT file path (optional)')
    args = parser.parse_args()
    
    success = generate_cfg(args.input, args.out)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
