import ply.lex as lex

# 1. Token Definitions
tokens = [
    'ID', 'NUMBER',
    'EQUAL', 'COLON', 'COMMA',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'GT'
]

# Reserved Keywords
reserved = {
    'def': 'DEF',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'while': 'WHILE'
}

tokens += list(reserved.values())

# 2. Regex Rules for Tokens
t_EQUAL = r'='
t_COLON = r':'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_GT = r'>'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters (spaces, tabs)
t_ignore = ' \t'

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)

# Build lexer
lexer = lex.lex(optimize=0)
