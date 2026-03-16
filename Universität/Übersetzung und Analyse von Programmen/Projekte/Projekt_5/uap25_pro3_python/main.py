# Matthias Janßen
# 1871808

import os
import sys
import argparse

from triplalex import lexer
import triplayacc
import compiler
import dfa_main

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

def generate_tram(ast_root, input_path, tram_dir, optimize=False):
    """Generate TRAM code."""
    base = os.path.splitext(os.path.basename(input_path))[0]
    tram_path = os.path.join(tram_dir, f'{base}.tram')
    
    if optimize:
        print("  Optimierung läuft...")
        defs = dfa_main.get_reaching_definitions(input_path)
        compiler.set_active_definitions(defs)
    else:
        compiler.set_active_definitions(None)
    
    tram_code = ast_root.code({}, 0)
    compiler.assemble(tram_code, tram_path)
    print(f'✓ TRAM code exported to: {tram_path}')
    return True

def generate_cfg(ast_root, input_path, cfg_dir):
    """Generate Control Flow Graph."""
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
    
    print("Was soll generiert werden?")
    print("  1. AST (Abstract Syntax Tree)")
    print("  2. TRAM Code")
    print("  3. CFG (Control Flow Graph)")
    print("  4. Live Variables")
    print("  5. Reached Uses")
    print("  6. Alles (AST + TRAM + CFG + Live Variables + Reached Uses)")
    print()
    
    choice = input("Auswahl [1-6]: ").strip()
    
    generate_ast_flag = choice in ('1', '6')
    generate_tram_flag = choice in ('2', '6')
    generate_cfg_flag = choice in ('3', '6')
    generate_live_flag = choice in ('4', '6')
    generate_reached_flag = choice in ('5', '6')
    
    optimize_flag = False
    if generate_tram_flag:
        opt_choice = input("Optimierung aktivieren? (y/n): ").strip().lower()
        optimize_flag = opt_choice == 'y'
    
    if not any([generate_ast_flag, generate_tram_flag, generate_cfg_flag, generate_live_flag, generate_reached_flag]):
        print("✗ Ungültige Auswahl")
        return
    
    print()
    print("Verarbeitung läuft...")
    print()
    
    process_file(
        input_path,
        generate_ast_flag,
        generate_tram_flag,
        generate_cfg_flag,
        generate_live_flag,
        generate_reached_flag,
        optimize_flag
    )

def process_file(input_path, gen_ast=True, gen_tram=True, gen_cfg=True, gen_live=False, gen_reached=False, optimize=False):
    """Process TRIPLA file and generate requested outputs."""
    
    proj_dir = os.path.dirname(__file__) or '.'
    dot_dir = os.path.join(proj_dir, 'dotFiles')
    tram_dir = os.path.join(proj_dir, 'tram_out')
    cfg_dir = os.path.join(proj_dir, 'cfg_out')
    
    os.makedirs(dot_dir, exist_ok=True)
    os.makedirs(tram_dir, exist_ok=True)
    os.makedirs(cfg_dir, exist_ok=True)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
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
                generate_tram(ast_root, input_path, tram_dir, optimize)
            except Exception as e:
                print(f'✗ Failed to generate TRAM: {e}')
                import traceback
                traceback.print_exc()
    
    if gen_cfg:
        # Wir müssen sicherstellen, dass wir eine AST-Version haben, die cfg() unterstützt.
        # Da dfa_main.build_cfg bereits graphbuilder nutzt, können wir es direkt verwenden.
        cfg = dfa_main.build_cfg(input_path)
        if cfg:
            vertices, edges, in_node, out_node = cfg
            base = os.path.splitext(os.path.basename(input_path))[0]
            cfg_path = os.path.join(cfg_dir, f'{base}.cfg.dot')
            import graphbuilder
            graphbuilder.export_cfg_to_dot(vertices, edges, in_node, out_node, cfg_path)
            print(f'✓ CFG exported to: {cfg_path}')
        else:
            print('✗ CFG parsing produced no AST.')

    if gen_live:
        dfa_main.live_variables(input_path)

    if gen_reached:
        dfa_main.reached_uses(input_path)
    
    # Immer auch DFG generieren wenn CFG oder reached angefordert wurde, 
    # damit die farbigen Kanten sichtbar sind.
    if gen_cfg or gen_reached:
        dfa_main.export_dfg(input_path)
    
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
  python main.py --file prog.tripla --live         # Nur Live Variables
  python main.py --file prog.tripla --reached      # Nur Reached Uses
        """
    )
    parser.add_argument('--file', '-f', help='Input TRIPLA source file')
    parser.add_argument('--ast', action='store_true', help='Generate AST')
    parser.add_argument('--tram', action='store_true', help='Generate TRAM code')
    parser.add_argument('--cfg', action='store_true', help='Generate CFG')
    parser.add_argument('--live', action='store_true', help='Run live-variables analysis')
    parser.add_argument('--reached', action='store_true', help='Run reached-uses analysis')
    parser.add_argument('--optimize', action='store_true', help='Enable DFA-based optimization for TRAM code')
    parser.add_argument('--all', '-a', action='store_true', help='Generate all outputs')
    
    args = parser.parse_args()
    
    if not args.file:
        interactive_mode()
    else:
        if args.all:
            gen_ast = gen_tram = gen_cfg = gen_live = gen_reached = True
        else:
            gen_ast = args.ast
            gen_tram = args.tram
            gen_cfg = args.cfg
            gen_live = args.live
            gen_reached = args.reached
            
            if not any([gen_ast, gen_tram, gen_cfg, gen_live, gen_reached]):
                gen_ast = gen_tram = gen_cfg = True
        
        process_file(args.file, gen_ast, gen_tram, gen_cfg, gen_live, gen_reached, args.optimize)

if __name__ == '__main__':
    main()
