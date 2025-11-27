# ------------------------------------------------------------
# triplalex.py
#
# tokenizer for the TRIPLA parser
# ------------------------------------------------------------
import ply.lex as lex


reserved = {
    'while' : 'WHILE',
    'do' : 'DO'
}

# List of token names. This is always required
tokens = [
    'CONST',
    'LBRACE', 'RBRACE'
]+list(reserved.values())

# Regular expression rules for simple tokens
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_WHILE = r'while'
t_DO = r'do'

# A regular expression rule with some action code
def t_CONST(t):
    r'\d+'
    t.value = int(t.value)
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
