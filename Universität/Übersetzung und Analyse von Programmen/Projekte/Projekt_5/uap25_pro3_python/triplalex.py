#Matthias Janßen
#1871808

# ------------------------------------------------------------
# triplalex.py
#
# Tokenizer für den TRIPLA-Parser
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

# Liste der Token-Namen. Diese ist immer erforderlich.
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

# Reguläre Ausdrucksregeln für einfache Token
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
    # Auf reservierte Wörter prüfen
    t.type = reserved.get(t.value,'ID')
    return t

# Regel zur Verfolgung von Zeilennummern definieren
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ein String mit ignorierten Zeichen (Leerzeichen und Tabs)
t_ignore  = ' \t'

# Fehlerbehandlungsregel
def t_error(t):
    print("Ungültiges Zeichen '%s'" % t.value[0])
    t.lexer.skip(1)

# Den Lexer erstellen
lexer = lex.lex()
