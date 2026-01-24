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
        edges = {}
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

        diamond = 'diamond'
        glue = 'glue'

        vertices = vertices_1 | vertices_2 | {diamond, glue}
        edges = (edges_1 | edges_2 |
                 {(out_node_1, '', glue), (diamond, 'T', in_node_2), (diamond, 'F', glue), (out_node_2, '', in_node_1)})
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
            psi_1[decl] = (in_i, out_i)
        
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
        edges = edges_1 | {(in_node_f, '', in_node_1), (out_node_f, '', out_node_1)}
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
        edges = {}
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

        diamond = 'diamond'
        glue = 'glue'

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
        E = E1 + E2 + {(out, ε, in2)}
        in = in1
        out = w

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

        diamond = 'diamond'
        glue = 'glue'

        vertices = vertices_1 | vertices_2 | {diamond, glue}
        edges = (edges_1 | edges_2 |
                 {(out_node_2, '', in_node_1), (out_node_1, '', diamond), 
                  (diamond, 'T', in_node_2), (diamond, 'F', glue)})
        in_node = in_node_2
        out_node = glue

        return vertices, edges, in_node, out_node