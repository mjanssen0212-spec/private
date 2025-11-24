
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
    ('right', 'ASSIGN'),
    ('left', 'LOP'),
    ('nonassoc', 'RELOP'),
    ('left', 'AOP'),
)

def p_expression_const(p):
    'expression : CONST'
    p[0] = ast.CONST(p[1])

def p_expression_while(p):
    'expression : WHILE expression DO LBRACE expression RBRACE'
    p[0] = ast.WHILE(p[2],p[5])

def p_expression_if(p):
    'expression : IF expression THEN expression ELSE expression'
    p[0] = ast.IF(p[2],p[4],p[6])

def p_expression_id(p):
    'expression : ID'
    p[0] = ast.ID(p[1])

def p_expression_aop(p):
    'expression : expression AOP expression'
    p[0] = ast.AOP(p[1], p[3])

def p_expression_relop(p):
    'expression : expression RELOP expression'
    p[0] = ast.RELOP(p[1], p[3])

def p_expression_lop(p):
    'expression : expression LOP expression'
    p[0] = ast.LOP(p[1], p[3])

def p_expression_bool(p):
    'expression : BOOL'
    p[0] = ast.BOOL(p[1])

def  p_expression_comma(p):
    'expression : expression COMMA expression'
    p[0] = ast.COMMA(p[1], p[3])

def p_expression_semi(p):
    'expression : expression SEMI expression'
    p[0] = ast.SEMI(p[1], p[3])

def p_expression_let(p):
    'expression : LET expression IN expression'
    p[0] = ast.LET(p[2], p[3])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ast.PAREN(p[2])

def p_expression_brace(p):
    'expression : LBRACE expression RBRACE'
    p[0] = ast.BRACE(p[2])

def p_expression_assign(p):
    'expression : expression ASSIGN expression'
    p[0] = ast.ASSIGN(p[1], p[3])


# def p_decl_single(p):
#     'decls : ID LPAREN V RPAREN LBRACE expression RBRACE'
#     # create a DECL node via ast.DECL if present
#     p[0] = [ ast.DECL(p[1], p[3], p[6]) ]
#
# def p_decl_concat(p):
#     'decls : decls decls'
#     p[0] = p[1] + p[2]

#def p_empty(p):
#    'empty :'
#    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()  # debug=True
