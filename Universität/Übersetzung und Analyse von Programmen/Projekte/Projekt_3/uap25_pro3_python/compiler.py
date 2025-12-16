
import syntax
from  vistram.tram import *

def assemble(tram_code,filename=""):
    assembly_code = ""
    Label.count=0
    tram_code+=[halt()]
    for instruction in tram_code:
        if (assembly_code != ""):
            assembly_code += "\n"
        assembly_code += instruction.toString()
    if (filename!=""):
        f = open(filename, "w", encoding="utf-8")
        f.write(assembly_code)
    return assembly_code

def elab_def(d,rho, nl):
    return
##########################################

class CONST(syntax.CONST):
    def code(self, rho, nl):
        return [const(self.value)]

class WHILE(syntax.WHILE):
    # Diese Übersetzung von WHILE entspricht nicht der Semantik von TRIPLA !!!
    def code(self, rho, nl):
        l1 = Label()
        l2 = Label()
        code_condition = self.condition.code(rho, nl)
        code_body = self.body.code(rho, nl)
        code_condition[0].assigned_labels += [l1] # Die erste Instruktion könnte schon einen Label haben, daher +=
        return code_condition + [ifzero(l2)]+code_body+[goto(l1)] + [nop(assigned_label=l1)]

class LET(syntax.LET):
    def code(self, declarations, body, rho, nl):
        l1 = Label()
        rho = elab_def(body, rho, nl)
        code_call = CALL.code(body, rho, nl)
        code_declarations = ""
        for declaration in declarations:
            code_declarations += declaration.code(rho, nl)
        return [goto l] + code_declarations +

class DECL(syntax.DECL):
    def code(self, fname, parameters, body, rho, nl):
        return

class CALL(syntax.CALL):
    def code(self, fname, parameters, rho, nl):
        for parameter in parameters:
            code = parameter.code(rho, nl)
        return ""

class VAR(syntax.VAR):
    def code(self, rho, nl):
        return