
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

)

def p_expression_const(p):
    'expression : CONST'
    p[0] = ast.CONST(p[1])


def p_expression_while(p):
    'expression : WHILE expression DO LBRACE expression RBRACE'
    p[0] = ast.WHILE(p[2],p[5])

#def p_empty(p):
#    'empty :'
#    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()  # debug=True
