from formula3.ast_lexer import AST_Lexer 
import formula3.ast_parser as ast_parser
import formula3.AST as AST
import unittest
import ply.yacc as yacc

TS_A_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'A', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":0}, "right":{AST.TYPE:AST.CLOSED, "offset":0}}} # A[i]
TS_B_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'B', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":1}, "right":{AST.TYPE:AST.CLOSED, "offset":1}}} # B[i+1] 
TS_C_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'C', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":2}, "right":{AST.TYPE:AST.CLOSED, "offset":2}}} # C[i+2]
TS_D_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'D', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":-3}, "right":{AST.TYPE:AST.CLOSED, "offset":2}}} # D[i-3..i+2]
TS_F_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'F', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":0}, "right":{AST.TYPE:AST.CLOSED, "offset":0}}}
TS_G_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'G', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":0}, "right":{AST.TYPE:AST.CLOSED, "offset":2}}} # G[i..i+2] 
TS_H_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'H', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":0}, "right":{AST.TYPE:AST.CLOSED, "offset":0}}} # H[i]
TS_I_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'I', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":0}, "right":{AST.TYPE:AST.CLOSED, "offset":0}}} # I[i] 
TS_J_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'J', "property":'value', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":0}, "right":{AST.TYPE:AST.CLOSED, "offset":0}}} # J[i].value
TS_K_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'A', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":0}, "right":{AST.TYPE:AST.CLOSED, "offset":0}}}
TS_L_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'B', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":0}, "right":{AST.TYPE:AST.CLOSED, "offset":0}}}
TS_M_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'A', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":-1}, "right":{AST.TYPE:AST.CLOSED, "offset":0}}} # M[i-1..i]
TS_O_L = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'A', "property":'a:b', "interval":{AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":-1}, "right":{AST.TYPE:AST.CLOSED, "offset":0}}} # M[i-1..i].mean

TS_A_POO = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'A', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_PHYSICAL, "left":{AST.TYPE:AST.OPEN, "offset":(-1, 'min')}, "right":{AST.TYPE:AST.OPEN, "offset":(1, 'min')}}}
TS_A_POC = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'A', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_PHYSICAL, "left":{AST.TYPE:AST.OPEN, "offset":(-1, 'min')}, "right":{AST.TYPE:AST.CLOSED, "offset":(1, 'min')}}}
TS_A_PCO = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'A', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_PHYSICAL, "left":{AST.TYPE:AST.CLOSED, "offset":(-1, 'min')}, "right":{AST.TYPE:AST.OPEN, "offset":(1, 'min')}}}
TS_A_PCC = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'A', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_PHYSICAL, "left":{AST.TYPE:AST.CLOSED, "offset":(-1, 'min')}, "right":{AST.TYPE:AST.CLOSED, "offset":(1, 'min')}}}


TS_A_T = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'A', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_PHYSICAL, "left":{AST.TYPE:AST.CLOSED, "offset":(0, 'min')}, "right":{AST.TYPE:AST.CLOSED, "offset":(0, 'min')}}}           # A[t]
TS_B_T = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'B', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_PHYSICAL, "left":{AST.TYPE:AST.CLOSED, "offset":(-1, 'min')}, "right":{AST.TYPE:AST.CLOSED, "offset":(1, 'min')}}}          # B[t-1 min .. t+1 min]
TS_E_T = {AST.TYPE:AST.TYPE_SLICE, AST.ID:'E', "property":'', "interval":{AST.TYPE:AST.SLICE_TYPE_PHYSICAL, "left":{AST.TYPE:AST.CLOSED, "offset":(0, 'min')}, "right":{AST.TYPE:AST.CLOSED, "offset":(0, 'min')}}}


STRING_TESTS = { '@A << "Hello" >>'    : {AST.TYPE: AST.STMT, 'parameters': {'A':None}, 'generators': [{'every': None, 'expressions':[("Hello", None)], AST.TYPE: 'generator'}]},
            }

BOUND_PARAM_TESTS = {
                 '@A="XYZ" << "Hello" >>'    : {AST.TYPE: AST.STMT, 'generators': [{'every': None, 'expressions': [("Hello",None)], AST.TYPE: 'generator'}], 'parameters': {'A':'XYZ'}},
            }


LOGICAL_INDEX_TESTS = {
               '@A <<A[i]>>'        : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions": [(TS_A_L, None)], "every":None}] },
               '@B <<B[i+1]>>'      : {AST.TYPE: AST.STMT, "parameters": {'B':None}, "generators": [{AST.TYPE:'generator', "expressions": [(TS_B_L, None)], "every":None}] },
               '@C <<C[i+2]>>'      : {AST.TYPE: AST.STMT, "parameters": {'C':None}, "generators": [{AST.TYPE:'generator', "expressions": [(TS_C_L, None)], "every":None}] },
               '@D <<D[i-3..i+2]>>' : {AST.TYPE: AST.STMT, "parameters": {'D':None}, "generators": [{AST.TYPE:'generator', "expressions": [(TS_D_L, None)], "every":None}] },
              }

INTERVAL_TESTS = {
               '@A <<A ]t - 1 min .. t + 1 min[ >>'        : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions": [(TS_A_POO, None)], "every":None}] },
               '@A <<A [t - 1 min .. t + 1 min[ >>'        : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions": [(TS_A_PCO, None)], "every":None}] },
               '@A <<A ]t - 1 min .. t + 1 min] >>'        : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions": [(TS_A_POC, None)], "every":None}] },
               '@A <<A [t - 1 min .. t + 1 min] >>'        : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions": [(TS_A_PCC, None)], "every":None}] },
              }


TIME_INDEX_TESTS = {
                '@A <<A[t]>>'                : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[(TS_A_T, None)], "every": None}]},
                '@B <<B[t-1 min..t+1 min]>>' : {AST.TYPE: AST.STMT, "parameters": {'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[(TS_B_T, None)], "every":None}]},
                    }

UMINUS_TESTS = {
                '@A <<-A[i]>>'   : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'UMINUS', "operand":TS_A_L}, None)], "every":None}]},
                '@A <<-1*A[i]>>' : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation": "MUL", "right":TS_A_L, "left":-1}, None)], "every":None}]},
               }

ADD_TESTS = {
             '@A << A[i] + 1337 >>'             : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'ADD', "left":TS_A_L, "right":1337},None)], "every":None}]},
             '@A @B << A[i] + B[i+1] >>'        : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'ADD', "left":TS_A_L, "right":TS_B_L},None)], "every":None}]},
             '@A @B << A[i] + B[i+1] + 1337>>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'ADD', "left":{AST.TYPE:'BINOP', "operation":'ADD', "left":TS_A_L, "right":TS_B_L}, "right":1337},None)], "every":None}]},
             }

LOGIC_TESTS = {
             '@A << A[i] and 1337 >>'           : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'AND', "left":TS_A_L, "right":1337},None)], "every":None}]},
             '@A << A[i] AND 1337 >>'           : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'AND', "left":TS_A_L, "right":1337},None)], "every":None}]},
             '@A << A[i] or 1337 >>'            : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'OR',  "left":TS_A_L, "right":1337},None)], "every":None}]},
             '@A << A[i] xor 1337 >>'           : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'XOR', "left":TS_A_L, "right":1337},None)], "every":None}]},
             }

SUB_TESTS = {
             '@A << A[i] - 1.337 >>'             : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'SUB', "left":TS_A_L, "right":1.337}, None)], "every":None}]},
             '@A @B << A[i] - B[i+1] >>'         : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'SUB', "left":TS_A_L, "right":TS_B_L}, None)], "every":None}]},
             '@A @B << A[i] - B[i+1] - 1.337>>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'SUB', "left":{AST.TYPE:'BINOP', "operation":'SUB', "left":TS_A_L, "right":TS_B_L}, "right":1.337}, None)], "every":None}]}
             }

MUL_TESTS = {
             '@A << A[i] * 1337 >>'                         : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'MUL', "left":TS_A_L, "right":1337}, None)], "every":None}]},
             '@A @B << A[i] * B[i+1] >>'                    : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'MUL', "left":TS_A_L, "right":TS_B_L}, None)], "every":None}]},
             '@A @B << A[i] * B[i+1] - 1337>>'              : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'SUB', "left":{AST.TYPE:'BINOP', "operation":'MUL', "left":TS_A_L, "right":TS_B_L}, "right":1337}, None)], "every":None}]},
             '@A @B << A[i] * (B[i+1] - 1337)>>'            : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'MUL', "left":TS_A_L, "right":{AST.TYPE:'BINOP', "operation":'SUB', "left":TS_B_L, "right":1337} }, None)], "every":None}]},
             '@A @B @C << A[i] * B[i+1] - 1337 * C[i+2]>>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None, 'C':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'SUB', "left":{AST.TYPE:'BINOP', "operation":'MUL', "left":TS_A_L, "right":TS_B_L}, "right":{AST.TYPE:'BINOP', "operation":'MUL', "left":1337, "right":TS_C_L}}, None)], "every":None}]},
             } 

DIV_TESTS = {
             '@A << A[i] / 1337 >>'             : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'DIV', "left":TS_A_L, "right":1337},None)], "every":None}]},
             '@A << 1337 / A[i] >>'             : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'DIV', "left":1337, "right":TS_A_L},None)], "every":None}]},
             '@A @B << A[i] / B[i+1] >>'        : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'DIV', "left":TS_A_L, "right":TS_B_L},None)], "every":None}]},
             '@A @B << A[i] * B[i+1] / 1337>>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'DIV', "left":{AST.TYPE:'BINOP', "operation":'MUL', "left":TS_A_L, "right":TS_B_L}, "right":1337},None)], "every":None}]},
             '@A @B @C << A[i] / B[i+1] * 1337 / C[i+2]>>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None, 'C':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'DIV', "left":{AST.TYPE:'BINOP', "operation":'MUL', "left":{AST.TYPE:'BINOP', "operation":'DIV', "left":TS_A_L, "right":TS_B_L}, "right":1337}, "right":TS_C_L},None)], "every":None}]},
             } 


PRECEDENCE_TESTS = {
             '@A << A[i] / ( 1337 * 2)  >>'           : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'DIV', "left":TS_A_L, "right":{AST.TYPE:'BINOP', "operation":'MUL', "left":1337, "right":2}}, None)], "every": None}]},
             '@A << A[i] / ( 1337 + 2)  >>'           : {AST.TYPE:AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'DIV', "left":TS_A_L, "right":{AST.TYPE:'BINOP', "operation":'ADD', "left":1337, "right":2}}, None)], "every": None}]},
             '@A << A[i] / (( 1337 + 2) - 10)  >>'    : {AST.TYPE:AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'DIV', "left":TS_A_L, "right":{AST.TYPE:'BINOP', "operation":'SUB', "left":{AST.TYPE:'BINOP', "operation":'ADD', "left":1337, "right":2}, "right":10}}, None)], "every": None}]}
             } 

POW_TESTS = {
             '@A << A[i] ** 1337 >>'             : {AST.TYPE: AST.STMT, "parameters": {'A':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'POW', "left":TS_A_L, "right":1337}, None)], "every":None}]},
             '@A @B << A[i] ** B[i+1] >>'        : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'POW', "left":TS_A_L, "right":TS_B_L}, None)], "every": None}]},
             '@A @B << A[i] * B[i+1] ** 1337>>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'MUL', "left":TS_A_L, "right":{AST.TYPE:'BINOP', "operation":'POW',  "left":TS_B_L, "right":1337}}, None)], "every": None}]}
             } 


EVERY_TESTS = {
               '@E <<mean(E[t])>> every 1 min' : {AST.TYPE: AST.STMT, "parameters":{'E':None}, "generators":[{AST.TYPE:'generator', "expressions":[({AST.TYPE: AST.TYPE_FUNCCALL, AST.ID:"mean", AST.ARG_LIST:((TS_E_T),)},None)], "every":(1, 'min', 0, 'hour') }]},
              }

PROPERTY_TESTS = {
               '@J << mean(J.value[i]) >>' : {AST.TYPE: AST.STMT, "parameters": {'J':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:AST.TYPE_FUNCCALL, AST.ID:"mean", AST.ARG_LIST:(TS_J_L, )},None)], "every": None}]},
              }

PROP_COPY_TESTS = {
               '@J << mean(J.value[i]); J//.*//[i] >>' : {
                                AST.TYPE: AST.STMT, 
                                "parameters": {
                                    'J':None}, 
                                "generators": [
                                    {AST.TYPE:'generator', 
                                     "expressions":
                                         [({AST.TYPE: AST.TYPE_FUNCCALL, AST.ID:"mean", AST.ARG_LIST:(TS_J_L,)}, None),
                                          ({AST.TYPE: "PROPCOPY", AST.ID:"J", "REGEXP":".*", "interval": {'type': 'LOGICAL', 'left': {'type': 'CLOSED', 'offset': 0}, 'right': {'type': 'CLOSED', 'offset': 0}}}, None)
                                         ], 
                                      "every": None
                                    }
                                ]
                            },
               '@J << J//.*//[i] >>' : {
                                AST.TYPE: AST.STMT, 
                                "parameters": {
                                    'J':None}, 
                                "generators": [
                                    {AST.TYPE:'generator', 
                                     "expressions":
                                         [
                                          ({AST.TYPE: "PROPCOPY", AST.ID:"J", "REGEXP":".*", "interval": {'type': 'LOGICAL', 'left': {'type': 'CLOSED', 'offset': 0}, 'right': {'type': 'CLOSED', 'offset': 0}}}, None)
                                         ], 
                                      "every": None
                                    }
                                ]
                            },
              }


IF_TESTS = { 
            '@A << A[i] if (A[i] > 0.01) otherwise 0 >>' : {'generators': [{'every': None, 'expressions': [({'true': TS_A_L, 'operation': 'IF', 'condition': {'operation': 'GT', 'left': TS_A_L, AST.TYPE: 'BINOP', 'right': 0.01}, 'false': 0, AST.TYPE: 'IFOT'},None)], AST.TYPE: 'generator'}], 'parameters': {'A':None}, AST.TYPE: AST.STMT},
            '@A << A[i] if (1) otherwise None>>'  : {'generators': [{'every': None, 'expressions': [({'true': TS_A_L, 'operation': 'IF', 'condition': 1, 'false': None, AST.TYPE: 'IFOT'},None)], AST.TYPE: 'generator'}], 'parameters': {'A':None}, AST.TYPE: AST.STMT},
            }

COMPARE_TESTS = { 
            '@A @B << (A[i] > B[i]) >>' : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'GT', "left":TS_K_L, "right":TS_L_L},None)], "every": None}]},
            '@A @B << A[i] < B[i] >>'   : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'LT', "left":TS_K_L, "right":TS_L_L},None)], "every": None}]},
            '@A @B << A[i] >= B[i] >>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'GTE', "left":TS_K_L, "right":TS_L_L},None)], "every": None}]},
            '@A @B << A[i] <= B[i] >>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'LTE', "left":TS_K_L, "right":TS_L_L},None)], "every": None}]},
            '@A @B << A[i] == B[i] >>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'EQ', "left":TS_K_L, "right":TS_L_L},None)], "every": None}]},
            '@A @B << A[i] != B[i] >>'  : {AST.TYPE: AST.STMT, "parameters": {'A':None, 'B':None}, "generators": [{AST.TYPE:'generator', "expressions":[({AST.TYPE:'BINOP', "operation":'NEQ', "left":TS_K_L, "right":TS_L_L},None)], "every": None}]},
            }

ASSIGNMENT_TESTS = {
                    '@A << mean(A[i-1 .. i]) => mean >>' : {'generators': [{'every': None, 'expressions': [({AST.TYPE:AST.TYPE_FUNCCALL, AST.ID:"mean", AST.ARG_LIST:(TS_M_L,)}, 'mean')], AST.TYPE: 'generator'}], 'parameters': {'A': None}, AST.TYPE: AST.STMT},
            }

COLON_TESTS = {
                    '@A << a:mean(A.a:b[i-1 .. i]) => b:mean >>' : {'generators': [{'every': None, 'expressions': [({AST.TYPE:AST.TYPE_FUNCCALL, AST.ID:"a:mean", AST.ARG_LIST:(TS_O_L,)}, 'b:mean')], AST.TYPE: 'generator'}], 'parameters': {'A': None}, AST.TYPE: AST.STMT},
            }


FUNC_TESTS = {
                    '@A << log(3) >>': {AST.TYPE: AST.STMT, AST.PARAMETERS: ('A', None), 'generators': [{'every': None, 'expressions': [({AST.TYPE:AST.TYPE_FUNCCALL, AST.ID:"log", AST.ARG_LIST: (3,)}, None)], AST.TYPE: 'generator'}], 'parameters': {'A': None}},
             }


PIPE_TESTS = {
                    '@A << log(A[i]) >> | << A[i] >>' : {AST.TYPE: AST.STMT, 
                                                    'parameters': {'A': None},
                                                    "generators":[
                                                                  {'every': None, 'expressions': [({AST.TYPE:AST.TYPE_FUNCCALL, AST.ID:"log", AST.ARG_LIST:(TS_A_L, )}, None)], AST.TYPE: 'generator'}, 
                                                                  {'every': None, 'expressions': [(TS_A_L, None)], AST.TYPE: 'generator'}
                                                                 ]},
              }

SEMICOLON_TESTS = {
                    '@A << 1 => one; "ABC" => abc >>' : {AST.TYPE: AST.STMT,
                                                                  'parameters' : {'A' : None},
                                                                  'generators':
                                                                      [
                                                                          {
                                                                           AST.TYPE: 'generator',
                                                                           'every': None,
                                                                           'expressions': [(1, 'one'),("ABC", 'abc')]
                                                                          } 
                                                                      ]  
                                                                 }, # end of root
                   }
COUNT_TESTS = {
                    '@A << count(A[i]) >>' :{'generators': [{'every': None, 'expressions': [({AST.TYPE:AST.TYPE_FUNCCALL, AST.ID:"count", AST.ARG_LIST:({'interval': {'left': {'offset': 0, AST.TYPE: AST.CLOSED}, AST.TYPE: AST.SLICE_TYPE_LOGICAL, 'right': {'offset': 0, AST.TYPE: AST.CLOSED}}, 'id': 'A', AST.TYPE: AST.TYPE_SLICE, 'property': ''},)},None)], AST.TYPE: 'generator'}], 'parameters': {'A': None}, AST.TYPE: AST.STMT},
               }

NONE_TESTS = {
                    '@A << A[i] + None >>' : {'generators': [{'every': None, 'expressions': [({'operation': 'ADD', 'left': {'interval': {'left': {'offset': 0, AST.TYPE: AST.CLOSED}, AST.TYPE: AST.SLICE_TYPE_LOGICAL, 'right': {'offset': 0, AST.TYPE: AST.CLOSED}}, 'id': 'A', AST.TYPE: AST.TYPE_SLICE, 'property': ''}, AST.TYPE: 'BINOP', 'right': None}, None)], AST.TYPE: 'generator'}], 'parameters': {'A': None}, AST.TYPE: AST.STMT},
              }

COMMENT_TESTS = {
                    '@A << A[i] /* Dies ist ein Kommentar */ >>' : {'generators': [{'every': None, 'expressions': [({'interval': {'left': {'offset': 0, AST.TYPE: AST.CLOSED}, AST.TYPE: AST.SLICE_TYPE_LOGICAL, 'right': {'offset': 0, AST.TYPE: AST.CLOSED}}, 'id': 'A', AST.TYPE: AST.TYPE_SLICE, 'property': ''},None)], AST.TYPE: 'generator'}], 'parameters': {'A': None}, AST.TYPE: AST.STMT},
              }


class TestAST(unittest.TestCase):

    def compareTuple(self, expected, result):
        pass

    def compareResult(self, expected, result, path=[]):
        
        if result==None and expected!=None:
            self.fail("the result on path %s is None, expected %s" % (" / ".join(path), expected))
        
        if isinstance(expected, dict):
            for key, valueExpected in expected.items():
                if not key in result:
                    self.fail("expected key %s not in result in path %s" % (key, " / ".join(path) ))
                valueResult=result[key]
                newPath=path[:]
                newPath.append(key)
                self.compareResult(valueExpected, valueResult, newPath)
            
        if isinstance(expected, (list, tuple)):
            if len(expected)!=len(result):
                self.fail("list/tuple has different size (expected %d / result %d) at path %s" % (len(expected), len(result), "/".join(path) ) )
            for i, valueExpected in enumerate(expected):
                valueResult=result[i]
                newPath=path[:]
                newPath.append(str(i))
                self.compareResult(valueExpected, valueResult, newPath)
        
        if expected!=result:
            self.fail("value for path %s: \nexpected :%s,\nresult   :%s" % (" / ".join(path), expected, result) )
            
        return
    

    def runTest(self, testcases, enableDebug):
        for expression, expected in testcases.items():      
            print ('Testing expression: ',expression)      
            lexer_ast=AST_Lexer()
            parser_ast = yacc.yacc(module=ast_parser, write_tables=enableDebug, debug=enableDebug)
            result=parser_ast.parse(expression, debug=enableDebug)
            if enableDebug:
                print "expected", expected
                print "result  ", result
            self.compareResult(expected, result)
    
    def testStrings(self):          self.runTest(STRING_TESTS, 0)
    def testBoundParameter(self):   self.runTest(BOUND_PARAM_TESTS, 0)
    def testLOGICAL_INDEX(self):    self.runTest(LOGICAL_INDEX_TESTS, 0)   
    def testTIME_INDEX(self):       self.runTest(TIME_INDEX_TESTS, 0)
    def testINTERVAL(self):         self.runTest(INTERVAL_TESTS, 0)
    def testUMINUS(self):           self.runTest(UMINUS_TESTS, 0)
    def testADD(self):              self.runTest(ADD_TESTS, 0)
    def testLOGIC(self):            self.runTest(LOGIC_TESTS, 0)
    def testSUB(self):              self.runTest(SUB_TESTS, 0)
    def testMUL(self):              self.runTest(MUL_TESTS, 0)
    def testDIV(self):              self.runTest(DIV_TESTS, 0)
    def testPOW(self):              self.runTest(POW_TESTS, 0)
    def testPrecedence(self):       self.runTest(PRECEDENCE_TESTS, 0)
    def testEVERY(self):            self.runTest(EVERY_TESTS, 0)
    def testPROPERTY(self):         self.runTest(PROPERTY_TESTS, 0)
    def testPROPCOPY(self):         self.runTest(PROP_COPY_TESTS, 0)
    def testCOMPARE(self):          self.runTest(COMPARE_TESTS, 0)
    def testIF(self):               self.runTest(IF_TESTS, 0)
    def testASSIGN(self):           self.runTest(ASSIGNMENT_TESTS, 0)
    def testColon(self):            self.runTest(COLON_TESTS, 0)         # Test whether id's containing a ':' work correctly
    def testFUNC(self):             self.runTest(FUNC_TESTS, 1)
    def testPIPE(self):             self.runTest(PIPE_TESTS, 0)
    def testSEMICOLON(self):        self.runTest(SEMICOLON_TESTS, 0)
    def testCOUNT(self):            self.runTest(COUNT_TESTS, 0)
    def testNONE(self):             self.runTest(NONE_TESTS, 0)
    def testCOMMENT(self):          self.runTest(COMMENT_TESTS, 0)
        

 
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
