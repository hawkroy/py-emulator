from ply import *

####################
#     Lexer        #
####################
keywords = (
        # configure primitive
        'SIMULATOR',
        'PARAMETER',
        'RESOURCE',
        'ENTITY',
        'METHOD',

        # runtime primitive
        'IF',
        'ELSE',
        'SET',
        'PRINT',
        'COMMAND'
        )

commands = (
        'REBOOT',
        'STOP_ENTITY',
        'HALT'
        )

tokens = keywords + (
        # configure primitive
        'NUMBER',
        'SCONST',
        'NAME',
        'LBRACE',
        'RBRACE',

        # runtime primitive
        'EQ'
        )

t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_EQ        = r'=='
t_SCONST    = r'\".*?\"'

t_ignore = ' \t\n\r'

keyword_map = {}
for r in keywords:
    keyword_map[r] = r

command_map = {}
for r in commands:
    command_map[r] = 'COMMAND'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[A-Za-z_][\w_]*'
    t.type = keyword_map.get(t.value, "NAME")
    if t.type == "NAME":
        t.type = command_map.get(t.value, "NAME")
    return t

def t_comment(t):
    r"[ ]*\043[^\n]*"   # \043 is '#'
    pass

def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()

#############################
#           Parser          #
#############################
def p_program(p):
    '''program : SIMULATOR LBRACE simulator RBRACE'''
    p[0] = p[3]

def p_simultar(p):
    '''simulator : simulator simulator_item
                 | simulator_item'''
    if len(p) == 2 and p[1]:
        p[0] = []
        p[0].append(p[1])
    elif len(p) == 3:
        p[0] = p[1]
        if p[2]:
            p[0].append(p[2])

def p_simultar_item(p):
    '''simulator_item : parameter
                      | resource 
                      | entity'''
    p[0] = p[1]         # return {LABEL, VAR}

def p_parameter(p):
    '''parameter : PARAMETER LBRACE param_list RBRACE'''
    p[0] = {}
    p[0]['PARAMETER'] = p[3]

def p_param_list(p):
    '''param_list : param_list param_item
                  | param_item'''
    if len(p) == 2 and p[1]:
        p[0] = []
        p[0].append(p[1])
    elif len(p) == 3:
        p[0] = p[1]
        if p[2]:
            p[0].append(p[2])

def p_param_item(p):
    '''param_item : NAME NUMBER '''
    p[0] = {}
    p[0][p[1]] = p[2]

def p_resource(p):
    '''resource : RESOURCE LBRACE resource_list RBRACE'''
    p[0] = {}
    p[0]['RESOURCE'] = p[3]

def p_resource_list(p):
    '''resource_list : resource_list resource_item
                     | resource_item'''
    if len(p) == 2 and p[1]:
        p[0] = []
        p[0].append(p[1])
    elif len(p) == 3:
        p[0] = p[1]
        if p[2]:
            p[0].append(p[2])

def p_resource_item(p):
    '''resource_item : NAME NUMBER '''
    p[0] = {}
    p[0][p[1]] = p[2]

def p_entity(p):
    '''entity : ENTITY SCONST LBRACE entity_body RBRACE'''
    p[0] = {}
    p[0]['ENTITY'] = [p[2], p[4]]       # {'ENTITY', [{name, code}]}

def p_entity_body(p):
    '''entity_body : METHOD LBRACE code_sequence RBRACE'''
    p[0] = p[3]

def p_sequence(p):
    '''code_sequence : code_sequence statement
                     | statement'''
    if len(p) == 2 and p[1]:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1]
        if p[2]:
            p[0] += p[2]

def p_set(p):
    '''statement : SET expr expr '''
    p[0] = [['SET', p[2], p[3]]]

def p_cmd(p):
    '''statement : COMMAND '''
    p[0] = [['COMMAND', p[1]]]

def p_print(p):
    '''statement : PRINT SCONST '''
    p[0] = [['PRINT', p[2][1:-1]]]

def p_if_statement_1(p):
    '''statement : IF condition LBRACE code_sequence RBRACE '''
    p[0] = []
    p[0].append(['CONDITION', p[2], 1, len(p[4])+1, 1])       #['CONDITION', condition, if-offset, else-offset, if-end-offset]
    p[0] += p[4]

def p_if_statement_2(p):
    '''statement : IF condition LBRACE code_sequence RBRACE ELSE LBRACE code_sequence RBRACE '''
    p[0] = []
    p[0].append(['CONDITION', p[2], 1, len(p[4])+1, len(p[8])+1])
    p[0] += p[4]
    p[0] += p[8]

def p_condition(p):
    '''condition : expr EQ expr'''
    p[0] = [p[2], p[1], p[3]]

def p_number(p):
    '''expr : NUMBER'''
    p[0] = int(p[1])

def p_name(p):
    '''expr : NAME'''
    p[0] = p[1]

bparser = yacc.yacc()

def parse(data, debug=0):
    bparser.error = 0
    p = bparser.parse(data, debug=debug)
    if bparser.error:
        return None
    return p
