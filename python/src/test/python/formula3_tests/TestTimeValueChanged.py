import F3Helper as Helper

import unittest
try:
    from at.ac.ait.enviro.tsapi.timeseries import TimeStamp
except ImportError:
    print "Unable to import TimeStamp from java"
    from formula3.PythonTimeStamp import TimeStamp
try:
    from at.ac.ait.enviro.tsapi.timeseries import TimeInterval
except ImportError:
    print "Unable to import TimeInterval from java"
    from formula3.PythonTimeInterval import TimeInterval
    
    
from formula3.ast_time_interpreter_changed_values import AST_time_interpreter_changed_values
from formula3.ast_parser import AST_Parser
try:
    from java.util import Date
except ImportError:
    print "Unable to import Date from java"
    from datetime import datetime as Date
    
def getASTFromExpression(expression):
    parser = AST_Parser()
    return parser.parse(expression)


def getResultFromInterpreter(intervalStringDict, expression):
    
    intervalTSDict={}
    for id, interval in intervalStringDict.items():
        time_interval = Helper.getTimeIntervalFromDates(interval)
        intervalTSDict[id]=time_interval
                
    time_interpreter = AST_time_interpreter_changed_values()
    ast = getASTFromExpression(expression)
    
    return time_interpreter.evaluate(ast, intervalTSDict)

class Test(unittest.TestCase):

    def testAST_Time_InterpreterSimple(self):
        result = getResultFromInterpreter({"A": ("1970-01-01 02:45:00", "1970-01-01 04:23:00")}, 
                                          '@A << mean(A[t-1 hour .. t]) >> every 1 hour @ 0 mins')
        expected = Helper.getTimeIntervalFromDates(("1970-01-01 03:00:00", "1970-01-01 05:00:00"))
        self.assertEquals(result, expected)


    def testAST_Time_Interpreter(self):
        result = getResultFromInterpreter({"A":("1970-01-01 02:45:00", "1970-01-01 04:23:00")}, 
                                          '@A << mean(A[t-60 min .. t])  + 3>> every 1 hour @ 0 mins')
        expected = Helper.getTimeIntervalFromDates(("1970-01-01 03:00:00", "1970-01-01 05:00:00"))
        self.assertEquals(result, expected)


    def testAST_Time_InterpreterTwo(self):
        # utils.base_unit_list = 'min'
        result = getResultFromInterpreter({"A":("1970-01-01 02:45:32", "1970-01-01 04:23:12")}, 
                                          '@A @B << (mean(A[t-1 hour .. t])  - mean(B[t .. t+1 hour])) * 4 >> every 1 hour @ 0 mins')
        expected = Helper.getTimeIntervalFromDates(("1970-01-01 02:00:00", "1970-01-01 05:00:00"))
        self.assertEquals(result, expected)

    def testAST_Time_InterpreterDouble(self):
        result = getResultFromInterpreter({"A":("2011-02-08 18:45:32", "2011-02-08 22:23:12")}, 
                                          '@A << (mean(A[t-1 hour .. t])  - mean(A[t .. t+1 hour])) * 4 >> every 1 hour @ 0 mins')
        expected = Helper.getTimeIntervalFromDates(("2011-02-08 18:00:00", "2011-02-08 23:00:00"))
        self.assertEquals(result, expected)

    def testAST_Time_InterpreterMean(self): # No, not mean as in "mean value" but as in "mean and nasty" :-) 
        result = getResultFromInterpreter({"A": ("1970-01-01 02:45:00", "1970-01-01 04:23:00")}, 
                                          '@A << mean(A[i])  + 3>>')
        expected = Helper.getTimeIntervalFromDates(("1970-01-01 02:45:00", "1970-01-01 04:23:00"))
        self.assertEquals(result, expected)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAST_Time_Interpreter']
    unittest.main()
