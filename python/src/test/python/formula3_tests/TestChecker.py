
import F3Helper as Helper
from formula3.ast_check import verify_exception as verify_exception

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


import unittest


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    
           
    def testLogicalAndPhysicalMixed(self):
        exp = '@A << A[i]+A[t..t+10min] >>'
        try :
            tsRes  = Helper.evalExpression(exp, None)
            self.fail("no exception thrown")
        except verify_exception, ex:
            pass
        else:
            self.fail("something unexpected happened")
                    
    def testLogicalWithEvery(self):
        exp = '@A << A[i] >> every 10 mins'
        try :
            tsRes  = Helper.evalExpression(exp, None)
            self.fail("no exception thrown")
        except verify_exception, ex:
            pass
        else:
            self.fail("something unexpected happened")

    def testPhysicalWithoutEvery(self):
        exp = '@A << A[t] >> '
        try :
            tsRes  = Helper.evalExpression(exp, None)
            self.fail("no exception thrown")
        except verify_exception, ex:
            pass
        else:
            self.fail("something unexpected happened")
                    


        
if __name__ == "__main__":
    unittest.main()
