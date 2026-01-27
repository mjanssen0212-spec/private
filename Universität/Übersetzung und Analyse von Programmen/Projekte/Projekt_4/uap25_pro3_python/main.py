# Matthias Janßen
# 1871808

import os
import sys
import argparse

from triplalex import lexer
import triplayacc
import compiler

def generate_ast(ast_root, input_path, dot_dir):
    """Generate AST DOT file."""
    base = os.path.splitext(os.path.basename(input_path))[0]
    ast_path = os.path.join(dot_dir, f'{base}.ast.dot')
    
    try:
        ast_root.export_dot(ast_path)
        print(f'✓ AST exported to: {ast_path}')
        return True
    except Exception as e:
        print(f'✗ Failed to export AST: {e}')
        return False

def generate_tram(ast_root, input_path, tram_dir):
    """Generate TRAM code."""
    base = os.path.splitext(os.path.basename(input_path))[0]
    tram_path = os.path.join(tram_dir, f'{base}.tram')
    
    tram_code = ast_root.code({}, 0)
    compiler.assemble(tram_code, tram_path)
    print(f'✓ TRAM code exported to: {tram_path}')
    return True

def generate_cfg(ast_root, input_path, cfg_dir):
    """Generate Control Flow Graph."""
    # Import graphbuilder for CFG support
    import graphbuilder
    
    base = os.path.splitext(os.path.basename(input_path))[0]
    cfg_path = os.path.join(cfg_dir, f'{base}.cfg.dot')
    
    try:
        vertices, edges, in_node, out_node = ast_root.cfg({})
        graphbuilder.export_cfg_to_dot(vertices, edges, in_node, out_node, cfg_path)
        print(f'✓ CFG exported to: {cfg_path}')
        return True
    except Exception as e:
        print(f'✗ Failed to generate CFG: {e}')
        return False

def interactive_mode():
    """Interactive mode: ask user what to generate."""
    print("TRIPLA Compiler und CFG Generator")
    print("=" * 50)
    print()
    
    # Get input file
    print("Verfügbare TRIPLA Programme:")
    tripla_dir = 'triplaprograms'
    if os.path.exists(tripla_dir):
        files = [f for f in os.listdir(tripla_dir) if f.endswith('.tripla')]
        for i, f in enumerate(files, 1):
            print(f"  {i}. {f}")
        print()
        
        choice = input("Dateinummer eingeben (oder vollständiger Pfad): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            input_path = os.path.join(tripla_dir, files[int(choice) - 1])
        else:
            input_path = choice
    else:
        input_path = input("Pfad zur TRIPLA Datei: ").strip()
    
    if not os.path.exists(input_path):
        print(f"✗ Datei nicht gefunden: {input_path}")
        return
    
    print(f"\nVerarbeite: {input_path}")
    print()
    
    # Ask what to generate
    print("Was soll generiert werden?")
    print("  1. AST (Abstract Syntax Tree)")
    print("  2. TRAM Code")
    print("  3. CFG (Control Flow Graph)")
    print("  4. Alles (AST + TRAM + CFG)")
    print()
    
    choice = input("Auswahl [1-4]: ").strip()
    
    generate_ast_flag = choice in ('1', '4')
    generate_tram_flag = choice in ('2', '4')
    generate_cfg_flag = choice in ('3', '4')
    
    if not any([generate_ast_flag, generate_tram_flag, generate_cfg_flag]):
        print("✗ Ungültige Auswahl")
        return
    
    print()
    print("Verarbeitung läuft...")
    print()
    
    # Parse source
    process_file(input_path, generate_ast_flag, generate_tram_flag, generate_cfg_flag)

def process_file(input_path, gen_ast=True, gen_tram=True, gen_cfg=True):
    """Process TRIPLA file and generate requested outputs."""
    
    proj_dir = os.path.dirname(__file__) or '.'
    dot_dir = os.path.join(proj_dir, 'dotFiles')
    tram_dir = os.path.join(proj_dir, 'tram_out')
    cfg_dir = os.path.join(proj_dir, 'cfg_out')
    
    os.makedirs(dot_dir, exist_ok=True)
    os.makedirs(tram_dir, exist_ok=True)
    os.makedirs(cfg_dir, exist_ok=True)
    
    # Read source file
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Parse for AST and TRAM (uses compiler module)
    if gen_ast or gen_tram:
        lexer.input(source)
        try:
            ast_root = triplayacc.parser.parse(source, lexer=lexer)
        except Exception as e:
            print(f'✗ Parse failed: {e}')
            return
        
        if ast_root is None:
            print('✗ Parsing produced no AST.')
            return
        
        if gen_ast:
            generate_ast(ast_root, input_path, dot_dir)
        
        if gen_tram:
            try:
                generate_tram(ast_root, input_path, tram_dir)
            except Exception as e:
                print(f'✗ Failed to generate TRAM: {e}')
                import traceback
                traceback.print_exc()
    
    # Parse for CFG (uses graphbuilder module)
    if gen_cfg:
        # Switch compiler module to graphbuilder for CFG support
        original_compiler = sys.modules.get('compiler')
        sys.modules['compiler'] = __import__('graphbuilder')
        
        # Re-import to use graphbuilder classes
        import importlib
        importlib.reload(triplayacc)
        
        lexer.input(source)
        try:
            ast_root_cfg = triplayacc.parser.parse(source, lexer=lexer)
        except Exception as e:
            print(f'✗ CFG parse failed: {e}')
            # Restore original compiler module
            if original_compiler:
                sys.modules['compiler'] = original_compiler
            return
        
        if ast_root_cfg is None:
            print('✗ CFG parsing produced no AST.')
            # Restore original compiler module
            if original_compiler:
                sys.modules['compiler'] = original_compiler
            return
        
        generate_cfg(ast_root_cfg, input_path, cfg_dir)
        
        # Restore original compiler module
        if original_compiler:
            sys.modules['compiler'] = original_compiler
            importlib.reload(triplayacc)
    
    print()
    print("✓ Verarbeitung abgeschlossen!")

def main():
    parser = argparse.ArgumentParser(
        description='TRIPLA Compiler und CFG Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python main.py                                    # Interaktiver Modus
  python main.py --file prog.tripla --all          # Alles generieren
  python main.py --file prog.tripla --ast --tram   # Nur AST und TRAM
  python main.py --file prog.tripla --cfg          # Nur CFG
        """
    )
    parser.add_argument('--file', '-f', help='Input TRIPLA source file')
    parser.add_argument('--ast', action='store_true', help='Generate AST')
    parser.add_argument('--tram', action='store_true', help='Generate TRAM code')
    parser.add_argument('--cfg', action='store_true', help='Generate CFG')
    parser.add_argument('--all', '-a', action='store_true', help='Generate all outputs')
    
    args = parser.parse_args()
    
    # Interactive mode if no arguments
    if not args.file:
        interactive_mode()
    else:
        # Command line mode
        if args.all:
            gen_ast = gen_tram = gen_cfg = True
        else:
            gen_ast = args.ast
            gen_tram = args.tram
            gen_cfg = args.cfg
            
            # If no flags specified, generate all
            if not any([gen_ast, gen_tram, gen_cfg]):
                gen_ast = gen_tram = gen_cfg = True
        
        process_file(args.file, gen_ast, gen_tram, gen_cfg)

if __name__ == '__main__':
    main()
