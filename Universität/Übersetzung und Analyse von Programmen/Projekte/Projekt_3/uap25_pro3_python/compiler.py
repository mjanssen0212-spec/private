
import syntax
from vistram.tram import *

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
    """(E1) elab_def (d1 ... dk) ρ nl = ρk where ρ0 = ρ and ρi = elab_def di ρi-1 nl
    
    Elaborates a list of function declarations and returns updated environment.
    
    Args:
        declarations: List of DECL nodes
        rho: Current environment (list of bindings)
        nl: Nesting level
        
    Returns:
        Updated environment with function definitions
    """
    if not isinstance(declarations, list):
        declarations = [declarations]
    
    result_rho = rho
    for decl in declarations:
        result_rho = elab_def_single(decl, result_rho, nl)
    return result_rho


def elab_def_single(decl, rho, nl):
    r"""(E2) elab_def (id{id1,...,idk}{e}) ρ nl = ρ[(ℓ,nl)\id]
    where ℓ is a new label
    
    Elaborates a single function declaration.
    
    Args:
        decl: Single DECL node
        rho: Current environment
        nl: Nesting level
        
    Returns:
        Updated environment with new function binding
    """

    l = Label()
    # Add binding (label, nl) -> fname to environment
    rho = rho | {decl.fname:(l,nl)}
    return rho


##########################################

class CONST(syntax.CONST):
    def __init__(self, value):
        super().__init__(value)
        self.tram_code = self.code([], 0)
    
    def code(self, rho, nl):
        """(K3) code (c) ρ nl = const(c)
        
        Compiles a constant to a CONST instruction.
        """
        return [const(self.value)]

class WHILE(syntax.WHILE):
    def __init__(self, condition, body):
        super().__init__(condition, body)
    
    def code(self, rho, nl):
        """(K5) code (while B do {E}) ρ nl = 
            ℓ1: code(B) ρ nl; IFZERO ℓ2; code(E) ρ nl; GOTO ℓ1; ℓ2: NOP
            
        where ℓ1, ℓ2 are new labels
        """
        l1 = Label()
        l2 = Label()
        code_condition = self.condition.code(rho, nl)
        code_body = self.body.code(rho, nl)
        # Assign l1 to the first instruction of condition
        if code_condition:
            code_condition[0].assigned_labels += [l1]
        return code_condition + [ifzero(l2)] + code_body + [goto(l1)] + [nop(assigned_label=l2)]


class LET(syntax.LET):
    def __init__(self, declarations, body):
        super().__init__(declarations, body)
    
    def code(self, rho, nl):
        """(K2) code (let d in e) ρ nl = 
            goto ℓ;
            code(d) ρ' nl;
            ℓ: code(e) ρ' nl
            
        where ℓ is a new label and ρ' = elab_def(d) ρ nl
        """
        l1 = Label()

        rho1 = elab_def(self.declarations, rho, nl)

        # Generate code for body expression
        code_body = self.body.code(rho1, nl)

        if code_body:
            code_body[0].assigned_labels += [l1]

        # Generate code for declarations with updated environment
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
            
        where ℓ is a new label and ρ(id) = (ℓ, nl')
        """
        # Create a label for this function with its name
        l1 = rho[self.fname][0]
        
        # Create environment for function parameters
        param_rho = rho  # Copy current environment
        # Add parameter bindings: (offset, nl+1) -> param_id
        for i, param in enumerate(self.params):
            param_rho = param_rho | {param.name:(i, nl + 1)}

        # Save method label
        param_rho = param_rho | {self.fname:(l1, nl)}

        # Generate code for function body with updated environment
        code_body = self.body.code(param_rho, nl + 1)
        code_body[0].assigned_labels += [l1]
        # Return code: ℓ : code_body ; return
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
            
        where ρ(id) = (ℓ, nl')
        """
        # Find the function in environment
        rho_value = rho[self.fname]
        label = rho_value[0]
        func_nl = rho_value[1]

        
        # Generate code for arguments
        code_args = []
        if isinstance(self.arguments, list):
            for arg in self.arguments:
                code_args.extend(arg.code(rho, nl))
        else:
            code_args = self.arguments.code(rho, nl)
        
        # Calculate depth difference
        depth = nl - func_nl
        
        # Generate invoke instruction
        k = len(self.arguments)

        return code_args + [invoke(k, label, depth)]


class VAR(syntax.VAR):
    def __init__(self, name):
        super().__init__(name)
    
    def code(self, rho, nl):
        """Variable access: look up in environment and load value.
        
        Returns LOAD instruction with appropriate offset and depth.
        """
        # Find variable in environment
        rho_value = rho[self.name]
        offset = rho_value[0]
        var_nl = rho_value[1]
        depth = var_nl - offset

        return [load(offset, depth)]


class BINOP(syntax.EXPRESSION):
    """Binary operation (arithmetic or boolean)."""
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
    
    def code(self, rho, nl):
        """Binary operations: evaluate both operands and apply operation."""
        code_left = self.left.code(rho, nl)
        code_right = self.right.code(rho, nl)
        
        # Map operators to TRAM instructions
        op_map = {
            '+': add,
            '-': sub,
            '*': mul,
            '/': div,
            '<': lt,
            '>': gt,
            '=': None,
            '<>': neq,
            '!=': neq,
            '==': eq,  # TODO: Implement logical AND
            '||': 'or',   # TODO: Implement logical OR
        }
        
        op_instruction = op_map.get(self.op)
        if op_instruction is None:
            raise RuntimeError(f"Unsupported operator: {self.op}")
        
        return code_left + code_right + [op_instruction()]
    
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"


class IF(syntax.EXPRESSION):
    """If-then-else expression."""
    def __init__(self, condition, then_branch, else_branch):
        super().__init__()
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def code(self, rho, nl):
        """(K6) code (if B then E1 else E2) ρ nl = 
            code(B) ρ nl; IFZERO ℓ2; code(E1) ρ nl; GOTO ℓ3;
            ℓ2: code(E2) ρ nl; ℓ3: NOP
            
        where ℓ2, ℓ3 are new labels
        """
        l2 = Label()
        l3 = Label()
        
        code_cond = self.condition.code(rho, nl)
        code_then = self.then_branch.code(rho, nl)
        code_else = self.else_branch.code(rho, nl)
        
        # Label for else branch
        if code_else:
            code_else[0].assigned_labels += [l2]
        else:
            code_else = [nop(assigned_label=l2)]
        
        # Label for end
        code_end = [nop(assigned_label=l3)]


        return code_cond + [ifzero(l2)] + code_then + [goto(l3)] + code_else + code_end
    
    def __str__(self):
        return f"if {self.condition} then {self.then_branch} else {self.else_branch}"


class SEQ(syntax.EXPRESSION):
    """Sequential composition of expressions."""
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
    
    def code(self, rho, nl):
        """Sequential composition: execute left, then right."""
        code_left = self.left.code(rho, nl)
        code_right = self.right.code(rho, nl)
        return code_left + code_right
    
    def __str__(self):
        return f"({self.left} ; {self.right})"


class ASSIGN(syntax.EXPRESSION):
    """Variable assignment."""
    def __init__(self, var_name, value):
        super().__init__()
        self.var_name = var_name
        self.value = value
    
    def code(self, rho, nl):
        """Assignment: evaluate value and store in variable."""
        # Find variable in environment
        for binding in rho:
            if len(binding) == 3 and binding[2] == self.var_name:
                offset = binding[0]
                var_nl = binding[1]
                depth = nl - var_nl
                code_value = self.value.code(rho, nl)
                return code_value + [store(offset, depth)]
        
        raise RuntimeError(f"Undefined variable: {self.var_name}")
    
    def __str__(self):
        return f"({self.var_name} := {self.value})"


class DO(syntax.EXPRESSION):
    """Do-while expression."""
    def __init__(self, body, condition):
        super().__init__()
        self.body = body
        self.condition = condition
    
    def code(self, rho, nl):
        """(K7) code (do {E} while B) ρ nl = 
            ℓ1: code(E) ρ nl; code(B) ρ nl; IFZERO ℓ2; GOTO ℓ1;
            ℓ2: NOP
            
        where ℓ1, ℓ2 are new labels
        """
        l1 = Label()
        l2 = Label()
        
        code_body = self.body.code(rho, nl)
        code_cond = self.condition.code(rho, nl)
        
        # Label for loop start
        if code_body:
            code_body[0].assigned_labels += [l1]
        else:
            code_body = [nop(assigned_label=l1)]
        
        return code_body + code_cond + [ifzero(l2)] + [goto(l1)] + [nop(assigned_label=l2)]
    
    def __str__(self):
        return f"do {{ {self.body} }} while {self.condition}"