from formula3.ast_lexer import AST_Lexer 
import formula3.ast_parser as ast_parser
import ply.yacc as yacc

import F3Helper as Helper

from formula3.exceptions.exception import Formula3Exception

try:
    from at.ac.ait.enviro.tsapi.timeseries import TimeSeries
except ImportError:
    print "Unable to import TimeSeries from java"
    from formula3.PythonTimeSeries import TimeSeries

try:
    from at.ac.ait.enviro.tsapi.timeseries import TimeInterval
except ImportError:
    from formula3.PythonTimeInterval import TimeInterval

try:
    from at.ac.ait.enviro.tsapi.timeseries import TimeStamp
except ImportError:
    from formula3.PythonTimeStamp import TimeStamp


from formula3.ast_interpreter import AST_Interpreter as interpreter

import formula3.globals as globals

import F3Helper
import unittest

enableDebug=False

class complexAggregate:
    'A helper class that gives back a list instead of a string'
    def getValueKeys(self, valueKeys):
        result=[]
        result.extend(valueKeys)
        result.extend(["x1", "x2"])
        return result


class Test(unittest.TestCase):


    def setUp(self):
        self.interp=interpreter()


    def tearDown(self):
        pass
    
    def compileExpression(self, expression):            
        lexer_ast=AST_Lexer()
        parser_ast = yacc.yacc(module=ast_parser, write_tables=enableDebug, debug=enableDebug)
        result=parser_ast.parse(expression, debug=enableDebug)

        # Note: We want to test single generators here, not pipe constructs
        # Thus we 
        # 1. make sure only one generator is given and
        # 2. Unpack it already to make the test code simplier
        generators=result["generators"]
        self.assertIsInstance(generators, list)
        self.assertEqual(1, len(generators))
        
        g=generators[0]
        
        return g

    def constructStandardTS(self):
        ts=F3Helper.TimeSeriesForTests()
        ts.setTSProperty(TimeSeries.VALUE_KEYS, ["v1", "v2"])
        return ts
           
    def testSimple(self):
        ' Give back simply the default value, nothing else'
        expression="@A <<A[i]>>"
        generator=self.compileExpression(expression)
        
        tsA=self.constructStandardTS()
        
        tssDict={'A':tsA}
        
        resultTS=self.interp.constructResultTS(generator, tssDict, F3Helper.TimeSeriesForTests)
        
        valueKeys=resultTS.getTSProperty(TimeSeries.VALUE_KEYS)
        
        self.assertEquals(["v1"], valueKeys)
        

    
    def testNotSoSimple(self):
        ' Give back all keys but with different methods'
        expression="@A <<A[i]; A//.*//[i]>>"
        generator=self.compileExpression(expression)
        
        tsA=self.constructStandardTS()
        
        tssDict={'A':tsA}
        
        resultTS=self.interp.constructResultTS(generator, tssDict, F3Helper.TimeSeriesForTests)
        
        valueKeys=resultTS.getTSProperty(TimeSeries.VALUE_KEYS)
        
        self.assertEquals(["v1", "v2"], valueKeys)
        
        
        
    def testAssignment(self):
        ' Give back all keys but with different methods'
        expression="@A <<A[i] => v3; A//.*//[i]>>"
        generator=self.compileExpression(expression)
        
        tsA=self.constructStandardTS()
        
        tssDict={'A':tsA}
        
        resultTS=self.interp.constructResultTS(generator, tssDict, F3Helper.TimeSeriesForTests)
        
        valueKeys=resultTS.getTSProperty(TimeSeries.VALUE_KEYS)
        
        self.assertEquals(["v3", "v1", "v2"], valueKeys)


    def testExplicitKey(self):
        ' Give back all keys but with different methods'
        expression="@A <<A.v2[i]; A//.*//[i]>>"
        generator=self.compileExpression(expression)
        
        tsA=self.constructStandardTS()
        
        tssDict={'A':tsA}
        
        resultTS=self.interp.constructResultTS(generator, tssDict, F3Helper.TimeSeriesForTests)
        
        valueKeys=resultTS.getTSProperty(TimeSeries.VALUE_KEYS)
        
        self.assertEquals(["v2", "v1"], valueKeys)
        


    def testComplexAgg(self):
        ' Give back keys from the aggregate'
        expression="@A << ca(A[i]) >>"
        
        globals.aggregates["ca"]=complexAggregate()
        
        generator=self.compileExpression(expression)
        
        tsA=self.constructStandardTS()
        
        tssDict={'A':tsA}
        
        resultTS=self.interp.constructResultTS(generator, tssDict, F3Helper.TimeSeriesForTests)
        
        valueKeys=resultTS.getTSProperty(TimeSeries.VALUE_KEYS)
        
        self.assertEquals(["v1", "x1", "x2"], valueKeys)
        
        del globals.aggregates["ca"]

# TODO: Test other things than aggregates like additions, ... 
    
if __name__ == "__main__":
    unittest.main()
