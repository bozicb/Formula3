import AST

from formula3.exceptions.exception import Formula3Exception

class verify_exception():
    def __init__(self, str):
        self.text=str

class AST_Checker(object):
    '''
    Verifies the semantic integrity of the F3 AST Tree
    
    @todo: Due to lack of time this checker is just a skeleton. This functionality will be implemented somewhere in the future (i.e. never)  
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def verify_expression(self, expr, everyInfo):
        '''
        Return "LOGICAL", if the expression is a logical slice
        return "PHYSICAL", if the expression is a physical slice
        return None if it is no slice at all
        '''
        
        if not isinstance(expr, dict):    # In this case it (probably) is a literal
            return None
        
        typeInfo=expr[AST.TYPE]
        if typeInfo=="BINOP":
            leftExpr=expr["left"]
            rightExpr=expr["right"]
            leftExprType=self.verify_expression(leftExpr, everyInfo)
            rightExprType=self.verify_expression(rightExpr, everyInfo)
             
            if leftExprType != None and rightExprType!=None and leftExprType!=rightExprType:
                  raise verify_exception("mixed logical and physical expressions")
            
            if leftExprType!=None:
                return leftExprType # After the previous "if" we can be sure that left is either None or equal to right.
                                    # After the current if we know that left=right, so return either one of them
            # Here we know that either right is not None or left and right are none, so return right    
            return rightExprType
    
        if typeInfo==AST.TYPE_SLICE:
            intervalInfo=expr["interval"]
            intervalType=intervalInfo["type"]
            return intervalType

        if typeInfo=="ASSIGN":
            return None
        
        if typeInfo=="IFOT":
            return None

        if typeInfo=="UMINUS":
            exprInfo=expr["operand"]
            intervalType=self.verify_expression(exprInfo, everyInfo)
            return intervalType
        
        if typeInfo==AST.TYPE_FUNCCALL:
            arg_list=expr[AST.ARG_LIST]
            typeAccumulator=None
            for arg in arg_list:
                intervalType=self.verify_expression(arg, everyInfo)
                if typeAccumulator==None:   # Bootstrap things
                    typeAccumulator=intervalType
                if typeAccumulator!=None and intervalType!=None and intervalType!=intervalType:
                    raise verify_exception("mixed logical and physical expressions")
                if intervalType=="LOGICAL" and everyInfo!=None:
                    raise verify_exception("used logical expressions with every clause") 
                if intervalType=="PHYSICAL" and everyInfo==None:
                    raise verify_exception("used physical expressions without every clause") 
            return typeAccumulator 
                

        
        if typeInfo=="SEMICOLON":
            leftExpr = expr["left"]
            rightExpr= expr["right"]
            self.verify_expression(leftExpr, everyInfo)
            self.verify_expression(rightExpr, everyInfo)
            return None # This is not a very good solution. It would be better to check both sub expressions for consistency
            
        if typeInfo=="PROPCOPY":
            return None # This is neither logical nor physical. It should work on any type
            
        raise verify_exception("unknown operation type %s " % (typeInfo))

        
    def verify_generator(self, expr):
        'Assumes that expr is a generator'  
        everyInfo=expr["every"]
        expressions=expr["expressions"]
        typeAccumulator=None
        for expressionInfo in expressions:
            expressionType=self.verify_expression(expressionInfo[0], everyInfo)
            if typeAccumulator==None:   # Bootstrap things
                typeAccumulator=expressionType
            if typeAccumulator!=None and expressionType!=None and typeAccumulator!=expressionType:
                raise verify_exception("mixed logical and physical expressions")
            if expressionType=="LOGICAL" and everyInfo!=None:
                raise verify_exception("used logical expressions with every clause") 
            if expressionType=="PHYSICAL" and everyInfo==None:
                raise verify_exception("used physical expressions without every clause") 
                
        
    def verify(self, ast):
        '''
        Execute a Formula3 expression on a list of TimeSeries
        @param ast: Formula3 AST
        @raise Formula3Exception
        '''
        type=ast["type"]
        parameters=ast["parameters"]
        generators=ast["generators"]
        
        for generator in generators:
              self.verify_generator(generator)
        
        
        
