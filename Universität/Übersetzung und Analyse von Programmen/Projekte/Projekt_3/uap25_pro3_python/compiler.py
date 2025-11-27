
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




