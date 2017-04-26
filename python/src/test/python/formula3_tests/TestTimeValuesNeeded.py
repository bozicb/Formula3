import time
import unittest
import F3Helper as Helper
import formula3.utils.utils as util

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
from formula3.ast_time_interpreter_values_needed import AST_Upstream_Time_Interpreter
from formula3.ast_parser import AST_Parser
    
def getASTFromExpression(expression):
    parser = AST_Parser()
    return parser.parse(expression)

def getResultFromInterpreter(interval_string, expression):
    time_interval = Helper.getTimeIntervalFromDates(interval_string)
    time_interpreter = AST_Upstream_Time_Interpreter()
    ast = getASTFromExpression(expression)
    return time_interpreter.evaluate(ast, time_interval)

class Test(unittest.TestCase):
    
    def testAST_Time_InterpreterSimple(self):
        # util.base_unit_list = 'min'
        result = getResultFromInterpreter(("1970-01-01 02:45:00", "1970-01-01 04:23:00"), 
                                          '@A << mean(A[t-1 hour .. t]) >> every 1 hour @ 0 mins')
        expected=dict()
        expected["A"] = Helper.getTimeIntervalFromDates(("1970-01-01 02:00:00", "1970-01-01 04:00:00"))
        self.assertEquals(expected, result)


    def testAST_Time_Interpreter(self):
        #utils.base_unit_list = 'min'
        result = getResultFromInterpreter(("1970-01-01 02:45:00", "1970-01-01 04:23:00"), 
                                          '@A << mean(A[t-60 min .. t])  + 3>> every 1 hour @ 0 mins')
        expected=dict()
        expected["A"] = Helper.getTimeIntervalFromDates(("1970-01-01 02:00:00", "1970-01-01 04:00:00"))
        self.assertEquals(expected, result)


    def testAST_Time_InterpreterTwo(self):
        # util.base_unit_list = ('min',)
        result = getResultFromInterpreter(("1970-01-01 02:45:32", "1970-01-01 04:23:12"), 
                                          '@A @B << (mean(A[t-1 hour .. t])  - mean(B[t .. t+1 hour]) ) * 4 >> every 1 hour @ 0 mins')
        expected=dict()
        expected["A"] = Helper.getTimeIntervalFromDates(("1970-01-01 02:00:00", "1970-01-01 04:00:00"))
        expected["B"] = Helper.getTimeIntervalFromDates(("1970-01-01 03:00:00", "1970-01-01 05:00:00"))
        self.assertEquals(expected, result)

    def testAST_Time_InterpreterDouble(self):
        result = getResultFromInterpreter(("2011-02-08 18:45:32", "2011-02-08 22:23:12"), 
                                          '@A << (mean(A[t-1 hour .. t])  - max(A[t .. t+1 hour])) * 4 >> every 1 hour @ 0 mins')
        expected=dict()
        expected["A"] = Helper.getTimeIntervalFromDates(("2011-02-08 18:00:00", "2011-02-08 23:00:00"))
        self.assertEquals(expected, result)
        
    def testUpStreamTimeInterpreter_Simple(self):
        result = getResultFromInterpreter(("1970-01-01 01:10:00", "1970-01-01 03:20:00"),
                                          "@A << mean(A[t-1 hour .. t]) >> every 1 hour @ 0 mins")
        expected=dict()
        expected["A"] = Helper.getTimeIntervalFromDates(("1970-01-01 01:00:00", "1970-01-01 03:00:00"))
        self.assertEquals(result, expected)
        
    def testUpStreamTimeInterpreter_Ext(self):
        result = getResultFromInterpreter(("1970-01-01 03:10:00", "1970-01-01 08:20:00"),
                                          "@A << mean(A[t - 30 mins .. t + 30 mins]) >> every 3 hours @ 0 mins")
        expected=dict()
        expected["A"] = Helper.getTimeIntervalFromDates(("1970-01-01 05:30:00", "1970-01-01 06:30:00"))
        self.assertEquals(result, expected)
        
    def testUpstreamTimeInterpreter_Double(self):
        result = getResultFromInterpreter(("1970-01-01 03:10:00", "1970-01-01 08:20:00"),
                                          "@A @B << mean(A[t - 1 hours .. t]) + max(B[t .. t + 1 hours]) >> every 1 hours @ 0 mins")
        expected=dict()
        expected["A"] = Helper.getTimeIntervalFromDates(("1970-01-01 03:00:00", "1970-01-01 08:00:00"))
        expected["B"] = Helper.getTimeIntervalFromDates(("1970-01-01 04:00:00", "1970-01-01 09:00:00"))
        self.assertEquals(result, expected)


    def testUpstreamTimeInterpreter_1minOfHour(self):
        result = getResultFromInterpreter(("1970-01-01 01:17:00","1970-01-01 02:34:00"),
                                          "@TS <<TS[t-1min..t]>> every 1 hour")
        expected=dict()
        expected["TS"] = Helper.getTimeIntervalFromDates(("1970-01-01 01:59:00","1970-01-01 02:00:00"))
        self.assertEquals(result, expected)

    def testAST_Time_InterpreterMean(self): # No, not mean as in "mean value" but as in "mean and nasty" :-) 
        result = getResultFromInterpreter(("1970-01-01 02:45:00", "1970-01-01 04:23:00"), 
                                          '@A <<mean(A[i])  + 3>>')
        expected=dict()
        expected["A"] = Helper.getTimeIntervalFromDates(("1970-01-01 02:45:00", "1970-01-01 04:23:00"))
        self.assertEquals(result, expected)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAST_Time_Interpreter']
    unittest.main()
