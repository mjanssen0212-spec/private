
# Matthias Janßen
# 1871808
# (c) Stephan Diehl, University of Trier, Germany, 2025

import html

class EXPRESSION:
    ppcount=0

    def __init__(self):
        self.pp=EXPRESSION.ppcount
        EXPRESSION.ppcount=EXPRESSION.ppcount+1

    def copy(self):
        return EXPRESSION()

    def allNodes(self):
        ret = [self]
        for node in (self.__getattribute__(a) for a in self.__dict__.keys()):
            if isinstance(node, EXPRESSION):
                ret = ret + node.allNodes()
            if isinstance(node, list):
                for n in node:
                    if isinstance(n, EXPRESSION):
                        ret = ret + n.allNodes()
        return ret

    def _escape_label(self, s: str) -> str:
        """Label für das DOT-Format maskieren."""
        return html.escape(s).replace('\n', '\\n').replace('"', '\\"')

    def _to_dot(self, idmap, counter):
        """Erzeugt eine DOT-Repräsentation für diesen Knoten und gibt seine Knoten-ID zurück.
        
        Args:
            idmap: Dictionary, das Python-Objekt-IDs auf DOT-Knoten-IDs abbildet
            counter: Liste mit einer einzelnen Ganzzahl zur Verfolgung der Knotenanzahl
            
        Returns:
            Tupel aus (node_id, Liste von DOT-Zeilen für diesen Teilbaum)
        """
        nid = f'n{counter[0]}'
        counter[0] += 1
        idmap[id(self)] = nid
        
        # Label erstellen: Klassenname mit allen Blattwerten
        label = self.__class__.__name__
        
        # Blattwerte zum Label für bestimmte Knotentypen hinzufügen
        leaf_values = []
        for attr_name in self.__dict__:
            if attr_name == 'pp':  # Internen Zähler überspringen
                continue
            attr_val = getattr(self, attr_name)
            
            # Einfache Blattwerte zum Label hinzufügen (nicht EXPRESSION oder Liste)
            if not isinstance(attr_val, EXPRESSION) and not isinstance(attr_val, list):
                leaf_values.append(f"{attr_name}={attr_val}")
        
        if leaf_values:
            label = label + "\\n" + ", ".join(leaf_values)
        
        label = self._escape_label(label)
        
        # DOT-Knotendefinition generieren
        lines = [f'  {nid} [label="{label}"];']
        
        # Kind-Attribute verarbeiten
        for attr_name in self.__dict__:
            if attr_name == 'pp':  # Internen Zähler überspringen
                continue
            attr_val = getattr(self, attr_name)
            
            if isinstance(attr_val, EXPRESSION):
                # Einzelner Kindknoten
                child_nid, child_lines = attr_val._to_dot(idmap, counter)
                lines.extend(child_lines)
                lines.append(f'  {nid} -> {child_nid} [label="{attr_name}"];')
            elif isinstance(attr_val, list):
                # Liste von Kindern (z.B. Deklarationen, Argumente)
                for i, item in enumerate(attr_val):
                    if isinstance(item, EXPRESSION):
                        child_nid, child_lines = item._to_dot(idmap, counter)
                        lines.extend(child_lines)
                        lines.append(f'  {nid} -> {child_nid} [label="{attr_name}[{i}]"];')
        
        return nid, lines

    def to_dot(self):
        """Generiert die vollständige DOT-Repräsentation des AST.
        
        Returns:
            Ein String, der den vollständigen DOT-Graphen enthält
        """
        idmap = {}
        counter = [0]
        lines = ['digraph AST {', '  node [shape=box, fontname="Arial"];']
        
        root_nid, root_lines = self._to_dot(idmap, counter)
        lines.extend(root_lines)
        
        lines.append('}')
        return '\n'.join(lines)

    def export_dot(self, filename: str):
        """Exportiert den AST als DOT-Datei.
        
        Args:
            filename: Pfad zur Ausgabe-DOT-Datei
        """
        dot_content = self.to_dot()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(dot_content)

class LET(EXPRESSION):
    def __init__(self, declarations, body):
        super().__init__()
        self.declarations=declarations
        self.body=body

    def __str__(self): return "let " \
        +','.join([ str(decl) for decl in self.declarations ]) \
        + " in " + str(self.body)

class DECL(EXPRESSION):
    def __init__(self, fname, params, body):
        self.fname=fname
        self.params=params
        self.body=body

    def __str__(self): return self.fname+"(" \
        +','.join([ str(param) for param in self.params ]) \
        +"){ "+str(self.body)+" }"

class CALL(EXPRESSION):
    def __init__(self, fname, arguments):
        super().__init__()
        self.fname=fname
        self.arguments=arguments

    def __str__(self): return self.fname+"(" \
        +','.join([ str(arg) for arg in self.arguments ]) +")"


class VAR(EXPRESSION):
    def __init__(self,name):
        super().__init__()
        self.name=name

    def __str__(self): return self.name

class BINOP(EXPRESSION):
    def __init__(self,operator,arg1,arg2):
        super().__init__()
        self.operator=operator
        self.arg1=arg1
        self.arg2=arg2

    def __str__(self): return "("+str(self.arg1)+self.operator+str(self.arg2)+")"

class CONST(EXPRESSION):
    def __init__(self,value):
        super().__init__()
        self.value=value

    def __str__(self): return str(self.value)

class BOOL(CONST):
    pass

class ASSIGN(EXPRESSION):
    def __init__(self, variable, expression):
        super().__init__()
        self.variable=variable
        self.expression=expression

    def __str__(self):
        var_name = self.variable.name if hasattr(self.variable, 'name') else str(self.variable)
        return var_name+"="+str(self.expression)

class SEQ(EXPRESSION):
    def __init__(self, exp1, exp2):
        super().__init__()
        self.exp1=exp1
        self.exp2=exp2

    def __str__(self): return str(self.exp1)+";"+str(self.exp2)

class IF(EXPRESSION):
    def __init__(self,condition,exp1,exp2):
        super().__init__()
        self.condition=condition
        self.exp1=exp1
        self.exp2=exp2

    def __str__(self): return "if "+str(self.condition)+" then { " \
            + str(self.exp1)+" } else { "+str(self.exp2)+" } "

class DO(EXPRESSION):
    def __init__(self,body,condition):
        super().__init__()
        self.body=body
        self.condition=condition

    def __str__(self): return "do { "+str(self.body)+" } while "+str(self.condition)

class WHILE(EXPRESSION):
    def __init__(self,condition,body):
        super().__init__()
        self.condition=condition
        self.body=body

    def __str__(self): return "while "+str(self.condition)+" do { "+str(self.body)+" }"

# see https://stackoverflow.com/questions/51753937/python-pretty-print-nested-objects

def pretty_print(clas, indent=0):
    print(' ' * indent +  type(clas).__name__ +  ':')
    indent += 4
    for k,v in clas.__dict__.items():
        if '__dict__' in dir(v):
            pretty_print(v,indent)
        else:
            print(' ' * indent +  k + ': ' + str(v))



