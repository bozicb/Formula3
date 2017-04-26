import ply.lex as lex
from ply.lex import TOKEN
from formula3.exceptions.exception import Formula3Exception 
from formula3.exceptions.Formula3LexerException import Formula3LexerException

import re

###################################################
# tokens is part of the interface to the parser
################################################### 
tokens=('NONE', 'STARTGEN', 'ENDGEN', 'LT', 'GT', 'SQUARE_BRA', 'SQUARE_KET', 'I', 'T',
        'IF', 'OTHERWISE', 'ASSIGN',
        'FLOAT', 'INTEGER', 'STRING', 'TS_PARAM_ID', 'TS_ID',  
        'AND', 'OR', 'XOR', 'PLUS','MINUS', 'TIMES', 'DIVIDE', 'POW', 'EQUALS',
        'LTE', 'GTE', 'EQ', 'NEQ', 'SEMICOLON',
        'ROUND_BRA','ROUND_KET', 'EVERY', 'FUNC_OR_ACCESS', 
        'DOTDOT', 'AT', 'SERPIPE', 'PROPCOPY', 'INT_WITH_TIME')
###################################################
# Token definitions
###################################################

identifier = r'(\w|[:])+'
ts_formal_param=r'@'+identifier
func_or_access = r'\.'+identifier
ts_param = identifier
                            

def AST_Lexer(**kwargs):
    
    ###################################################
    # Lexer definitions
    ###################################################
    
    # Note: Due to the PLY flexer documentation the rules are checked in the following sequence:
    # 1. All tokens defined by functions are added in the same order as they appear in the lexer file.
    # 2. Tokens defined by strings are added next by sorting them in order of decreasing regular expression length (longer expressions are added first).
    # Thus the order of the following definitions might be crucial. Don't change it unless you know what you are doing
    
    
    literals = "[]t"
    
    
    ###################################################
    # States
    ###################################################
    # We use states to read data within quotes differently
    states = (
       ('DQUOTE','exclusive'),
       ('DCOMMENT','exclusive'),
    )

    
    ######################################
    # Ruleset for "initial" goes here    #
    ######################################
    
    t_ignore  = ' \t\n\r'
    
    def t_error(t):
        raise Formula3LexerException("unexpected character", t.lineno, t.lexpos, t.value)
    
    def t_STARTGEN(t):
        r'<<'
        return t

    def t_ENDGEN(t):
        r'>>'
        return t

    def t_LT(t):
        r'<(?!=)'
        return t
    
    def t_GT(t):
        r'>(?!=)'
        return t    
    
    def t_EVERY(t):
        r'every'
        return t
    
    def t_IF(t):
        r'if'
        return t
    
    def t_OTHERWISE(t):
        r'otherwise'
        return t

    def t_AND(t):
        r'(?i)and'  # ok, ok. This is inconsequent. Either all keywords match upper AND lower or none. But let's keep this in as a reminder how to do it. 
        return t
    
    def t_OR(t):
        r'or'
        return t

    def t_XOR(t):
        r'xor'
        return t

    def t_DOTDOT(t):
        r'\.\.'
        return t
    
    def t_AT(t):
        r'@\s'
        return t
    
    def t_NONE(t):
        r'None'
        return t

    @TOKEN(ts_formal_param)
    def t_TS_PARAM_ID(t):
        t.value = t.value[1:]
        return t
    
    @TOKEN(func_or_access)
    def t_FUNC_OR_ACCESS(t):
        # TODO: This can be simplified now to an ID preceded by a DOT in the parser
        t.value = t.value[1:]
        return t
    
    def t_FLOAT(t):
        r'\d+\.\d+([eE][+-]?\d+)?'
        try:
            t.value = float(t.value)
        except ValueError:
            print("Not a valid float %s" % t.value)
            t.value = 0
        return t


    def t_INT_WITH_TIME(t): 
        # A variant followed by a timely unit. This is parsed as one unit to avoid problems with one of the 
        # time units occuring elsewhere as a name of a function. This is especially a problem with the word "min" as it also denotes the minimum operator.
        r'(\d+)\ *(ms|secs|sec|mins|min|hours|hour|days|day|weeks|week)' # An int, followed by zero or more spaces and them one of the mentioned keywords.
        
        matchedString=t.value
        pattern=t_INT_WITH_TIME.__doc__
        matcher=re.match(pattern, matchedString, 0)
        groups = matcher.groups()
        value_string=groups[0]
        unit_string=groups[1]
        
        
        try:
            value = int(value_string)
        except ValueError:
            print("Integer value too large %s" % t.value)
            value = 0

        t.value = (value, unit_string) 
        return t


        
    def t_INTEGER(t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        return t
 
    @TOKEN(ts_param)
    def t_TS_ID(t):
        if t.value=='t':    # Note: t and n are reserved words    
            t.type='T'
        if t.value=='i':
            t.type='I'
        return t
    
    def t_string(t):
        r'\"'
        t.lexer.begin('DQUOTE')

    def t_comment(t):
        r'/\*'
        t.lexer.begin('DCOMMENT')
        

    t_SQUARE_BRA= r'\['
    t_SQUARE_KET= r'\]' 
    t_PLUS      = r'\+'
    t_MINUS     = r'-'
    t_POW       = r'\*\*'
    t_TIMES     = r'\*'
    t_DIVIDE    = r'/'
    t_GTE       = r'>='
    t_LTE       = r'<='    
    t_EQ        = r'=='
    t_NEQ       = r'!='
    t_ROUND_BRA = r'\('
    t_ROUND_KET = r'\)'
    t_ASSIGN    = r'=>'
    t_EQUALS    = r'=(?!>|=)'
    t_SERPIPE   = r'\|'
    t_SEMICOLON = r';'
    t_PROPCOPY  = r'//.*?//'
    

    def p_error(p):
        print "Syntax error at '%s'" % p.value

    #########################################################
    #    Rules for state d_quote                            #
    #    This state is entered, when a quote is seen        #
    #    i.e. when the lexer sees the beginning of a string #
    #    It is left when the lexer sees another quote       #
    #########################################################
    
    t_DQUOTE_ignore=""
    
    def t_DQUOTE_error(t):
        raise Formula3LexerException("unexpected character", t.lexpos, t.lineno, t.value)

    
    def t_DQUOTE_STRING(t):
        r'.*?\"'  # Everything till the NEXT double quote (but not further)
        t.lexer.begin('INITIAL')
        t.value=t.value[:-1]    # Up to now the trailing quote is still in value. Remove it
        return t


    #########################################################
    #    Rules for state d_comment                          #
    #    This state is entered, when a "/*" is seen         #
    #    i.e. when the lexer sees the beginning of a comment#
    #    It is left when the lexer sees a "*/"              #
    #########################################################
    
    t_DCOMMENT_ignore=""
    
    def t_DCOMMENT_error(t):
        raise Formula3LexerException("unexpected character", t.lexpos, t.lineno, t.value)

    
    def t_DCOMMENT_STRING(t):
        r'.*?\*/'  # Everything till the "*/" (but not further)
        t.lexer.begin('INITIAL')
        # Note that this rule returns nothing thus discarding the read comment



            
    return lex.lex(**kwargs)

if __name__ == "__main__":  # A small test whether this module is formally correct
    lexer = AST_Lexer() 
