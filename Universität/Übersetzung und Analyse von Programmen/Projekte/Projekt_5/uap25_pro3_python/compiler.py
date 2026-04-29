#Matthias Janßen
#1871808
import syntax
from vistram.tram import *

# Globaler Cache für DFA-Ergebnisse zur Optimierung
_active_defs = None

def set_active_definitions(defs):
    global _active_defs
    _active_defs = defs

def assemble(tram_code,filename="./tram_out/out.tram"):
    assembly_code = ""
    Label.count = 0
    tram_code += [halt()]
    for instruction in tram_code:
        if assembly_code != "":
            assembly_code += "\n"
        assembly_code += instruction.toString()
    if filename != "":
        f = open(filename, "w", encoding="utf-8")
        f.write(assembly_code)
    return assembly_code


def elab_def(declarations, rho, nl):
    """(E1) elab_def (d1 ... dk) ρ nl = ρk wobei ρ0 = ρ und ρi = elab_def di ρi-1 nl
    
    Erarbeitet eine Liste von Funktionsdeklarationen und gibt die aktualisierte Umgebung zurück.
    
    Args:
        declarations: Liste von DECL-Knoten
        rho: Aktuelle Umgebung (Liste von Bindungen)
        nl: Verschachtelungsebene
        
    Returns:
        Aktualisierte Umgebung mit Funktionsdefinitionen
    """
    if not isinstance(declarations, list):
        declarations = [declarations]
    
    result_rho = rho
    for decl in declarations:
        result_rho = elab_def_single(decl, result_rho, nl)
    return result_rho


def elab_def_single(decl, rho, nl):
    r"""(E2) elab_def (id{id1,...,idk}{e}) ρ nl = ρ[(ℓ,nl)\id]
    wobei ℓ ein neues Label ist
    
    Erarbeitet eine einzelne Funktionsdeklaration.
    
    Args:
        decl: Einzelner DECL-Knoten
        rho: Aktuelle Umgebung
        nl: Verschachtelungsebene
        
    Returns:
        Aktualisierte Umgebung mit neuer Funktionsbindung
    """

    l = Label()
    # Füge Bindung (label, nl) -> fname zur Umgebung hinzu
    rho = rho | {decl.fname:(l,nl)}
    return rho


##########################################

class BOOL(syntax.BOOL):
    def code(self, rho, nl):
        """Kompiliert einen Boolean zu einer CONST-Anweisung (1 für true, 0 für false)."""
        return [const(1 if self.value else 0)]

class CONST(syntax.CONST):
    def __init__(self, value):
        super().__init__(value)
        self.tram_code = self.code([], 0)
    
    def code(self, rho, nl):
        """(K3) code (c) ρ nl = const(c)
        
        Kompiliert eine Konstante zu einer CONST-Anweisung.
        """
        return [const(self.value)]

class WHILE(syntax.WHILE):
    def __init__(self, condition, body):
        super().__init__(condition, body)
    
    def code(self, rho, nl):
        """(K5) code (while B do {E}) ρ nl = 
            ℓ1: code(B) ρ nl; IFZERO ℓ2; code(E) ρ nl; GOTO ℓ1; ℓ2: NOP
            
            wobei ℓ1, ℓ2 neue Labels sind
        """
        l1 = Label()
        l2 = Label()
        l3 = Label()
        l4 = Label()

        code_condition = self.condition.code(rho, nl)
        code_body = self.body.code(rho, nl)

        code_condition_unlabeled = code_condition

        code_condition[0].assigned_labels += [l1]
        code_body[0].assigned_labels += [l4]

        return (code_condition_unlabeled + [ifzero(l3)] + [goto(l4)]
                + code_condition + [ifzero(l2)] + [pop]
                + code_body + [goto(l1)]
                + [const(0, assigned_label=l3)]
                + [nop(assigned_label=l2)])


class LET(syntax.LET):
    def __init__(self, declarations, body):
        super().__init__(declarations, body)
    
    def code(self, rho, nl):
        """(K2) code (let d in e) ρ nl = 
            goto ℓ;
            code(d) ρ' nl;
            ℓ: code(e) ρ' nl
            
            wobei ℓ ein neues Label ist und ρ' = elab_def(d) ρ nl
        """
        l1 = Label()

        rho1 = elab_def(self.declarations, rho, nl)

        # Generiere Code für den Body-Ausdruck
        code_body = self.body.code(rho1, nl)

        if code_body:
            code_body[0].assigned_labels += [l1]

        # Generiere Code für Deklarationen mit aktualisierter Umgebung
        code_declarations = []

        if isinstance(self.declarations, list):
            for decl in self.declarations:
                code_declarations.extend(decl.code(rho1, nl))
        else:
            code_declarations = self.declarations.code(rho1, nl)

        return [goto(l1)] + code_declarations + code_body


class DECL(syntax.DECL):
    def __init__(self, fname, params, body):
        super().__init__(fname, params, body)
    
    def code(self, rho, nl):
        r"""(K13) code (id{id1,...,idk}{e}) ρ nl = 
            ℓ : code(e) ρ[(0,nl+1)\id1] ... [(k-1,nl+1)\idk] nl+1;
            return
            
        wobei ℓ ein neues Label ist und ρ(id) = (ℓ, nl')
        """
        # Erstelle ein Label für diese Funktion mit ihrem Namen
        l1 = rho[self.fname][0]
        
        # Erstelle Umgebung für Funktionsparameter
        param_rho = rho  # Kopiere aktuelle Umgebung
        # Füge Parameterbindungen hinzu: (offset, nl+1) -> param_id
        for i, param in enumerate(self.params):
            param_rho = param_rho | {param.name:(i, nl + 1)}

        # Speichere Methoden-Label
        param_rho = param_rho | {self.fname:(l1, nl)}

        # Generiere Code für Funktionsbody mit aktualisierter Umgebung
        code_body = self.body.code(param_rho, nl + 1)
        code_body[0].assigned_labels += [l1]
        # Return-Code: ℓ : code_body ; return
        return code_body + [ireturn()]


class CALL(syntax.CALL):
    def __init__(self, fname, arguments):
        super().__init__(fname, arguments)
    
    def code(self, rho, nl):
        """(K12) code (id(e1,...,ek)) ρ nl = 
            code(e1) ρ nl;
            ...
            code(ek) ρ nl;
            invoke k ℓ (nl - nl')
            
            wobei ρ(id) = (ℓ, nl')
        """
        # Finde die Funktion in der Umgebung
        rho_value = rho[self.fname]
        label = rho_value[0]
        func_nl = rho_value[1]

        
        # Generiere Code für Argumente
        code_args = []
        if isinstance(self.arguments, list):
            for arg in self.arguments:
                code_args.extend(arg.code(rho, nl))
        else:
            code_args = self.arguments.code(rho, nl)
        
        # Berechne Tiefenunterschied
        depth = nl - func_nl
        
        # Generiere Invoke-Anweisung
        k = len(self.arguments)

        return code_args + [invoke(k, label, depth)]


class VAR(syntax.VAR):
    def __init__(self, name):
        super().__init__(name)
    
    def code(self, rho, nl):
        """Variablenzugriff: Nachschlag in der Umgebung und Wert laden.
        
        Gibt eine LOAD-Anweisung mit entsprechendem Offset und Tiefe zurück.
        """
        # Finde Variable in der Umgebung
        rho_value = rho[self.name]
        offset = rho_value[0]
        var_nl = rho_value[1]
        depth = nl - var_nl

        return [load(offset, depth)]


class BINOP(syntax.BINOP):
    """Binäroperation (arithmetisch oder boolean)."""
    def __init__(self, op, left, right):
        super().__init__(op, left, right)
        self.op = op
        self.left = left
        self.right = right
    
    def code(self, rho, nl):
        """Binäroperationen: Beide Operanden auswerten und Operation anwenden.
        Spezialbehandlung für logische Operatoren (nicht-strikte Auswertung).
        """
        if self.op == '&&':
            # E1 && E2  =>  if E1 then E2 else false
            # Wir verwenden die IF-Logik für nicht-strikte Auswertung
            from compiler import IF, CONST
            return IF(self.left, self.right, CONST(False)).code(rho, nl)
        
        if self.op == '||':
            # E1 || E2  =>  if E1 then true else E2
            from compiler import IF, CONST
            return IF(self.left, CONST(True), self.right).code(rho, nl)

        code_left = self.left.code(rho, nl)
        code_right = self.right.code(rho, nl)
        
        # Abbildung von Operatoren auf TRAM-Anweisungen
        op_map = {
            '+': add,
            '-': sub,
            '*': mul,
            '/': div,
            '<': lt,
            '>': gt,
            '<>': neq,
            '!=': neq,
            '==': eq
        }
        
        op_instruction = op_map.get(self.op)

        return code_left + code_right + [op_instruction()]
    
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"


class IF(syntax.IF):
    """If-then-else Ausdruck."""
    def __init__(self, condition, then_exp, else_exp):
        super().__init__(condition, then_exp, else_exp)
        self.condition = condition
        self.then_exp = then_exp
        self.else_exp = else_exp
    
    def code(self, rho, nl):
        """(K6) code (if B then E1 else E2) ρ nl = 
            code(B) ρ nl; IFZERO ℓ2; code(E1) ρ nl; GOTO ℓ3;
            ℓ2: code(E2) ρ nl; ℓ3: NOP
            
            wobei ℓ2, ℓ3 neue Labels sind
        """
        l1 = Label()
        l2 = Label()
        
        code_cond = self.condition.code(rho, nl)
        code_then = self.then_exp.code(rho, nl)
        code_else = self.else_exp.code(rho, nl)
        
        code_else[0].assigned_labels += [l1]

        return code_cond + [ifzero(l1)] + code_then + [goto(l2)] + code_else + [nop(assigned_label=l2)]
    
    def __str__(self):
        return f"if {self.condition} then {self.then_branch} else {self.else_branch}"


class SEQ(syntax.SEQ):
    """Sequenzielle Zusammensetzung von Ausdrücken."""
    def __init__(self, exp1, exp2):
        super().__init__(exp1, exp2)
        self.exp1 = exp1
        self.exp2 = exp2
    
    def code(self, rho, nl):
        """Sequenzielle Zusammensetzung: Führe den linken Ausdruck aus, dann den rechten."""
        exp1 = self.exp1.code(rho, nl)
        exp2 = self.exp2.code(rho, nl)
        return exp1 + [pop()] + exp2
    
    def __str__(self):
        return f"({self.exp1} ; {self.exp2})"


class ASSIGN(syntax.ASSIGN):
    """Variablenzuweisung."""
    def code(self, rho, nl):
        """Zuweisung: Wert auswerten und in der Variable speichern."""
        # Finde Variable in der Umgebung
        rho_value = rho[self.variable]

        offset = rho_value[0]
        var_nl = rho_value[1]
        depth = nl - var_nl

        code_value = self.expression.code(rho, nl)
        
        # Optimierung: Wenn die Zuweisung keine Verwendung erreicht,
        # lassen wir den store/load Teil weg.
        if _active_defs is not None:
            var_name = self.variable.name if hasattr(self.variable, 'name') else str(self.variable)
            if (self, var_name) not in _active_defs:
                # print(f"DEBUG: Optimizing out assignment to {var_name} at {self}")
                return code_value
        
        return code_value + [store(offset, depth)] + [load(offset, depth)]


class DO(syntax.DO):
    """Do-while Ausdruck."""
    def __init__(self, body, condition):
        super().__init__(body, condition)
        self.body = body
        self.condition = condition
    
    def code(self, rho, nl):
        """(K7) code (do {E} while B) ρ nl = 
            ℓ1: code(E) ρ nl; code(B) ρ nl; IFZERO ℓ2; GOTO ℓ1;
            ℓ2: NOP
            
            wobei ℓ1, ℓ2 neue Labels sind
        """
        l1 = Label()
        l2 = Label()
        
        code_body = self.body.code(rho, nl)
        code_cond = self.condition.code(rho, nl)
        
        # Label für Schleifenbeginn
        code_body[0].assigned_labels += [l1]

        return code_body + code_cond + [ifzero(l2)] + [goto(l1)] + [nop(assigned_label=l2)]

    def __str__(self):
        return f"do {{ {self.body} }} while {self.condition}"