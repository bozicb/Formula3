from ast_lexer import tokens                                    # This defines tokens for the parser. Even if not locally referenced it is important!!
from formula3.exceptions.exception import Formula3Exception
from formula3.exceptions.Formula3ParserException import Formula3ParserException
from formula3.ast_lexer import AST_Lexer
from formula3.ast_check import AST_Checker
import ply.yacc as yacc


import AST


###################################################
# Class AST_Parser 
###################################################

# Note: Due to some limitations of PLY, precedence MUST be declared at module level and not inside the class
# Attention: Add regular binary operators AFTER GT and LT (as they are used for sharp brackets as well!
precedence = (
#              ('nonassoc', 'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NEQ'), 
#              ('left', 'SEMICOLON'),            
#              ('left', 'ASSIGN'),            
#              ('left', 'AND', 'OR', 'XOR'),
#              ('left', 'PLUS', 'MINUS'),
#              ('left', 'TIMES', 'DIVIDE'),
              ('left', 'IF', 'OTHERWISE'), 
              ('left', 'GT'),
              ('right', 'POW'),
              ('right', 'UMINUS'),
            )


class AST_Parser:
    '''
    Parser for Formula3 expressions. Generates an AST for further 
    processing. 
    '''
        
    def __init__(self, debug=0, logger=None):
        ''' 
        Initialises the AST_Parser
        @param debug: Set debug=1 to enable the debug output of the PLY parser  
        '''
        self.debug = debug
        self.parser = yacc.yacc(debuglog=logger, errorlog = logger)
        self.checker = AST_Checker()
        
    def parse(self, expression):
        '''
        Parses a Formula3 expression and returns the AST
        @param expression: Formula3 expression
        @return: Abstract Syntax Tree  
        '''
        ast_lexer=AST_Lexer()
        result = self.parser.parse(expression, lexer=ast_lexer, debug=self.debug)
        if result==None:
            raise Formula3Exception("syntax error")        
        self.checker.verify(result)        # This will throw an exception when the AST is not plausible
        return result
    

###################################################
# Parser definitions
###################################################

def p_stmt(p):
    ''' 
    stmt :  ts_param_id_list pipe 
    '''
    paramList=p[1]
    generatorList=p[2]    
    p[0]={AST.TYPE: AST.STMT, "parameters": paramList, "generators": generatorList}


def p_pipe_serial(p):
    '''pipe : pipe SERPIPE generator''' # Real pipes.
    generatorList=p[1]
    newGenerator=p[3]
    generatorList.append(newGenerator)
    p[0]=generatorList

def p_pipe_simple(p):
    '''pipe : generator'''   # A pipe consisting of just one generator or the start of a recursion of pipes 
    generatorList=[p[1]]
    p[0]=generatorList

def p_generator_with_every(p):
    '''generator : generator every_phrase'''
    generator=p[1]
    generator["every"]=p[2]
    p[0]=generator


def p_generator(p):
    '''generator : STARTGEN expression_list ENDGEN'''
#    '''generator : LT expression_list GT'''
    p[0] = {AST.TYPE:'generator', "expressions":p[2], "every":None}

def p_ts_param_id_list(p):
    ''' ts_param_id_list : formal_parameter'''
    p[0] = p[1]



def p_ts_param_id_list_TS_PARAM_ID(p):
    ''' ts_param_id_list : ts_param_id_list formal_parameter'''
    oldList = p[1]
    new_entry=p[2]

    new_key=new_entry.keys()
    if len(new_key)<>1:
        raise Formula3Exception("internal error")

    new_key=new_key[0]
    
    if new_key in oldList:
        raise Formula3Exception("Formal Parameter " + new_key + " given twice")
    
    oldList.update(new_entry)
    p[0] = oldList


    
def p_formal_parameter_undefined(p):
    '''formal_parameter : TS_PARAM_ID'''
    id=p[1]
    result={id:None}
    p[0]=result
    
    
def p_formal_parameter_defined(p):
    '''formal_parameter : TS_PARAM_ID EQUALS STRING'''
    id=p[1]
    boundTo=p[3]
    result={id:boundTo}
    p[0]=result

#################################################
#def p_expression_list(p):
#    '''expression_list : expression'''
#    p[0]=p[1]


#####################################################################################
# precedence semicolon
def p_semicolon(p):
    'expression_list : expression_list SEMICOLON assign_expression'
    currentList=p[1]
    newExpression=p[3]
    currentList.append(newExpression)
    p[0]=currentList

#####################################################################################
def p_reduce_assign(p):
    'expression_list : assign_expression'
    p[0]=[p[1]]

#####################################################################################
# precedence assign
def p_assign(p):
    'assign_expression : if_expression ASSIGN TS_ID'
    p[0]=(p[1], p[3])

def p_prop_copy(p):
    'assign_expression : TS_ID PROPCOPY interval'
    tsid=p[1]
    regexp=p[2] # Still with the slashes 
    regexp=regexp.strip('/')
    interval=p[3]
    p[0]=({AST.TYPE: AST.TYPE_PROPCOPY, AST.ID:tsid, "REGEXP": regexp, "interval": interval}, None)

#####################################################################################
def p_reduce_if(p):
    'assign_expression : if_expression'
    p[0]=(p[1], None)

#####################################################################################
# precedence if 
def p_if(p):
    'if_expression : logic_expression IF if_expression OTHERWISE logic_expression'
    trueExpr =p[1]
    ifExpr   =p[3]
    otherExpr=p[5]
    p[0] = {AST.TYPE: 'IFOT', "operation": 'IF', "condition": ifExpr, "true": trueExpr, "false": otherExpr}  
    



#####################################################################################
def p_reduce_logic(p):
    'if_expression : logic_expression'
    p[0]=p[1]

#####################################################################################
# precedence logic 
def p_and(p):
    'logic_expression : logic_expression AND add_expression'
    p[0] = {AST.TYPE: 'BINOP', "operation": 'AND', "left": p[1], "right": p[3]}
   
def p_or(p):
    'logic_expression : logic_expression OR add_expression'
    p[0] = {AST.TYPE: 'BINOP', "operation": 'OR', "left": p[1], "right": p[3]}
   
def p_xor(p):
    'logic_expression : logic_expression XOR add_expression'
    p[0] = {AST.TYPE: 'BINOP', "operation": 'XOR', "left": p[1], "right": p[3]}

#####################################################################################
#def p_reduce_compare(p):
#    'logic_expression : compare_expression'
#    p[0]=p[1]


#####################################################################################
# precedence compare 
def p_gt(p):
    'logic_expression : add_expression GT add_expression'
    p[0] = {AST.TYPE: 'BINOP', "operation": 'GT', "left": p[1], "right": p[3]}
    
def p_lt(p):
    'logic_expression : add_expression LT add_expression'
    p[0] = {AST.TYPE: 'BINOP', "operation": 'LT', "left": p[1], "right": p[3]}
    
def p_gte(p):
    'logic_expression : add_expression GTE add_expression'
    p[0] = {AST.TYPE: 'BINOP', "operation": 'GTE', "left": p[1], "right": p[3]}
    
def p_lte(p):
    'logic_expression : add_expression LTE add_expression'
    p[0] = {AST.TYPE: 'BINOP', "operation": 'LTE', "left": p[1], "right": p[3]}
    

def p_eq(p):
    'logic_expression : add_expression EQ add_expression'
    p[0] = {AST.TYPE:'BINOP', "operation":'EQ', "left":p[1], "right":p[3]}
    
def p_neq(p):
    'logic_expression : add_expression NEQ add_expression'
    p[0] = {AST.TYPE: 'BINOP', "operation": 'NEQ', "left": p[1], "right": p[3]}
   

#####################################################################################
def p_reduce_add(p):
    'logic_expression : add_expression'
    p[0]=p[1]


#####################################################################################
# precedence add 
def p_plus(p):
    'add_expression : add_expression PLUS mult_expression'
    p[0] = {AST.TYPE:'BINOP', "operation":'ADD', "left":p[1], "right":p[3]}

def p_minus(p):
    'add_expression : add_expression MINUS mult_expression'
    p[0] = {AST.TYPE:'BINOP', "operation":'SUB', "left":p[1], "right":p[3]}
  


#####################################################################################
def p_reduce_mult(p):
    'add_expression : mult_expression'
    p[0]=p[1]


#####################################################################################
# precedence mult 
def p_div(p):
    'mult_expression : mult_expression DIVIDE expression'
    p[0] = {AST.TYPE:'BINOP', "operation":'DIV', "left":p[1], "right":p[3]}
    
def p_times(p):
    'mult_expression : mult_expression TIMES expression'
    p[0] = {AST.TYPE:'BINOP', "operation":'MUL', "left":p[1], "right":p[3]}



#####################################################################################
def p_reduce_pow(p):
    'mult_expression : expression'
    p[0]=p[1]

#####################################################################################
#Precedence level "pow"
def p_pow(p):
    'expression : expression POW expression'
    p[0] = {AST.TYPE:'BINOP', "operation":'POW', "left":p[1], "right":p[3]}
    

def p_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    expr=p[2]
    if isinstance(expr, (int, float)):   # If the negative can be computed here (as it is a literal), do it.
        p[0]=-1*expr
    else:                               # otherwise put it as a special operator into the AST.
        p[0]={AST.TYPE: "UMINUS", "operand":p[2]}

def p_num(p):
    'expression : number'
    p[0] = p[1]      

def p_string(p):
    'expression : STRING'
    p[0] = p[1]      
    
def p_ts(p):
    'expression : ts_slice'
    p[0] = p[1]
    

def p_brackets(p):
    'expression : ROUND_BRA if_expression ROUND_KET'
    p[0] = p[2]


###################################################################################################
# function calls
###################################################################################################
# Note: This code works but has been disabled to smooth the transition from the old "aggregate" functionality.
#def p_call(p):
#    '''expression : TS_ID ROUND_BRA argument_list ROUND_KET'''
#    p[0]={ARG.TYPE: ARG.TYPE_FUNCCALL, ARG.ARG_LIST: p[2]}
    

# Note: put in this code temporarilly that creates an aggregate  
def p_funccall(p):
    '''expression : TS_ID ROUND_BRA expression ROUND_KET'''

    func_name = p[1]
    arg_list  = (p[3],)
    p[0] = {AST.TYPE:AST.TYPE_FUNCCALL, "id":func_name, AST.ARG_LIST:arg_list}




#def p_arg_list(p):
#    '''argument_list : expression 
#                    | argument_list ',' expression                         
#    '''
#    if len(p)==2: # a simple expression
#        p[0]=[p]    # Make it a list
#    else:
#        p[0]=p[1]
#        p[0].append(p[3])
#    


###################################################################################################


def p_slice(p):
    '''ts_slice : property_access interval'''

    id      =p[1][0]
    property=p[1][1]
    aggregate=''
    interval=p[2]
    
    p[0] = {AST.TYPE:AST.TYPE_SLICE, AST.ID:id, "property":property, "interval":interval}






def p_number(p):
    '''number : FLOAT
              | INTEGER
    '''
    p[0] = p[1]
        
    
        
###################################################################################################


def p_property_access(p):
    ''' property_access : TS_ID
                        | TS_ID FUNC_OR_ACCESS
    '''
    ts_id=p[1]
    property_id=''
    if len(p)>2: # ID given
        property_id = p[2]

    p[0] = (ts_id, property_id)




def p_interval(p):
    '''interval : numeric_interval
                | logical_interval
                | time_interval
    '''
    p[0] = p[1]

def p_numeric_interval(p):       # [1]
    ''' numeric_interval : SQUARE_BRA INTEGER SQUARE_KET ''' 
    p[0] = ('NUMERIC', p[2])


def p_logical_interval_simple(p):       # [i]
    ''' logical_interval : SQUARE_BRA log_index_expression SQUARE_KET''' 
    offset=p[2]
    p[0] = {AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":offset}, "right":{AST.TYPE:AST.CLOSED, "offset":offset}}



def p_time_interval_simple(p):          # [t]
    ''' time_interval : bra time_index_expression ket'''
    leftType=p[1]
    if leftType==AST.OPEN:
        raise Formula3ParserException('Semantic error: No open intervals allowed with single argument "t" ', p.lineno, p.lexpos, p.value )
    rightType=p[1]
    if rightType==AST.OPEN:
        raise Formula3ParserException('Semantic error: No open intervals allowed with single argument "t" ', p.lineno, p.lexpos, p.value )
        
    p[0] = {AST.TYPE:AST.SLICE_TYPE_PHYSICAL, "left":{AST.TYPE:AST.CLOSED, "offset":p[2]}, "right":{AST.TYPE:AST.CLOSED, "offset":p[2]}}
    
    
    

def p_logical_interval_range(p):
    ''' logical_interval : SQUARE_BRA log_index_expression DOTDOT log_index_expression SQUARE_KET'''
    leftOffset=p[2]
    rightOffset=p[4]
        
    p[0] = {AST.TYPE:AST.SLICE_TYPE_LOGICAL, "left":{AST.TYPE:AST.CLOSED, "offset":leftOffset}, "right":{AST.TYPE:AST.CLOSED, "offset":rightOffset}}
        
    
def p_time_interval_range(p):
    ''' time_interval : bra time_index_expression DOTDOT time_index_expression ket'''
    leftType=p[1]
    leftOffset=p[2]
    rightOffset=p[4]
    rightType=p[5]
    result={AST.TYPE: AST.SLICE_TYPE_PHYSICAL, "left":{AST.TYPE:leftType, "offset":leftOffset}, "right":{AST.TYPE:rightType, "offset":rightOffset}}
    p[0] = result
    

def p_BRA(p):
    '''bra : SQUARE_BRA
           | SQUARE_KET
    '''
    bracket=p[1]
    if bracket=='[':
        p[0]=AST.CLOSED
    elif bracket==']':
        p[0]=AST.OPEN
    else:
        pass # Should throw a strange compiler error instead

def p_KET(p):
    '''ket : SQUARE_KET
           | SQUARE_BRA
    '''
    bracket=p[1]
    if bracket==']':
        p[0]=AST.CLOSED
    elif bracket=='[':
        p[0]=AST.OPEN
    else:
        pass # Should throw a strange compiler error instead

################################################################
    

def p_log_index_expression(p):          # i | i+1
    '''
    log_index_expression : I
                     | I PLUS INTEGER
                     | I MINUS INTEGER
    '''
    if len(p)==2 :
        p[0]= 0
        return
    
    if len(p)==4:
        op=p[2]
        sign= 1 if op=='+' else -1
        offset=p[3]
        offset*=sign
        p[0]=offset
        return
    # no error handling yet for cases where len(p) is unexpected 
    
def p_time_index_expression(p):         # t | t+1
    '''
    time_index_expression : T
                          | T PLUS INT_WITH_TIME
                          | T MINUS INT_WITH_TIME
    '''
    if len(p) == 2: # [t]
        p[0] = (0, 'min')
        return 
    
    if len(p) == 4: # [t+3 min]
        op = p[2]
        int_with_time=p[3]
        value=int_with_time[0]
        unit=int_with_time[1]
        if op == '-':
            value*=-1
        # else if what happens if neither is the case because the parser failed?
        p[0] = (value, unit)
        return
    # no error handling yet for cases where len(p) is unexpected
    
######################################################################################    
    
def p_every_phrase_not_aligned(p):
    '''
    every_phrase : EVERY INT_WITH_TIME
    '''
    
    int_with_time=p[2]
    value=int_with_time[0]
    unit =int_with_time[1]
    
    p[0] = (value, unit, 0, "hour") # It can (seriously) be discussed whether these defaults are useful
    # Note that the generated tuple is (should be) compatible with the "timevalue" routine collection
    # in the utils module 

def p_every_phrase_aligned(p):
    '''
    every_phrase : EVERY INT_WITH_TIME AT INT_WITH_TIME
    '''
    int_with_time_period=p[2]
    int_with_time_phase =p[4]
    
    value_period=int_with_time_period[0]
    unit_period =int_with_time_period[1]
    
    value_phase=int_with_time_phase[0]
    unit_phase =int_with_time_phase[1]
    
    
    p[0] = (value_period, unit_period, value_phase, unit_phase)


def p_none(p):
    'expression : NONE'
    p[0] = None

def p_error(p):
    if p != None:
        raise Formula3ParserException("Syntax error ", p.lineno, p.lexpos, p.value )
