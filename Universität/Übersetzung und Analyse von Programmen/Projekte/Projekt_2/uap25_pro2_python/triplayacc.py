#Matthias Janßen
#1871808

# ------------------------------------------------------------
# triplayacc.py
#
# Yacc grammar of the TRIPLA language
''' Here an initial grammar
    E ->  while E do { E }
       | CONST

    CONST: Positive, integer numbers = 0 | [1-9][0-9]*

'''

# Note: For LALR(1) left recursion is preferred
# ------------------------------------------------------------

import ply.yacc as yacc
import syntax as ast

# Get the token map from the lexer.  This is required.
from triplalex import tokens

precedence = (
    ('left', 'SEMI'),
    ('left', 'LOP'),
    ('nonassoc', 'EQOP', 'RELOP'),
    ('left', 'AOP'),
    ('right', 'ASSIGN'),
)

class Node:
    def __init__(self, type, children=None, leaf=None):
         self.type = type
         self.children = children if children else []
         self.leaf = leaf
    def __repr__(self):
         if self.leaf is not None and not self.children:
             return f"Node({self.type!r}, leaf={self.leaf!r})"
         if self.children:
             return f"Node({self.type!r}, children={self.children!r})"
         return f"Node({self.type!r})"

# -------------------------
# Expression (E) -> produce Node('expression', ...)
# -------------------------
def p_expression_let(p):
    'expression : LET dexpr IN expression'
    p[0] = Node('E', children=[p[1], p[2], p[3], p[4]])

def p_expression_id(p):
    'expression : ID'
    p[0] = Node('E', children=[Node('ID', leaf=p[1])])

def p_expression_call(p):
    'expression : ID LPAREN aexpr RPAREN'
    p[0] = Node('E', children=[Node('ID', leaf=p[1]), p[2], p[3], p[4]])

def p_expression_aop(p):
    'expression : expression AOP expression'
    # children: left, operator node, right
    p[0] = Node('E', children=[p[1], Node('AOP', leaf=p[2]), p[3]])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = Node('E', children=[p[1], p[2], p[3]])

def p_expression_const(p):
    'expression : CONST'
    p[0] = Node('E', children=[Node('CONST', leaf=p[1])])

def p_expression_assign(p):
    'expression : ID ASSIGN expression'
    p[0] = Node('E', children=[Node('ID', leaf=p[1]), Node('ASSIGN', leaf=p[2]), p[3]])

def p_expression_semi(p):
    'expression : expression SEMI expression'
    p[0] = Node('E', children=[p[1],p[2], p[3]])

def p_expression_if(p):
    'expression : IF bexpr THEN expression ELSE expression'
    p[0] = Node('E', children=[p[1], p[2], p[3], p[4], p[5], p[6]])

def p_expression_while(p):
    'expression : WHILE bexpr DO LBRACE expression RBRACE'
    p[0] = Node('E', children=[p[1], p[2], p[3], p[4], p[5], p[6]])

# -------------------------
# A : Argumentliste (calls) -> keep ARGS node as before
# -------------------------
def p_aexpr_expression(p):
    'aexpr : expression'
    p[0] = Node('A', children=[p[1]])

def p_aexpr_comma(p):
    'aexpr : aexpr COMMA expression'
    args_node = p[1]
    args_node.children.append(p[3])
    p[0] = args_node

# def p_aexpr_empty(p):
#     'aexpr : '
#     p[0] = Node('A', children=[])

# -------------------------
# D : Deklarationen -> dexpr node
# -------------------------
def p_dexpr_decl(p):
    'dexpr : ID LPAREN vexpr RPAREN LBRACE expression RBRACE'
    # children: ID, vexpr, expression
    p[0] = Node('D', children=[Node('ID', leaf=p[1]),p[2], p[3], p[4], p[5], p[6], p[7]])

def p_dexpr_concat(p):
    'dexpr : dexpr dexpr'
    # flatten children of both dexpr nodes
    left = p[1]
    right = p[2]
    p[0] = Node('D', children=left.children + right.children)

# -------------------------
# V : Parameterliste -> vexpr node
# -------------------------
def p_vexpr_id(p):
    'vexpr : ID'
    p[0] = Node('V', children=[Node('ID', leaf=p[1])])

def p_vexpr_comma(p):
    'vexpr : vexpr COMMA vexpr'
    p[0] = Node('V', children=[p[1], p[2], p[3]])

def p_vexpr_empty(p):
    'vexpr : '
    p[0] = Node('V', children=[])

# -------------------------
# B : Boolesche Ausdrücke -> bexpr node
# B -> (B) | BOOL | B LOP B | B EQOP B | E RELOP E | E EQOP E
# -------------------------
def p_bexpr_paren(p):
    'bexpr : LPAREN bexpr RPAREN'
    p[0] = Node('B', children=[p[1], p[2], p[3]])

def p_bexpr_bool(p):
    'bexpr : BOOL'
    p[0] = Node('B', children=[Node('BOOL', leaf=p[1])])

def p_bexpr_lop(p):
    'bexpr : bexpr LOP bexpr'
    p[0] = Node('B', children=[p[1], Node('LOP', leaf=p[2]), p[3]])

def p_bexpr_eqop_bexpr(p):
    'bexpr : bexpr EQOP bexpr'
    p[0] = Node('B', children=[p[1], Node('EQOP', leaf=p[2]), p[3]])

def p_bexpr_eqop_expression(p):
    'bexpr : expression EQOP expression'
    p[0] = Node('B', children=[p[1], Node('EQOP', leaf=p[2]), p[3]])

def p_bexpr_relop_expr(p):
    'bexpr : expression RELOP expression'
    p[0] = Node('B', children=[p[1], Node('RELOP', leaf=p[2]), p[3]])


#def p_empty(p):
#    'empty :'
#    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()  # debug=True
