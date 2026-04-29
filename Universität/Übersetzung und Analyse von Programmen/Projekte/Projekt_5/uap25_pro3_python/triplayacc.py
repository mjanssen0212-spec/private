
# Matthias Janßen
# 1871808
# ------------------------------------------------------------
# triplayacc.py
#
# Yacc-Grammatik der TRIPLA-Sprache
''' Hier eine initiale Grammatik
    E ->  while E do { E }
       | CONST

    CONST: Positive, ganze Zahlen = 0 | [1-9][0-9]*

'''

# Hinweis: Für LALR(1) wird Linksrekursion bevorzugt
# ------------------------------------------------------------

import ply.yacc as yacc
import compiler as ast

# Die Token-Map vom Lexer abrufen. Dies ist erforderlich.
from triplalex import tokens

precedence = (
    ('left', 'SEMI'),
    ('left', 'LOP'),
    ('nonassoc', 'EQOP', 'RELOP'),
    ('left', 'AOP'),
    ('right', 'ASSIGN'),
)
#E ->
def p_expression_let(p):
    'expression : LET dexpr IN expression'
    p[0] = ast.LET(p[2], p[4])

def p_expression_id(p):
    'expression : ID'
    p[0] = ast.VAR(p[1])

def p_expression_true(p):
    'expression : TRUE'
    p[0] = ast.BOOL(True)

def p_expression_false(p):
    'expression : FALSE'
    p[0] = ast.BOOL(False)

def p_expression_call(p):
    'expression : ID LPAREN aexpr RPAREN'
    p[0] = ast.CALL(p[1], p[3])

def p_expression_call_empty(p):
    'expression : ID LPAREN RPAREN'
    p[0] = ast.CALL(p[1], [])

def p_expression_aop(p):
    'expression : expression AOP expression'
    p[0] = ast.BINOP(p[2], p[1], p[3])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_const(p):
    'expression : CONST'
    p[0] = ast.CONST(p[1])

def p_expression_assign(p):
    'expression : ID ASSIGN expression'
    p[0] = ast.ASSIGN(p[1], p[3])

def p_expression_semi(p):
    'expression : expression SEMI expression'
    p[0] = ast.SEQ(p[1], p[3])

def p_expression_if(p):
    'expression : IF bexpr THEN expression ELSE expression'
    p[0] = ast.IF(p[2],p[4],p[6])

def p_expression_while(p):
    'expression : WHILE bexpr DO LBRACE expression RBRACE'
    p[0] = ast.WHILE(p[2],p[5])

#A ->
def p_aexpr_expression(p):
    'aexpr : expression'
    p[0] = [p[1]]

def p_aexpr_comma(p):
    'aexpr : aexpr COMMA expression'
    p[0] = p[1] + [p[3]]

#D ->
def p_dexpr_decl(p):
    'dexpr : ID LPAREN vexpr RPAREN LBRACE expression RBRACE'
    p[0] = [ast.DECL(p[1], p[3], p[6])]

def p_dexpr_empty_params(p):
    'dexpr : ID LPAREN RPAREN LBRACE expression RBRACE'
    p[0] = [ast.DECL(p[1], [], p[5])]

def p_dexpr_concat(p):
    'dexpr : dexpr dexpr'
    p[0] = p[1] + p[2]

#V ->
def p_vexpr_id(p):
    'vexpr : ID'
    p[0] = [ast.VAR(p[1])]

def p_vexpr_comma(p):
    'vexpr : vexpr COMMA vexpr'
    p[0] = p[1] + p[3]

#B ->
def p_bexpr_paren(p):
    'bexpr : LPAREN bexpr RPAREN'
    p[0] = p[2]

def p_bexpr_lop(p):
    'bexpr : bexpr LOP bexpr'
    p[0] = ast.BINOP(p[2], p[1], p[3])

def p_bexpr_relop(p):
    'bexpr : expression RELOP expression'
    p[0] = ast.BINOP(p[2], p[1], p[3])

def p_bexpr_true(p):
    'bexpr : TRUE'
    p[0] = ast.BOOL(True)

def p_bexpr_false(p):
    'bexpr : FALSE'
    p[0] = ast.BOOL(False)

def p_bexpr_eqop_bexpr(p):
    'bexpr : bexpr EQOP bexpr'
    p[0] = ast.BINOP(p[2], p[1], p[3])

def p_bexpr_eqop_expression(p):
    'bexpr : expression EQOP expression'
    p[0] = ast.BINOP(p[2], p[1], p[3])

#def p_empty(p):
#    'empty :'
#    pass

# Fehlerregel für Syntaxfehler
def p_error(p):
    print("Syntaxfehler in der Eingabe!")

# Den Parser erstellen
parser = yacc.yacc()  # debug=True
