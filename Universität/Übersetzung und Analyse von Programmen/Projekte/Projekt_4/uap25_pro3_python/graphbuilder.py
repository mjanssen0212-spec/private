import compiler

class CONST(compiler.CONST):
    def cfg(self, psi):
        """
        Control Flow Graph für Konstanten.
        
        Gemäß der Regel: wenn w = const dann
            V = {w}
            E = ∅
            in = w
            out = w
        
        Args:
            psi: Kontext-Parameter für die CFG-Konstruktion
            
        Returns:
            Tupel (V, E, in, out) mit:
            - V: Menge der Knoten {w}
            - E: Menge der Kanten (leer)
            - in: Eingangsknoten w
            - out: Ausgangsknoten w
        """
        w = self
        vertices = {w}
        edges = set()
        in_node = w
        out_node = w
        
        return vertices, edges, in_node, out_node

class WHILE(compiler.WHILE):
    def cfg(self, psi):
        """
        Control Flow Graph für WHILE:

        Gemäß der Regel wenn w = while e1 do {e2} dann
        V = V1 + V2 + {diamond, glue}
        E = E1 + E2 {(out1, ε, diamond), (diamond, T, in2), (diamond, F, glue), (out2, ε, in1}
        in = in1
        out = glue

        where V1, E1, in1, out1 = cfg(e1, psi) und V2, E2, in2, out2 = cfg(e2, psi)
            und diamond und glue neue Knoten sind
        """
        w = self
        e1 = self.condition
        e2 = self.body

        vertices_1, edges_1, in_node_1, out_node_1 = e1.cfg(psi)
        vertices_2, edges_2, in_node_2, out_node_2 = e2.cfg(psi)

        diamond = ('diamond', w)
        glue = ('glue', w)

        vertices = vertices_1 | vertices_2 | {diamond, glue}
        edges = (edges_1 | edges_2 |
                 {(out_node_1, '', diamond), (diamond, 'T', in_node_2), (diamond, 'F', glue), (out_node_2, '', in_node_1)})
        in_node = in_node_1
        out_node = glue

        return vertices, edges, in_node, out_node

class LET(compiler.LET):
    def cfg(self, psi):
        """
        Control Flow Graph für LET:

        Gemäß der Regel wenn w = let f1(v1¹,...,vn1¹){e1}...fk(v1ᵏ,...,vnkᵏ){ek} in e dann
        V = V' ∪ ⋃Vi
        E = E' ∪ ⋃Ei
        in = in'
        out = out'

        where ψ' = ψ[(in1,out1)/f1]···[(ink, outk)/fk]
        mit ini = (START, fi(v1ⁱ,...,vniⁱ)), outi = (END, fi(v1ⁱ,...,vniⁱ)),
        und (V', E', in', out') = cfg(e, ψ')
        und (Vi, Ei, ini, outi) = cfg(fi(v1ⁱ,...,viⁱ){ei}, ψ')

        Returns:
            Tupel (V, E, in, out) mit:
            - V: Menge der Knoten
            - E: Menge der Kanten
            - in: Eingangsknoten
            - out: Ausgangsknoten
        """
        w = self
        e = w.body
        decls = w.declarations

        psi_1 = psi.copy() if isinstance(psi, dict) else {}
        
        for decl in decls:
            in_i = ('START', decl)
            out_i = ('END', decl)
            psi_1[decl.fname] = (in_i, out_i)
        
        vertices_1, edges_1, in_node_1, out_node_1 = e.cfg(psi_1)
        
        vertices = vertices_1
        edges = edges_1
        
        for decl in decls:
            vertices_i, edges_i, in_node_i, out_node_i = decl.cfg(psi_1)
            vertices = vertices | vertices_i
            edges = edges | edges_i
        
        in_node = in_node_1
        out_node = out_node_1

        return vertices, edges, in_node, out_node

class DECL(compiler.DECL):
    def cfg(self, psi):
        """
        Control Flow Graph für DECL:

        Gemäß der Regel: Wenn w = f(...){e} dann
        V = V' ∪ {in_f, out_f}
        E = E' ∪ {(in_f, ε, in'), (out', ε, out_f)}
        in = in_f
        out = out_f

        where V', E', in', out' = cfg(e, ψ) und (in_f, out_f) = ψ(f)

        Returns:
            Tupel (V, E, in, out) mit:
            - V: Menge der Knoten
            - E: Menge der Kanten
            - in: Eingangsknoten
            - out: Ausgangsknoten
        """

        w = self
        e = w.body
        f = w.fname

        vertices_1, edges_1, in_node_1, out_node_1 = e.cfg(psi)

        in_node_f, out_node_f = psi[f]

        vertices = vertices_1 | {in_node_f, out_node_f}
        edges = edges_1 | {(in_node_f, '', in_node_1), (out_node_1, '', out_node_f)}
        in_node = in_node_f
        out_node = out_node_f

        return vertices, edges, in_node, out_node


class CALL(compiler.CALL):
    def cfg(self, psi):
        """
        Control Flow Graph für CALL:

        Gemäß der Regel: wenn w = f(e1, ..., ek) dann
        V = {inf, outf, out} ∪ ⋃Vi
        E = {(out1, ε, in2), ..., (outk-1, ε, ink),
             (outk, ε, call), (call, ε, inf), (outf, ε, ret),
             (call, ε, ret)} ∪ ⋃Ei
        in = in1
        out = ret

        where (Vi, Ei, ini, outi) = cfg(ei, ψ),
        (inf, outf) = ψ(f) and call = (CALL, w), ret = (RET, w).

        Returns:
            Tupel (V, E, in, out) mit:
            - V: Menge der Knoten
            - E: Menge der Kanten
            - in: Eingangsknoten
            - out: Ausgangsknoten
        """
        w = self
        f = w.fname
        arguments = w.arguments
        
        in_node_f, out_node_f = psi[f]
        
        call = ('CALL', w)
        ret = ('RET', w)
        
        # Berechne cfg für alle Argumente ei
        vertices = {in_node_f, out_node_f, ret}
        edges = set()

        first_in = None
        prev_out = None
        
        for i, arg in enumerate(arguments):
            vertices_i, edges_i, in_node_i, out_node_i = arg.cfg(psi)

            vertices = vertices | vertices_i
            edges = edges | edges_i

            if i == 0:
                first_in = in_node_i
            else:
                # Verkettung: (out_{i-1}, ε, in_i)
                edges.add((prev_out, '', in_node_i))
            
            prev_out = out_node_i

        if prev_out is not None:
            edges.add((prev_out, '', call))
        
        edges = edges | {(call, '', in_node_f), (out_node_f, '', ret), (call, '', ret)}
            
        in_node = first_in
        out_node = ret
        
        return vertices, edges, in_node, out_node


class VAR(compiler.VAR):
    def cfg(self, psi):
        """
        Control Flow Graph für Variablen.

        Gemäß der Regel: wenn w = var dann
            V = {w}
            E = ∅
            in = w
            out = w

        Args:
            psi: Kontext-Parameter für die CFG-Konstruktion

        Returns:
            Tupel (V, E, in, out) mit:
            - V: Menge der Knoten {w}
            - E: Menge der Kanten (leer)
            - in: Eingangsknoten w
            - out: Ausgangsknoten w
        """
        w = self
        vertices = {w}
        edges = set()
        in_node = w
        out_node = w

        return vertices, edges, in_node, out_node

class BINOP(compiler.BINOP):
    def cfg(self, psi):
        """
        Control Flow Graph für Binop:

        Gemäß der Regel: Wenn w = e1 op e2 dann
        V = V1 + V2 + {w}
        E = E1 + E2 + {(out1, ε, in2), (out2, ε, w)}
        in = in'
        out = w

        where V1, E1, in1, out1 = cfg(e1, psi)
        V2, E2, in2, out2 = cfg(e2, psi)

        Returns:
            Tupel (V, E, in, out) mit:
            - V: Menge der Knoten
            - E: Menge der Kanten
            - in: Eingangsknoten
            - out: Ausgangsknoten
        """

        w = self
        e1 = w.left
        e2 = w.right

        vertices_1, edges_1, in_node_1, out_node_1 = e1.cfg(psi)
        vertices_2, edges_2, in_node_2, out_node_2 = e2.cfg(psi)

        vertices = vertices_1 | vertices_2 | {w}
        edges = edges_1 | edges_2 | {(out_node_1, '', in_node_2), (out_node_2, '', w)}
        in_node = in_node_1
        out_node = w

        return vertices, edges, in_node, out_node

class IF(compiler.IF):
    def cfg(self, psi):
        """
        Control Flow Graph für IF

        Gemäß der Regel: wenn w = if e1 then e2 else e3 dann
        V = V1 + V2 + V3 + {diamond, glue}
        E = E1 + E2 + E3 +
            {(out1, ϵ, diamond), (diamond, T, in2), (diamond, F, in3), (out2, ϵ, glue), (out3, ϵ, glue)}
        in = in1
        out = glue

        where (Vi, Ei, ini, outi) = cfg(ei, psi) und diamond und glue neue Knoten sind
        """
        w = self

        e1 = self.condition
        e2 = self.exp1
        e3 = self.exp2

        vertices_1, edges_1, in_node_1, out_node_1 = e1.cfg(psi)
        vertices_2, edges_2, in_node_2, out_node_2 = e2.cfg(psi)
        vertices_3, edges_3, in_node_3, out_node_3 = e3.cfg(psi)

        diamond = ('diamond', w)
        glue = ('glue', w)

        vertices = vertices_1 | vertices_2 | vertices_3 | {diamond, glue}
        edges = edges_1 | edges_2 | edges_3 | {
            (out_node_1, '', diamond),
            (diamond, 'T', in_node_2),
            (diamond, 'F', in_node_3),
            (out_node_2, '', glue),
            (out_node_3, '', glue)
        }
        in_node = in_node_1
        out_node = glue

        return vertices, edges, in_node, out_node


class SEQ(compiler.SEQ):
    def cfg(self, psi):
        """
        Control Flow Graph für SEQ:

        Gemäß der Regel: Wenn e1 ; e2 dann
        V = V1 + V2
        E = E1 + E2 + {(out1, ε, in2)}
        in = in1
        out = out2

        where V1, E1, in1, out1 = cfg(e1, psi) und V2, E2, in2, out2 = cfg(e2, psi)

        Returns:
            Tupel (V, E, in, out) mit:
            - V: Menge der Knoten
            - E: Menge der Kanten
            - in: Eingangsknoten w
            - out: Ausgangsknoten w
        """
        w = self
        e1 = self.exp1
        e2 = self.exp2

        vertices_1, edges_1, in_node_1, out_node_1 = e1.cfg(psi)
        vertices_2, edges_2, in_node_2, out_node_2 = e2.cfg(psi)

        vertices = vertices_1 | vertices_2
        edges = edges_1 | edges_2 | {(out_node_1, '', in_node_2)}
        in_node = in_node_1
        out_node = out_node_2

        return vertices, edges, in_node, out_node

class ASSIGN(compiler.ASSIGN):
    def cfg(self, psi):
        """
        Control Flow Graph für Zuweisungen

        Gemäß der Regel: Wenn w = id=e dann
        V = V' + {e}
        E = E' + {(out', ε, w)}
        in = in'
        out = w

        where V', E' in' out' = cfg(e, psi)

        Returns:
            Tupel (V, E, in, out) mit:
            - V: Menge der Knoten
            - E: Menge der Kanten
            - in: Eingangsknoten w
            - out: Ausgangsknoten w
        """
        w = self
        e = self.expression

        vertices_1, edges_1, in_node_1, out_node_1 = e.cfg(psi)

        vertices = vertices_1 | {w}
        edges = edges_1 | {(out_node_1, '', w)}
        in_node = in_node_1
        out_node = w

        return vertices, edges, in_node, out_node

class DO(compiler.DO):
    def cfg(self, psi):
        """
        Control Flow Graph für DO:

        Gemäß der Regel wenn w = do {e2} while e1 dann
        V = V1 + V2 + {diamond, glue}
        E = E1 + E2 + {(out2, ε, in1), (out1, ε, diamond), (diamond, T, in2), (diamond, F, glue)}
        in = in2
        out = glue

        where V1, E1, in1, out1 = cfg(e1, psi) und V2, E2, in2, out2 = cfg(e2, psi)
            und diamond und glue neue Knoten sind
        """
        w = self
        e1 = self.condition
        e2 = self.body

        vertices_1, edges_1, in_node_1, out_node_1 = e1.cfg(psi)
        vertices_2, edges_2, in_node_2, out_node_2 = e2.cfg(psi)

        diamond = ('diamond', w)
        glue = ('glue', w)

        vertices = vertices_1 | vertices_2 | {diamond, glue}
        edges = (edges_1 | edges_2 |
                 {(out_node_2, '', in_node_1), (out_node_1, '', diamond), 
                  (diamond, 'T', in_node_2), (diamond, 'F', glue)})
        in_node = in_node_2
        out_node = glue

        return vertices, edges, in_node, out_node


def remove_glue_nodes(vertices, edges, in_node, out_node):
    """
    Entfernt überflüssige glue-Knoten aus dem CFG.
    
    Ein glue-Knoten ist ein Durchgangsknoten, der die beiden Zweige eines
    IF oder WHILE wieder zusammenführt. Diese Knoten haben keine semantische
    Bedeutung und können entfernt werden, indem die Kanten direkt verbunden werden.
    
    Args:
        vertices: Menge der Knoten
        edges: Menge der Kanten (Tupel: (from, label, to))
        in_node: Eingangsknoten
        out_node: Ausgangsknoten
    
    Returns:
        Tupel (vertices, edges, in_node, out_node) ohne glue-Knoten
    """
    # Finde alle glue-Knoten (aber behalte out_node wenn es ein glue ist)
    glue_nodes = set()
    for v in vertices:
        if isinstance(v, tuple) and len(v) == 2 and v[0] == 'glue':
            # Nur entfernen wenn es nicht der out_node ist
            if v != out_node:
                glue_nodes.add(v)
    
    # Entferne jeden glue-Knoten
    new_vertices = vertices - glue_nodes
    new_edges = set()
    
    for glue in glue_nodes:
        # Finde alle eingehenden Kanten zum glue-Knoten
        incoming = [(src, label) for src, label, dst in edges if dst == glue]
        
        # Finde alle ausgehenden Kanten vom glue-Knoten
        outgoing = [(label, dst) for src, label, dst in edges if src == glue]
        
        # Verbinde alle eingehenden mit allen ausgehenden Kanten
        for src, in_label in incoming:
            for out_label, dst in outgoing:
                # Kombiniere die Labels (normalerweise beide leer)
                combined_label = in_label if in_label else out_label
                new_edges.add((src, combined_label, dst))
    
    # Füge alle Kanten hinzu, die nicht glue-Knoten betreffen
    for src, label, dst in edges:
        if src not in glue_nodes and dst not in glue_nodes:
            new_edges.add((src, label, dst))
    
    # Aktualisiere in_node und out_node, falls sie glue-Knoten waren
    new_in_node = in_node
    new_out_node = out_node
    
    if in_node in glue_nodes:
        # Finde den neuen in_node (sollte normalerweise nicht vorkommen)
        for src, label, dst in edges:
            if dst == in_node:
                new_in_node = src
                break
    
    if out_node in glue_nodes:
        # Finde den neuen out_node
        for src, label, dst in edges:
            if src == out_node:
                new_out_node = dst
                break
    
    return new_vertices, new_edges, new_in_node, new_out_node


def export_cfg_to_dot(vertices, edges, in_node, out_node, filename):
    """
    Exportiert einen Control Flow Graph im DOT-Format.
    
    Args:
        vertices: Menge der Knoten
        edges: Menge der Kanten (Tupel: (from, label, to))
        in_node: Eingangsknoten
        out_node: Ausgangsknoten
        filename: Pfad zur Ausgabedatei
    """
    # Entferne glue-Knoten vor dem Export
    vertices, edges, in_node, out_node = remove_glue_nodes(vertices, edges, in_node, out_node)
    
    lines = ['digraph CFG {']
    lines.append('  rankdir=TB;')
    lines.append('  node [fontname="Arial"];')
    lines.append('')
    
    # Mapping von Knoten zu eindeutigen IDs
    node_to_id = {}
    node_counter = 0
    
    def get_node_id(node):
        nonlocal node_counter
        if node not in node_to_id:
            node_to_id[node] = f'n{node_counter}'
            node_counter += 1
        return node_to_id[node]
    
    def format_label(node):
        """Formatiert das Label eines Knotens für DOT."""
        if isinstance(node, str):
            return node
        elif isinstance(node, tuple):
            # Tupel wie (START, decl) oder (CALL, w) oder (RET, w) oder (diamond, w) oder (glue, w)
            if len(node) == 2:
                label_type, obj = node
                
                # Für diamond und glue: spezielle Labels
                if label_type == 'diamond':
                    return '<?>'
                elif label_type == 'glue':
                    return label_type
                
                # Funktionsname extrahieren
                func_name = None
                if hasattr(obj, 'fname'):
                    # DECL oder CALL mit fname
                    func_name = obj.fname
                elif hasattr(obj, '__class__'):
                    # Anderes Objekt - versuche fname zu finden
                    if hasattr(obj, 'fname'):
                        func_name = obj.fname
                
                if func_name:
                    # Bei CALL und RET: füge arguments hinzu
                    if label_type in ('CALL', 'RET') and hasattr(obj, 'arguments'):
                        args_str = ', '.join(format_label(arg) for arg in obj.arguments)
                        return f"{label_type} {func_name}({args_str})"
                    # Bei START und END: füge params hinzu
                    elif label_type in ('START', 'END') and hasattr(obj, 'params'):
                        params_str = ', '.join(param.name if hasattr(param, 'name') else str(param) for param in obj.params)
                        return f"{label_type} {func_name}({params_str})"
                    return f"{label_type} {func_name}"
                else:
                    return f"{label_type} {obj.__class__.__name__}"
            
            # Fallback für andere Tupel-Formate
            parts = []
            for part in node:
                if isinstance(part, str):
                    parts.append(part)
                elif hasattr(part, 'fname'):
                    parts.append(part.fname)
                elif hasattr(part, '__class__'):
                    parts.append(part.__class__.__name__)
                else:
                    parts.append(str(part))
            return ' '.join(parts)
        elif hasattr(node, '__class__'):
            # AST-Knoten: zeige konkreten Inhalt
            class_name = node.__class__.__name__
            
            # CONST: zeige den Wert
            if class_name == 'CONST' and hasattr(node, 'value'):
                return str(node.value)
            
            # VAR: zeige den Variablennamen
            elif class_name == 'VAR' and hasattr(node, 'name'):
                return node.name
            
            # BINOP: zeige die komplette Operation
            elif class_name == 'BINOP' and hasattr(node, 'operator'):
                left_str = format_label(node.left) if hasattr(node, 'left') else '?'
                right_str = format_label(node.right) if hasattr(node, 'right') else '?'
                return f"{left_str}{node.operator}{right_str}"
            
            # ASSIGN: zeige Zuweisung
            elif class_name == 'ASSIGN' and hasattr(node, 'variable'):
                var_name = node.variable.name if hasattr(node.variable, 'name') else str(node.variable)
                return f"{var_name}="
            
            # IF: zeige "if"
            elif class_name == 'IF':
                return 'if'
            
            # WHILE: zeige "while"
            elif class_name == 'WHILE':
                return 'while'
            
            # DO: zeige "do"
            elif class_name == 'DO':
                return 'do'
            
            # SEQ: zeige ";"
            elif class_name == 'SEQ':
                return ';'
            
            # CALL: zeige Funktionsaufruf
            elif class_name == 'CALL' and hasattr(node, 'fname'):
                return f"CALL {node.fname}"
            
            # Default: Klassenname
            else:
                return class_name
        else:
            return str(node)
    
    def get_node_shape(node):
        """Bestimmt die Form eines Knotens basierend auf seinem Typ."""
        label = format_label(node)
        
        # IN/OUT als Kreis (doublecircle)
        if label == 'IN' or label == 'OUT':
            return 'doublecircle', label
        
        # diamond als Diamant (kann Tupel oder String sein)
        if label == '<?>' or (isinstance(node, tuple) and len(node) == 2 and node[0] == 'diamond'):
            return 'diamond', label
        
        # START/END/CALL/RET als Box
        if isinstance(node, tuple) and len(node) >= 1:
            if isinstance(node[0], str) and node[0] in ('START', 'END', 'CALL', 'RET'):
                return 'box', label
        
        # glue als Box (kann Tupel oder String sein)
        if label == 'glue' or (isinstance(node, tuple) and len(node) == 2 and node[0] == 'glue'):
            return 'box', label
        
        # Normale Knoten als Ellipse
        return 'ellipse', label
    
    # Spezielle Knoten für IN und OUT
    in_id = get_node_id('IN')
    out_id = get_node_id('OUT')
    
    lines.append(f'  {in_id} [shape=doublecircle, label="IN"];')
    lines.append(f'  {out_id} [shape=doublecircle, label="OUT"];')
    lines.append('')
    
    # Sammle alle Knoten aus vertices und edges
    all_nodes = set(vertices)
    all_nodes.add(in_node)
    all_nodes.add(out_node)
    
    # Füge auch alle Knoten aus den Kanten hinzu
    for edge in edges:
        if len(edge) == 3:
            from_node, _, to_node = edge
        else:
            from_node, to_node = edge
        all_nodes.add(from_node)
        all_nodes.add(to_node)
    
    # Alle anderen Knoten definieren
    for vertex in all_nodes:
        if vertex == 'IN' or vertex == 'OUT':
            continue  # Bereits definiert
        
        vid = get_node_id(vertex)
        shape, label = get_node_shape(vertex)
        lines.append(f'  {vid} [shape={shape}, label="{label}"];')
    
    lines.append('')
    
    # Kante von IN zum Eingangsknoten
    in_node_id = get_node_id(in_node)
    lines.append(f'  {in_id} -> {in_node_id};')
    
    # Alle Kanten aus dem CFG
    for edge in edges:
        if len(edge) == 3:
            from_node, label, to_node = edge
        else:
            # Falls Kanten ohne Label
            from_node, to_node = edge
            label = ''
        
        from_id = get_node_id(from_node)
        to_id = get_node_id(to_node)
        
        if label:
            lines.append(f'  {from_id} -> {to_id} [label="{label}"];')
        else:
            lines.append(f'  {from_id} -> {to_id};')
    
    # Kante vom Ausgangsknoten zu OUT
    out_node_id = get_node_id(out_node)
    lines.append(f'  {out_node_id} -> {out_id};')
    
    lines.append('}')
    
    # In Datei schreiben
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f'CFG exported to: {filename}')