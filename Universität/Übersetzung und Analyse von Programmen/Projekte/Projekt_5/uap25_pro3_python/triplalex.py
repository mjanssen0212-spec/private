#Matthias Janßen
#1871808

# ------------------------------------------------------------
# triplalex.py
#
# tokenizer for the TRIPLA parser
# ------------------------------------------------------------
import ply.lex as lex


reserved = {
    'while' : 'WHILE',
    'do' : 'DO',

    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',

    'let' : 'LET',
    'in' : 'IN',
    
    'true': 'TRUE',
    'false': 'FALSE'
}

# List of token names. This is always required
tokens = [
    'CONST',
    'ID',
    'AOP',
    'RELOP',
    'LOP',
    'EQOP',
    'COMMA', 'SEMI',
    'LBRACE', 'RBRACE',
    'LPAREN', 'RPAREN',
    'ASSIGN'
]+list(reserved.values())

# Regular expression rules for simple tokens
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_RELOP = r'<=|>=|<|>'
t_LOP   = r'\|\||&&'
t_AOP   = r'\+|\-|\*|/'
t_EQOP  = r'==|!='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA   = r','
t_SEMI    = r';'
t_ASSIGN = r'='

def t_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    t.type = reserved.get(t.value,'ID')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
