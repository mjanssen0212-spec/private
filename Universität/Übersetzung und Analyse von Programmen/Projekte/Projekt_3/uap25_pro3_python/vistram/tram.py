
# (c) Stephan Diehl, University of Trier, Germany, 2025

class TRAM:
    def __init__(self, prog):
        self.set_label_addresses(prog)
        self.program=prog+[halt()]
        self.print_prog(self.program)
        self.pc = 0
        self.stack = []
        self.top = -1
        self.pp = 0 #-1
        self.fp = 0 #-1

    def start(self):
        while self.pc>=0:
            self.print_instruction(self.program[self.pc])
            self.program[self.pc].execute(self)
            print(self.stack)

    def set_label_addresses(self,code):
        pos = 0
        for instr in code:
            for label in instr.assigned_labels:
                label.address = pos
            pos = pos + 1

    def pop(self):
        del self.stack[self.top]
        self.top = self.top - 1

    def push(self,v):
        self.stack.append(v)
        self.top = self.top + 1

    def spp(self,d,pp,fp):
        if (d==0):
            return pp
        else:
            return self.spp(d-1,self.stack[self.fp+3],self.stack[self.fp+4])

    def sfp(self, d, pp, fp):
        if (d==0):
            return fp
        else:
            return self.sfp(d-1, self.stack[self.fp+3], self.stack[self.fp+4])

    def print_prog(self,prog):
        pos=0
        for instr in prog:
            print(str(pos)+": ",end="")
            pos=pos+1
            self.print_instruction(instr)

    def print_instruction(self, instr):
            print(type(instr).__name__, end = "")
            for attr in vars(instr).keys():
                value=getattr(instr,attr)
                if isinstance(value,list): continue
                if isinstance(value,Label):
                    value="#"+str(value.address)
                else:
                    value=str(value)
                print(" "+value,end="")
            print()

#################

class Label:
    count=0
    address=-1

    def __init__(self,address=-1,text=""):
        Label.count+=1
        self.id=Label.count
        self.address=address
        if text=="":
            self.text=f"L{Label.count}"
        else:
            self.text=text

    def toString(self): return self.text


##################

class Instruction:

    def __init__(self,assigned_label=None):
        self.assigned_labels = []
        if not assigned_label is None:
            if isinstance(assigned_label,Label):
                self.assigned_labels+=[assigned_label]
            else:
                self.assigned_labels+=assigned_label

    def toString(self):
        s=self.toStringx()
        #print(s)
        return(s)

    def toStringx(self):
        if (len(self.assigned_labels)==0):
            return "  "
        else:
            return ','.join( [ label.toString()
                               for label in self.assigned_labels] )+": "

class halt(Instruction):
    def __init__(self,assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        tram.pc=-1

    def toString(self): return super().toString()+"HALT"

class nop(Instruction):
    def __init__(self,assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        tram.pc=tram.pc+1

    def toString(self): return super().toString()+"NOP"

class pop(Instruction):
    def __init__(self,assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self): return super().toString()+"POP"

class const(Instruction):
    def __init__(self, k, assigned_label=None):
        super().__init__(assigned_label=assigned_label)
        self.k=k

    def execute(self,tram):
        tram.push(self.k)
        tram.pc=tram.pc+1

    def toString(self): return super().toString()+"CONST "+str(self.k)

class store(Instruction):
    def __init__(self, k, assigned_label=None):
        super().__init__(assigned_label=assigned_label)
        self.k=k
        self.d=d

    def execute(self,tram):
        tram.stack[tram.spp(self.d,tram.pp,tram.fp)+self.k]=tram.stack[tram.top]
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self):
        return super().toString()+"STORE "+str(self.k)+" "+str(self.d)

class load(Instruction):
    def __init__(self, k, d, assigned_label=None):
        super().__init__(assigned_label=assigned_label)
        self.k=k
        self.d=d

    def execute(self,tram):
        tram.push(tram.stack[tram.spp(self.d,tram.pp,tram.fp)+self.k])
        tram.pc=tram.pc+1

    def toString(self):
        return super().toString()+"LOAD "+str(self.k)+" "+str(self.d)

class add(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        tram.stack[tram.top-1]=tram.stack[tram.top-1]+tram.stack[tram.top]
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self): return super().toString()+"ADD"



class sub(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        tram.stack[tram.top-1]=tram.stack[tram.top-1]-tram.stack[tram.top]
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self): return super().toString() + "SUB"

class mul(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        tram.stack[tram.top-1]=tram.stack[tram.top-1]*tram.stack[tram.top]
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self): return super().toString() + "MUL"

class div(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        tram.stack[tram.top-1]=tram.stack[tram.top-1]/tram.stack[tram.top]
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self): return super().toString() + "DIV"

class lt(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        if tram.stack[tram.top-1]<tram.stack[tram.top]:
            tram.stack[tram.top-1]=1
        else:
            tram.stack[tram.top-1]=0
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self): return super().toString() + "LT"

class gt(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        if tram.stack[tram.top-1]>tram.stack[tram.top]:
            tram.stack[tram.top-1]=1
        else:
            tram.stack[tram.top-1]=0
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self): return super().toString() + "GT"

class eq(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        if tram.stack[tram.top-1]==tram.stack[tram.top]:
            tram.stack[tram.top-1]=1
        else:
            tram.stack[tram.top-1]=0
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self): return super().toString() + "EQ"

class neq(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        if tram.stack[tram.top-1]!=tram.stack[tram.top]:
            tram.stack[tram.top-1]=1
        else:
            tram.stack[tram.top-1]=0
        tram.pop()
        tram.pc=tram.pc+1

    def toString(self): return super().toString() + "NEQ"

class land(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        if tram.stack[tram.top-1] == 1 & tram.stack[tram.top] == 1:
            tram.stack[tram.top-1]=1
        else:
            tram.stack[tram.top-1]=0
        tram.pop()
        tram.pc=tram.pc+1


class lor(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        if tram.stack[tram.top-1] == 1 | tram.stack[tram.top] == 1:
            tram.stack[tram.top-1]=1
        else:
            tram.stack[tram.top-1]=0
        tram.pop()
        tram.pc=tram.pc+1

class goto(Instruction):
    def __init__(self, label, assigned_label=None):
        super().__init__(assigned_label=assigned_label)
        self.label=label

    def execute(self,tram):
        tram.pc=self.label.address

    def toString(self):
        return super().toString() + "GOTO "+self.label.toString()

class ifzero(Instruction):
    def __init__(self, label, assigned_label=None):
        super().__init__(assigned_label=assigned_label)
        self.label=label

    def execute(self,tram):
        if tram.stack[tram.top]==0:
            tram.pc=self.label.address
        else:
            tram.pc=tram.pc+1
        tram.pop()

    def toString(self):
        return super().toString() + "IFZERO "+self.label.toString()

class invoke(Instruction):
    def __init__(self,n,label,d, assigned_label=None):
        super().__init__(assigned_label=assigned_label)
        self.n=n
        self.label=label
        self.d=d

    def execute(self,tram):
        tmp_top=tram.top
        tram.push(tram.pc+1)
        tram.push(tram.pp)
        tram.push(tram.fp)
        tram.push(tram.spp(self.d,tram.pp,tram.fp))
        tram.push(tram.sfp(self.d,tram.pp,tram.fp))
        tram.pp=tmp_top-self.n+1
        tram.fp=tmp_top+1
        tram.pc=self.label.address

    def toString(self):
        return super().toString() \
               + "INVOKE "+str(self.n)+" "+self.label.toString()+" "+str(self.d)

class ireturn(Instruction):
    def __init__(self, assigned_label=None):
        super().__init__(assigned_label=assigned_label)

    def execute(self,tram):
        res=tram.stack[tram.top]
        tram.top=tram.pp
        tram.pc=tram.stack[tram.fp]
        tram.pp=tram.stack[tram.fp+1]
        tram.fp=tram.stack[tram.fp+2]
        del tram.stack[tram.top:]
        tram.top=tram.top-1
        tram.push(res)

    def toString(self): return super().toString() + "RETURN"

