#!/usr/bin/env python
"""Test-Skript zum Exportieren von Control Flow Graphs im DOT-Format."""

import os
import sys

# Graphbuilder importieren (enthält die CFG-Implementierungen)
import graphbuilder as gb
from triplalex import lexer
import triplayacc


def convert_to_graphbuilder(ast_node):
    """
    Konvertiert einen compiler AST-Knoten zu einem graphbuilder AST-Knoten.
    Dies ist nötig, da die cfg() Methoden in graphbuilder definiert sind.
    """
    # Einfache Lösung: Parse nochmal mit graphbuilder als Modul
    # Da triplayacc die Klassen direkt verwendet, müssen wir den Parser patchen
    return ast_node


def test_cfg_export(input_path, output_path=None):
    """
    Parst ein TRIPLA-Programm und exportiert den CFG.
    
    Args:
        input_path: Pfad zur TRIPLA-Quelldatei
        output_path: Optional - Pfad zur Ausgabe-DOT-Datei
    """
    # Ausgabepfad bestimmen
    if output_path is None:
        proj_dir = os.path.dirname(__file__)
        cfg_dir = os.path.join(proj_dir, 'cfg_examples')
        os.makedirs(cfg_dir, exist_ok=True)
        
        base = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(cfg_dir, base + '.cfg.dot')
    
    # Quelldatei lesen
    with open(input_path, 'r', encoding='utf-8') as f:
        src = f.read()
    
    print(f"Parsing: {input_path}")
    print(f"Source:\n{src}\n")
    
    # Wichtig: triplayacc verwendet compiler-Klassen, aber wir brauchen graphbuilder-Klassen
    # Wir müssen den Parser temporär umkonfigurieren
    import triplayacc
    original_module = sys.modules.get('compiler')
    
    try:
        # Ersetze compiler durch graphbuilder für das Parsing
        sys.modules['compiler'] = gb
        
        # Parser neu laden
        import importlib
        importlib.reload(triplayacc)
        
        # Jetzt parsen
        ast_root = triplayacc.parser.parse(src, lexer=lexer)
        
    finally:
        # Original wiederherstellen
        if original_module:
            sys.modules['compiler'] = original_module
        importlib.reload(triplayacc)
    
    if ast_root is None:
        print('Parsing produced no AST (syntax error or empty input).')
        return
    
    print(f"AST Type: {type(ast_root).__name__}")
    print(f"AST Module: {type(ast_root).__module__}\n")
    
    # CFG erstellen
    try:
        print("Building CFG...")
        vertices, edges, in_node, out_node = ast_root.cfg({})
        
        print(f"Vertices: {len(vertices)}")
        print(f"Edges: {len(edges)}")
        print(f"In: {type(in_node).__name__ if hasattr(in_node, '__class__') else in_node}")
        print(f"Out: {type(out_node).__name__ if hasattr(out_node, '__class__') else out_node}\n")
        
        # CFG exportieren
        gb.export_cfg_to_dot(vertices, edges, in_node, out_node, output_path)
        
        print(f"\nTo visualize, run:")
        print(f"  dot -Tpng {output_path} -o {output_path.replace('.dot', '.png')}")
        
    except Exception as e:
        print(f'CFG generation failed: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        test_cfg_export(input_file, output_file)
    else:
        # Teste mit dem Beispiel aus der Aufgabe
        print("=" * 70)
        print("Testing with argsParamsExample.tripla")
        print("=" * 70 + "\n")
        test_cfg_export('triplaprograms/argsParamsExample.tripla')
        
        print("\n" + "=" * 70)
        print("Testing with simpleExpressionSequence.tripla")
        print("=" * 70 + "\n")
        test_cfg_export('cfg_examples/simpleExpressionSequence.tripla')
        
        print("\n" + "=" * 70)
        print("Testing with complex.tripla")
        print("=" * 70 + "\n")
        test_cfg_export('cfg_examples/complex.tripla')
