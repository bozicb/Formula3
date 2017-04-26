# Purpose: Test F3 wrapped in a TSP.
# This is not a complete test for everything F3 might give us.
# It's main purpose is to demonstrate and check how a TSP is operated

import unittest


from formula3.TSP_AST import TSP_AST
from formula3.PythonTimeSeries import TimeSeries
from formula3.exceptions.exception import Formula3Exception

import F3Helper
    

class Test(unittest.TestCase):
    
    
    def compareSlot(self, s1, s2, vKeys):
        '''
        Compare two timeseries
        ''' 
        
        for key in vKeys:
            val1 = s1.get(key)
            val2 = s2.get(key)
            self.assertTrue( val1 == val2, 
                             'Different values in slot: '+str(val1)+' and '+str(val2)+' ('+str(key)+')') 

        pass

    
    def compareTS(self, ts1, ts2):
        '''
        Compare two slots
        ''' 
#        ts1 = ts1
##        ts2 = ts2
#        self.printTS(ts1)
#        print("\n")
#        self.printTS(ts2)


        # both TS should have the same amount of slots
        ts1Size = len(ts1.getTimeStamps())
        ts2Size = len(ts2.getTimeStamps())
        self.assertEquals(ts1Size, ts2Size, 
                          "Both TimeSeries should have the same amount of slots")
        
        # VALUE_KEYS from both TimeSeries
        vk_array1=ts1.getTSProperty(TimeSeries.VALUE_KEYS)
        vk_array2=ts2.getTSProperty(TimeSeries.VALUE_KEYS)
        
        self.assertEquals(vk_array1, vk_array2)
        
        
        for timestamp in ts1.getTimeStamps():
            slot1 = ts1.getSlot(timestamp)            
            slot2 = ts2.getSlot(timestamp)
            
            self.compareSlot(slot1, slot2, vk_array1) 
            
        for timestamp in ts2.getTimeStamps():
            slot1 = ts1.getSlot(timestamp)            
            slot2 = ts2.getSlot(timestamp)
            
            self.compareSlot(slot1, slot2, vk_array2)

    
    def testCopyNamedTS(self):
        # A simple test. Just pass the TS through
        tsp=TSP_AST()
        tsp.compile("@A <<A[i]>>")
        tsp.TSClass=F3Helper.TimeSeriesForTests
        
        tsOrig = F3Helper.constructTS([0, 1000, 2000, 3000, 4000], ["A", "B"], A=[10, 20, 30, 40,  50], B=[0, 1000, 2000, 3000, 4000])
        tsExp  = F3Helper.constructTS([0, 1000, 2000, 3000, 4000], ["A", "B"], A=[10, 20, 30, 40,  50], B=[0, 1000, 2000, 3000, 4000])

        tsRes=tsp.eval({"A":tsOrig});
        self.compareTS(tsExp, tsRes[0])

    def testCompileLog(self):
        # Another important functionality. A means to get the compile log and give it to a potential remote user.
        # Hint, hint, hint. Not every user might have root access to the system that runs F3 and has access to the log files
        # More hinting: if the above hint sounds outlandish to you...think of interactive F3, not only statically configured systems 
        tsp=TSP_AST()
        tsp.compile("@A <<A[i]>>")
        tsp.getParseLog()

    def testMultIntegerTS(self):
        tsp=TSP_AST()
        tsp.TSClass=F3Helper.TimeSeriesForTests
        tsp.compile("@A <<A[i] * 2>>")
        tsOrig = F3Helper.constructTS([0, 1000, 2000, 3000, 4000], ["A", "B"], A=[10, 20, 30, 40,  50], B=[0, 1000, 2000, 3000, 4000])
        tsExp  = F3Helper.constructTS([0, 1000, 2000, 3000, 4000], ["A", "B"], A=[20, 40, 60, 80, 100], B=[0, 1000, 2000, 3000, 4000])
        tsRes=tsp.eval({"A":tsOrig});
        self.compareTS(tsExp, tsRes[0])
        
    def testEventTimeCalculation(self):
        tsp=TSP_AST()
        tsp.compile("@A <<A[t] * 2>> every 1 min")

        input=F3Helper.getTimeIntervalFromDates(("2010-01-08 12:34:56", "2010-01-08 12:36:56"))
        inputDict={"A":input}
        result=tsp.getDataChangedInterval(inputDict);
        
        expected=F3Helper.getTimeIntervalFromDates(("2010-01-08 12:35:00", "2010-01-08 12:36:00"))
        self.assertEquals(expected, result)
    
        
    def testNeededTimeCalculation(self):
        tsp=TSP_AST()
        tsp.compile("@A <<A[t] * 2>> every 1 hour")

        input=F3Helper.getTimeIntervalFromDates(("2010-01-08 11:34:56", "2010-01-08 12:36:56"))
        result=tsp.getDataNeededIntervals(input);
        
        expected=dict()
        expected["A"]=F3Helper.getTimeIntervalFromDates(("2010-01-08 12:00:00", "2010-01-08 12:00:00"))
        self.assertEquals(expected, result)


    def testParameterInfo(self):
        tsp=TSP_AST()
        tsp.compile('@A @B="XYZ" <<A[t] * 2>> every 1 hour')

        parameters=tsp.getParameterInfo()
          
        expected={"A":None, "B":"XYZ"}
        self.assertEquals(expected, parameters)
        
    def testProfiling(self):
        tsp=TSP_AST()
        tsp.TSClass=F3Helper.TimeSeriesForTests
        tsp.compile("@A <<A[i] * 2>>")
        tsOrig = F3Helper.constructTS([0, 1000, 2000, 3000, 4000], ["A", "B"], A=[10, 20, 30, 40,  50], B=[0, 1000, 2000, 3000, 4000])
        tsExp  = F3Helper.constructTS([0, 1000, 2000, 3000, 4000], ["A", "B"], A=[20, 40, 60, 80, 100], B=[0, 1000, 2000, 3000, 4000])
        
        tsp.setProfiling(True)
        
        tsRes=tsp.eval({"A":tsOrig});
        self.compareTS(tsExp, tsRes[0])
    
    def testSyntaxError(self):
        tsp=TSP_AST()
        tsp.TSClass=F3Helper.TimeSeriesForTests
        try:
            tsp.compile("@A << A >>")
        except Formula3Exception:
            parseLog=tsp.getParseLog()
            self.assertNotEqual("Not compiled yet", parseLog)
            
        