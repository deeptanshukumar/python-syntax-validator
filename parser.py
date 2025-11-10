import ply.yacc as yacc
from parser import tokens, lexer

# 1. Precedence Rules
precedence = (
    ('nonassoc', 'IF'),
    ('nonassoc', 'ELSE'),
)

start = 'statement'

# 2. Grammar Rules
def p_empty(p):
    'empty :'
    p[0] = None


def p_statement(p):
    '''statement : func_def
                 | assignment_stmt
                 | conditional_stmt
                 | loop_stmt'''
    p[0] = p[1]


def p_func_def(p):
    '''func_def : DEF ID LPAREN arg_list RPAREN COLON'''
    p[0] = ('FUNC_DEF', p[2], p[4])


def p_arg_list(p):
    '''arg_list : ID
                | ID COMMA arg_list
                | empty'''
    p[0] = p[1]


def p_assignment_stmt(p):
    '''assignment_stmt : ID EQUAL expression'''
    p[0] = ('ASSIGN', p[1], p[3])


def p_expression(p):
    '''expression : NUMBER
                  | list_content'''
    p[0] = p[1]


def p_list_content(p):
    '''list_content : LBRACKET list_items RBRACKET'''
    p[0] = ('LIST', p[2])


def p_list_items(p):
    '''list_items : NUMBER
                  | NUMBER COMMA list_items
                  | empty'''
    p[0] = p[1]


def p_condition(p):
    '''condition : ID GT NUMBER'''
    p[0] = ('COND', p[1], '>', p[3])


def p_suite(p):
    '''suite : statement
             | empty'''
    p[0] = p[1]


def p_conditional_stmt(p):
    '''conditional_stmt : IF condition COLON suite elif_list else_block'''
    p[0] = ('IF', p[2], p[4], p[5], p[6])


def p_elif_list(p):
    '''elif_list : elif_block elif_list
                 | empty'''
    p[0] = [p[1]] if p[1] else []


def p_elif_block(p):
    '''elif_block : ELIF condition COLON suite'''
    p[0] = ('ELIF', p[2], p[4])


def p_else_block(p):
    '''else_block : ELSE COLON suite %prec ELSE
                  | empty'''
    p[0] = ('ELSE', p[3]) if len(p) > 2 else None


def p_loop_stmt(p):
    '''loop_stmt : WHILE condition COLON suite'''
    p[0] = ('WHILE', p[2], p[4])


def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (type: {p.type})")
    else:
        print("Syntax error at EOF (Incomplete statement)")
    return None


# Build parser
parser = yacc.yacc(optimize=0)


# 3. Tests
if __name__ == '__main__':
    print("\nPython Syntax Validator (5 Constructs)\n")

    test_cases = [
        "def calculate(a, b):",
        "my_variable = 500",
        "if x > 10: my_var = 1 elif x > 0: y = 2 else: z = 3",
        "while count > 0: count = 1",
        "my_list = [1, 2, 3]",
        "empty_list = []",
        "def wrong_func(a, b)",
        "if 10 > 5: x = 1"
    ]

    for i, code in enumerate(test_cases):
        print(f"\n[Test Case {i+1}] Code: {code}")
        result = parser.parse(code, lexer=lexer)
        if result:
            print(" Valid:", result)
        else:
            print(" Invalid syntax")
