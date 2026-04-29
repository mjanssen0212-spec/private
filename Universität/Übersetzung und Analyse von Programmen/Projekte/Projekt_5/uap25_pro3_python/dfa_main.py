# Matthias Janßen
# 1871808
# Datenflussanalyse für TRIPLA (Hausaufgabe)

import os
import sys
import argparse

# CFG Support aktivieren
sys.modules['compiler'] = __import__('graphbuilder')

from triplalex import lexer
import triplayacc
import graphbuilder

# --- Hilfsfunktionen für die Knoten-Identifikation ---

def get_node_info(node):
    """Gibt den Typnamen und ob es ein Spezialknoten ist zurück."""
    name = f'TUPLE_{node[0]}' if isinstance(node, tuple) else node.__class__.__name__
    is_spec = lambda label: isinstance(node, tuple) and len(node) == 2 and node[0] == label
    return name, is_spec

def get_params(node):
    """Extrahiert Parameternamen aus START/END Knoten."""
    _, is_spec = get_node_info(node)
    if (is_spec('START') or is_spec('END')) and hasattr(node[1], 'params'):
        return {p.name if hasattr(p, 'name') else str(p) for p in node[1].params}
    return set()

def format_node(node):
    """Lesbare Darstellung eines Knotens."""
    if isinstance(node, tuple) and len(node) == 2:
        return f'{node[0]} {node[1].fname}' if hasattr(node[1], 'fname') else str(node)
    name, _ = get_node_info(node)
    if name == 'VAR': return node.name
    if name == 'ASSIGN': return f"{node.variable.name if hasattr(node.variable, 'name') else node.variable}="
    return str(node)

# --- CFG- & Datenfluss-Infrastruktur ---

def build_cfg(input_path):
    """Parst TRIPLA und liefert den CFG (mit Caching)."""
    if not hasattr(build_cfg, 'cache') or getattr(build_cfg, 'path', None) != input_path:
        with open(input_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Sicherstellen, dass der Parser die graphbuilder-Knoten verwendet
        import importlib
        importlib.reload(triplayacc)
        
        ast = triplayacc.parser.parse(source, lexer=lexer)
        if not ast: return None
        build_cfg.cache = ast.cfg({})
        build_cfg.path = input_path
    return build_cfg.cache

def solve_backward(nodes, succ, transfer_func):
    """Generischer Fixpunkt-Algorithmus für Rückwärtsanalysen."""
    ins, outs = {n: set() for n in nodes}, {n: set() for n in nodes}
    changed = True
    while changed:
        changed = False
        for n in sorted(nodes, key=str):
            old_in, old_out = ins[n].copy(), outs[n].copy()
            outs[n] = set().union(*(ins[s] for s in succ[n])) if succ[n] else set()
            ins[n] = transfer_func(n, outs[n])
            if ins[n] != old_in or outs[n] != old_out: changed = True
    return ins, outs

# --- Analysen ---

def live_variables(input_path, quiet=False):
    """Berechnet lebendige Variablen (Rückwärtsanalyse)."""
    cfg = build_cfg(input_path)
    if not cfg: return None
    vertices, edges, in_node, out_node = cfg
    nodes = set(vertices) | {in_node, out_node} | {s for s, _, d in edges} | {d for s, _, d in edges}
    succ = {n: {d for s, _, d in edges if s == n} for n in nodes}
    
    def transfer(n, out_set):
        name, is_spec = get_node_info(n)
        use = {n.name} if name == 'VAR' else set()
        defn = {n.variable.name if hasattr(n.variable, 'name') else n.variable} if name == 'ASSIGN' else (get_params(n) if is_spec('START') or is_spec('END') else set())
        return use | (out_set - defn)

    ins, outs = solve_backward(nodes, succ, transfer)
    if not quiet:
        print("\nLive-Variables-Analyse\n" + "="*22)
        for n in sorted(nodes, key=str):
            print(f"Knoten: {format_node(n)}\n  IN : {sorted(ins[n])}\n  OUT: {sorted(outs[n])}\n")
    return ins, outs

def reached_uses(input_path, quiet=False):
    """Interprozedurale Reached-Uses-Analyse (Vorwärts, mit Live-Filter)."""
    l_res = live_variables(input_path, quiet=True)
    if not l_res: return None
    l_ins, l_outs = l_res
    
    cfg = build_cfg(input_path)
    vertices, edges, in_node, out_node = cfg
    nodes = set(vertices) | {in_node, out_node} | {s for s, _, d in edges} | {d for s, _, d in edges}
    succ = {n: {d for s, _, d in edges if s == n} for n in nodes}
    pred = {n: {s for s, _, d in edges if d == n} for n in nodes}

    gk = {}
    for n in nodes:
        name, is_spec = get_node_info(n)
        gen = {(n, n.name)} if name == 'VAR' else ({(n, p) for p in get_params(n)} if is_spec('START') else set())
        kill = {n.variable.name if hasattr(n.variable, 'name') else n.variable} if name == 'ASSIGN' else (get_params(n) if is_spec('START') or is_spec('END') else set())
        gk[n] = (gen, kill)

    ins, outs = {n: set() for n in nodes}, {n: set() for n in nodes}
    changed = True
    while changed:
        changed = False
        for n in sorted(nodes, key=str):
            old_in, old_out = ins[n].copy(), outs[n].copy()
            ins[n] = set().union(*(outs[p] for p in pred[n])) if pred[n] else set()
            
            _, is_spec = get_node_info(n)
            gen, kill = gk[n]
            
            if is_spec('CALL'):
                w = n[1]
                start_n = next((s for s in succ[n] if get_node_info(s)[1]('START')), None)
                ret_n = next((s for s in succ[n] if get_node_info(s)[1]('RET')), None)
                end_n = next((p for p in pred[ret_n] if get_node_info(p)[1]('END')), None) if ret_n else None
                if start_n and ret_n and end_n:
                    delta = {(p, v) for (p, v) in (outs[end_n] - outs[start_n]) if v not in gk[start_n][1]}
                    outs[n] = (ins[n] | ins[start_n]) - delta
                else: outs[n] = {(p, v) for (p, v) in ins[n] if v not in kill} | gen
            else: outs[n] = {(p, v) for (p, v) in ins[n] if v not in kill} | gen
            
            # Live-Variablen Filter für Präzision
            ins[n] = {(p, v) for (p, v) in ins[n] if v in l_ins[n]}
            outs[n] = {(p, v) for (p, v) in outs[n] if v in l_outs[n]}
            if ins[n] != old_in or outs[n] != old_out: changed = True

    if not quiet:
        print("\nReached-Uses-Analyse\n" + "="*20)
        for n in sorted(nodes, key=str):
            f_in = f"{{{', '.join(f'({format_node(p)}, {v})' for p,v in sorted(ins[n], key=lambda x: str(x[0])) )}}}"
            f_out = f"{{{', '.join(f'({format_node(p)}, {v})' for p,v in sorted(outs[n], key=lambda x: str(x[0])) )}}}"
            print(f"Knoten: {format_node(n)}\n  IN : {f_in}\n  OUT: {f_out}\n")
    return ins, outs

def get_reaching_definitions(input_path):
    """Gibt ein Set von (Definition, Variable) Paaren zurück, die mindestens eine Verwendung erreichen."""
    r_ins, _ = reached_uses(input_path, quiet=True)
    active_defs = set()
    for n, reaching in r_ins.items():
        name, _ = get_node_info(n)
        if name == 'VAR':
            for def_node, var_name in reaching:
                if var_name == n.name:
                    active_defs.add((def_node, var_name))
    return active_defs

def export_dfg(input_path):
    """Exportiert den CFG mit zusätzlichen Datenflusskanten."""
    cfg = build_cfg(input_path)
    if not cfg: return
    
    r_res = reached_uses(input_path, quiet=True)
    if not r_res: return
    r_ins, _ = r_res
    
    df_edges = set()
    for n, reaching in r_ins.items():
        name, _ = get_node_info(n)
        # Wenn der Knoten eine Verwendung ist (VAR), füge Kanten von den Definitionen hinzu
        if name == 'VAR':
            for def_node, var_name in reaching:
                if var_name == n.name:
                    df_edges.add((def_node, n, var_name))
    
    base = os.path.splitext(os.path.basename(input_path))[0]
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cfg_out')
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    cfg_path = os.path.join(out_dir, f'{base}.dfg.dot')
    
    vertices, edges, in_node, out_node = cfg
    graphbuilder.export_cfg_to_dot(vertices, edges, in_node, out_node, cfg_path, df_edges=df_edges)
    print(f"✓ DFG exportiert nach: {cfg_path}")

def main():
    parser = argparse.ArgumentParser(description='TRIPLA DFA Tool')
    parser.add_argument('input', help='TRIPLA Datei')
    parser.add_argument('--mode', choices=['live', 'reached', 'dfg', 'cfg'], default='live', help='Modus')
    args = parser.parse_args()
    if args.mode == 'live': live_variables(args.input)
    elif args.mode == 'reached': reached_uses(args.input)
    elif args.mode == 'dfg': export_dfg(args.input)
    elif args.mode == 'cfg': 
        cfg = build_cfg(args.input)
        if cfg:
            vertices, edges, in_node, out_node = cfg
            base = os.path.splitext(os.path.basename(args.input))[0]
            out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cfg_out')
            if not os.path.exists(out_dir): os.makedirs(out_dir)
            cfg_path = os.path.join(out_dir, f'{base}.cfg.dot')
            graphbuilder.export_cfg_to_dot(vertices, edges, in_node, out_node, cfg_path)
            print(f"✓ CFG exportiert nach: {cfg_path}")

if __name__ == '__main__':
    main()
