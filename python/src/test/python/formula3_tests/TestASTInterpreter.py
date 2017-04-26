import math

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


import unittest


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    
           
    def compareSlot(self, s1, s2, vKeys, t):
        '''
        Compare two timeseries
        ''' 
        
        for key in vKeys:
            val1 = s1.get(key)
            val2 = s2.get(key)
            self.assertTrue( val1 == val2, 
                             'Different values in slot %d. Key is %s, expected=%s, found %s: ' % (t.asMilis(), key, str(val1), str(val2)) 
                             )

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
        vKey1 = ts1.getTSProperty(TimeSeries.VALUE_KEYS)
        vKey2 = ts2.getTSProperty(TimeSeries.VALUE_KEYS)
        
        # Test if VALUE_KEYS from both TS are identical
#        self.assertTrue(vKey1.containsAll(vKey2))
#        self.assertTrue(vKey2.containsAll(vKey1))
        
        for timestamp in ts1.getTimeStamps():
            slot1 = ts1.getSlot(timestamp)            
            slot2 = ts2.getSlot(timestamp)
            
            self.compareSlot(slot1, slot2, vKey1, timestamp) 
            
        for timestamp in ts2.getTimeStamps():
            slot1 = ts1.getSlot(timestamp)            
            slot2 = ts2.getSlot(timestamp)
            
            self.compareSlot(slot1, slot2, vKey1, timestamp)
            


#    def testLogicalSlicing(self):
#        tsOrig = Helper.gimmeTS(valueStart=10, valueIncr=10, timeStart=0, timeIncr=1000, size=10) # Times: 0 sec, 1 sec, 2, ... 10
#        t=TimeStamp(5000)
#        tsNode=('TS', 'A', '', ('PHYSICAL', ('LEFT', 'CLOSED', (0, 'min')), ('RIGHT', 'CLOSED', (0, 'min'))), '')
#        tsExpected=Helper.gimmeTS(valueStart=50, valueIncr=10, timeStart=5000, timeIncr=1000, size=1) # Times: 5 sec. Just one single slot, Vassily
#        slice=interpreter.logic_splice(tsNode, [t], tsOrig, 5)        
#        self.compareTS(tsExpected, slice)
#
#    def testPhysSlicing(self):
#        tsOrig = Helper.gimmeTS(valueStart=10, valueIncr=10, timeStart=0, timeIncr=1000, size=10) # Times: 0 sec, 1 sec, 2, ... 10
#        leftOffset =utils.utils.normalizeTimeValue((0, 'sec'))
#        rightOffset=utils.utils.normalizeTimeValue((0, 'sec'))
#        t=TimeStamp(5000)
#        tsNode=('TS', 'A', '', ('PHYSICAL', ('LEFT', 'CLOSED', (0, 'min')), ('RIGHT', 'CLOSED', (0, 'min'))), '')
#        tsExpected=Helper.gimmeTS(valueStart=50, valueIncr=10, timeStart=5000, timeIncr=1000, size=1) # Times: 5 sec. Just one single slot, Vassily
#
#        slice=interpreter.physical_slice(tsNode, tsOrig, t, leftOffset, rightOffset)
#        
#        self.compareTS(tsExpected, slice)
        

    def errorBehaviour(self):
        exp = '@A << XXX >>'
        tsOrig = Helper.constructTS([0,1000,2000,3000], ["v"], v=[5.5,10.5,15.5,20.5])
        try:
            tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        except Formula3Exception:
            pass

    def copyNamedTS(self):
        exp = '@A << A[i] >>'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["A", "B"], A=[10, 20, 30, 40, 50], B=[0, 1000, 2000, 3000, 4000])
        tsExp  = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["A"],      A=[10, 20, 30, 40, 50])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})        
        self.compareTS(tsExp, tsRes[0])
       
    def copyNamedTSAlternative(self):
        exp = '@A << A//.*//[i] >>'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["A", "B"], A=[10, 20, 30, 40, 50], B=[0, 1000, 2000, 3000, 4000])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})        
        self.compareTS(tsOrig, tsRes[0])

        # Special case: an empty time series. This caused a problem in the past       
        exp = '@A <<  mean(A[t-10min..t]); A//.*//[i] >> every 10 mins'
        tsOrig = Helper.constructTS([], ["A", "B"], A=[], B=[])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})        
        self.compareTS(tsOrig, tsRes[0])
       
        

    def copyIgnoreFirstTS(self):
        exp = '@I @A << A[i] >>'
        ts1 = Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])
        ts2 = Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[40, 50, 60, 70], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp=Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue"],                valueDPvalue=[40, 50, 60, 70])
        tsRes  = Helper.evalExpression(exp, {'I': ts1, 'A': ts2})
        self.compareTS(tsExp, tsRes[0])

        
    def copyIgnoreSecondTS(self):
        exp = '@A @I << A[i] >>'
        ts1 = Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])
        ts2 = Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[40, 50, 60, 70], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp=Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue"],                valueDPvalue=[10, 20, 30, 40])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'I': ts2})
        self.compareTS(tsExp, tsRes[0])
        

    def firstComeFirstServe(self):
        exp = '@A << A[i]*2; A[i]*3 >>'
        ts1 = Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp=Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue"]               , valueDPvalue=[20, 40, 60, 80])
        tsRes  = Helper.evalExpression(exp, {'A': ts1})
        self.compareTS(tsExp, tsRes[0])


    def emptyTS(self):
        exp = '@A << A[t]*2 >> every 1 sec' 
        ts1 = Helper.constructTS([], ["valueDPvalue", "valueDPtest"], valueDPvalue=[], valueDPtest=[])
        tsExp=Helper.constructTS([], ["valueDPvalue"]               , valueDPvalue=[])
        tsRes  = Helper.evalExpression(exp, {'A': ts1})
        self.compareTS(tsExp, tsRes[0])

    def alignedAddIntIndex(self):
        exp = '@A @B << A[i] + B[i] >>'
        ts1 = Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])
        ts2 = Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp=Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue"]               , valueDPvalue=[20, 40, 60, 80])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})
        self.compareTS(tsExp, tsRes[0])


    def alignedSubIntIndex(self):
        exp = '@A @B << A[i] - B[i] >>'
        ts1 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])
        ts2 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[ 5, 10, 15, 25], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp=Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[ 5, 10, 15, 15])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})        
        self.compareTS(tsExp, tsRes[0])
        

    def alignedMultiIntIndex(self):
        exp = '@A @B << A[i] * B[i] >>'
        ts1 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[ 10,  20,  30,   40], valueDPtest=[1000, 2000, 3000, 4000])
        ts2 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[ 10,  20,  30,   40], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp=Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[100, 400, 900, 1600])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})        
        self.compareTS(tsExp, tsRes[0])
        
        
    def alignedDivIntIndex(self):
        exp = '@A @B << A[i] / B[i] >>'
        ts1   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])
        ts2   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 10, 10, 10], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[ 1,  2,  3,  4])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})        
        self.compareTS(tsExp, tsRes[0])
        
        
    def alignedPowIntIndex(self):
        exp = '@A @B << A[i] ** B[i] >>'
        ts1   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[ 10,  20,  30,  40], valueDPtest=[1000, 2000, 3000, 4000])
        ts2   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[  2,   2,   2,   2], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[100, 400, 900, 1600])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})        
        self.compareTS(tsExp, tsRes[0])
        
        
    def alignedAddFloatIndex(self):
        exp = '@A @B << A[i] + B[i] >>'
        ts1   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[ 10.2,  20.2,  30.2,  40.2], valueDPtest=[1000, 2000, 3000, 4000])
        ts2   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[ 10.3,  20.3,  30.3,  40.3], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[ 20.5,  40.5,  60.5,  80.5])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})        
        self.compareTS(tsExp, tsRes[0])
        
        
    def alignedSubFloatIndex(self):
        exp = '@A @B << A[i] - B[i] >>'
        ts1   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10.75, 20.75, 30.75, 40.75], valueDPtest=[1000, 2000, 3000, 4000])
        ts2   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[ 5.25, 10.25, 15.25, 20.25], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[ 5.5,  10.5,  15.5,  20.5 ])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})        
        self.compareTS(tsExp, tsRes[0])
           
    
    def shiftForward(self):
        exp = '@A << A[i+1] >>'
        tsOrig=Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])
        tsExp = Helper.constructTS([1000, 2000, 3000], ["valueDPvalue"], valueDPvalue=[20,30,40])
        tsRes = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
    
    def shiftBack(self):
        exp = '@A << A[i-1] >>'    
        tsOrig= Helper.constructTS([1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])        
        tsExp = Helper.constructTS(      [2000, 3000, 4000], ["valueDPvalue"],                valueDPvalue=[10, 20, 30])
        tsRes = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
    
    
    def multiInt(self):
        exp = '@A << A[i] * 2 >>'  
        tsOrig= Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[0, 1000, 2000, 3000])  
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"], valueDPvalue=[20, 40, 60, 80])        
        tsRes = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
        
    def multiReal(self):
        exp = '@A << A[i] * 0.5 >>'  
        tsOrig= Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[0, 1000, 2000, 3000])           
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"], valueDPvalue=[5, 10, 15, 20])
        tsRes = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
        
    def addInt(self):
        exp = '@A << A[i] + 2 >>'  
        tsOrig= Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[0, 1000, 2000, 3000])           
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[12, 22, 32, 42])   
        tsRes = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
        
    def addReal(self):
        exp = '@A << A[i] + 2.4 >>'  
        tsOrig= Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[0, 1000, 2000, 3000])           
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[12.4, 22.4, 32.4, 42.4])
        tsRes = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
        
    def powAdd(self):
        exp = '@A << A[i] ** 2 + 5 >>'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])  
        tsExp =  Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"], valueDPvalue=[105, 405, 905, 1605])
        tsRes = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
 

    def addString(self):
        exp = '@A << A[i] + "X" >>'  
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000], ["s", "n"], s=["20",  "40",  "60",  "80"], n=[0, 1000, 2000, 3000])
        tsExp  = Helper.constructTS([0, 1000, 2000, 3000], ["s"]     , s=["20X", "40X", "60X", "80X"])        
        tsRes = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        

    def uminus(self):
        exp = '@A << -A[i] >>'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000], ["values", "extraValues"], values=[0,  1,  2,  3], extraValues=[10, 11, 12, 13])
        tsExp  = Helper.constructTS([0, 1000, 2000, 3000], ["values"],                values=[0, -1, -2, -3])        
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})        
        self.compareTS(tsExp, tsRes[0])
       

        
#    def testValueSet(self):
#        exp = '@A < A[2] >'
#        tsOrig = Helper.constructTS([0, 1000, 2000, 3000, 4000, 5000, 6000], [312, 231, 1213, 11, 123, 3, 8812])
#        tsExp = Helper.constructTS([0, 1000, 2000, 3000, 4000, 5000, 6000], [1213, 1213, 1213, 1213, 1213, 1213, 1213])
#        tsRes  = Helper.evalExpression(exp, [tsOrig])
#        self.compareTS(tsExp, tsRes[0])
        
            
    def logicalMean(self):
        exp = '@A << mean(A[i-1 .. i]) >>'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000, 4000, 5000], ["v1", "x1"], v1=[10, 4, 6, 10, 10, 4], x1=[0, 1000, 2000, 3000, 4000, 5000])
        tsExp  = Helper.constructTS([0, 1000, 2000, 3000, 4000, 5000], ["v1"],       v1=[10, 7, 5, 8, 10, 7])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
       
    def logicalMax(self):
        exp = '@A << max(A[i-1 .. i]) >>'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000, 4000, 5000], ["A", "B"], A=[1, 4, 6, 10, 10, 4], B=[0, 1000, 2000, 3000, 4000, 5000])
        tsExp = Helper.constructTS( [0, 1000, 2000, 3000, 4000, 5000], ["A"],      A=[1, 4, 6, 10, 10, 10])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
       
    def logicalMin(self):
        exp = '@A << min(A[i-1 .. i]) >>'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000, 4000, 5000], ["v1", "v2"], v1=[10, 6, 4, 10, 10, 4], v2=[0, 1000, 2000, 3000, 4000, 5000])
        tsExp = Helper.constructTS( [0, 1000, 2000, 3000, 4000, 5000], ["v1"],       v1=[10, 6, 4,  4, 10, 4])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
       
            
    def physicalMeanSimple(self):
        
        # REQUEST_INTERVAL
        
        exp = '@A << mean(A[t .. t + 1 sec])>> every 1 sec'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000], ["v", "v1"], v=[0,    0, 1, 999], v1=[0, 1000, 2000, 3000])
        tsExp  = Helper.constructTS([0, 1000, 2000],       ["v"],       v=[0,    0.5, 500])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A << mean(A[t .. t+1min])>> every 1 min'
        tsOrig = Helper.constructTS([0, 1000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20], valueDPtest=[1000, 2000])
        # This does not cover a complete minute thus we expect no result, i.e. an empty timeseries
        tsExp = Helper.constructTS([], ["valueDPvalue"], valueDPvalue=[])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
#        exp = '@A < A[t .. t+1min].mean> every 1 min'
#        tsOrig = Helper.gimmeTS(valueStart=10, valueIncr=10, timeStart=0, timeIncr=1000, size=2) # Times: 0 sec, 1 sec, 2
#        # Now we set the REQUEST_INTERVAL property and things should work :-)
#        tsOrig.setTSProperty(TimeSeries.REQUEST_INTERVAL, TimeInterval(TimeInterval.Openness.CLOSED, TimeStamp(0), TimeStamp(60*1000), TimeInterval.Openness.CLOSED))
#        tsExp = Helper.constructTS([0], [15], [0])
#        tsRes  = Helper.evalExpression(exp, [tsOrig])
#        self.compareTS(tsExp, tsRes[0])

    
    def physicalMeanWithEmptyTS(self):
        
        exp = '@A << mean(A[t .. t+1min])>> every 1 min'
        tsOrig = Helper.constructTS([], ["valueDPvalue", "valueDPtest"], valueDPvalue=[], valueDPtest=[])
        tsOrig.setTSProperty(TimeSeries.REQUEST_INTERVAL, TimeInterval(TimeInterval.Openness.CLOSED, TimeStamp(0), TimeStamp(60*1000), TimeInterval.Openness.CLOSED))
        tsExp = Helper.constructTS([], ["valueDPvalue"], valueDPvalue=[])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])


    def physicalMeanWithPropCopy(self):
        
        exp = '@A << mean(A[t .. t+10sec]); A//.*//[t..t+10sec]>> every 1 sec'
        tsOrig = Helper.constructTS([1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[1000, 2000, 3000], valueDPtest=[4000, 5000, 6000])
        tsOrig.setTSProperty(TimeSeries.REQUEST_INTERVAL, TimeInterval(TimeInterval.Openness.CLOSED, TimeStamp(0), TimeStamp(60*1000), TimeInterval.Openness.CLOSED))
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[2000, 2000, 2500, 3000], valueDPtest=[4000, 4000, 5000, 6000])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])


    def physicalOpenClose(self):
        
        # REQUEST_INTERVAL
        
        exp = '@A << mean(A[t .. t + 1 sec]) >> every 1 sec'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000], ["values", "v1"], values=[0,    0,      1,   999], v1=[0, 1000, 2000, 3000])
        tsExp  = Helper.constructTS([0, 1000, 2000],       ["values"],       values=[   0,    0.5,   500])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])

        exp = '@A << mean(A]t .. t + 1 sec]) >> every 1 sec'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000], ["v", "v1"], v=[0,    0,   1,   999], v1=[0, 1000, 2000, 3000])
        tsExp  = Helper.constructTS([0, 1000, 2000],       ["v"],       v=[      0, 1.0, 999.0])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A << mean(A[t .. t + 1 sec[) >> every 1 sec'
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000], ["v", "v1"], v=[0, 0, 1.0, 999.0], v1=[0, 1000, 2000, 3000])
        tsExp  = Helper.constructTS([0, 1000, 2000],       ["v"],       v=[0, 0, 1.0])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A << mean(A]t .. t + 1 sec[)>> every 1 sec'  # Note: For the sake of easy testing this test also relies on the fact that no value to calc the mean from will result in no slot in the result
        tsOrig = Helper.constructTS([0, 1000, 2000, 3000], ["v", "v1"], v=[0,    0,   1, 999], v1=[0, 1000, 2000, 3000])
        tsExp  = Helper.constructTS([],                    ["v"],       v=[])
        tsRes  = Helper.evalExpression(exp, {'A': tsOrig})
        self.compareTS(tsExp, tsRes[0])
        
    
    def tAnd(self):
        exp = '@A @B << A[i] and B[i] >>'
        ts1 = Helper.constructTS([0, 10, 20, 30], ["v", "w"], v=[0,    0, 1, 1000], w=[0, 1000, 2000, 3000])
        ts2 = Helper.constructTS([0, 10, 20, 30], ["a", "b"], a=[0, 1000, 0,    1], b=[0, 2000, 4000, 6000])
        tsExp=Helper.constructTS([0, 10, 20, 30], ["v"]     , v=[0,    0, 0,    1])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})   
        self.compareTS(tsExp, tsRes[0])
    
    def tOr(self):
        exp = '@A @B << A[i] or B[i] >>'
        ts1 = Helper.constructTS([0, 10, 20, 30], ["v", "v1"], v=[0,    0, 1, 1000], v1=[0, 1000, 2000, 3000])
        ts2 = Helper.constructTS([0, 10, 20, 30], ["v", "v1"], v=[0, 1000, 0,    1], v1=[0, 2000, 4000, 6000])
        tsExp=Helper.constructTS([0, 10, 20, 30], ["v"],       v=[0,    1, 1,    1])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})   
        self.compareTS(tsExp, tsRes[0])
    
    def tXor(self):
        exp = '@A @B << A[i] xor B[i] >>'
        ts1 = Helper.constructTS([0, 10, 20, 30], ["values", "extraValues"], values=[0,    0, 1, 1000], extraValues=[0, 1000, 2000, 3000])
        ts2 = Helper.constructTS([0, 10, 20, 30], ["values", "extraValues"], values=[0, 1000, 0,    1], extraValues=[0, 2000, 4000, 6000])
        tsExp=Helper.constructTS([0, 10, 20, 30], ["values"],                values=[0,    1, 1,    0])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})   
        self.compareTS(tsExp, tsRes[0])

    def greater(self):
        exp = '@A @B << (A[i] > B[i]) >>'
        ts1 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])  
        ts2 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 10, 10, 10], valueDPtest=[1000, 2000, 3000, 4000])  
        tsExp=Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[ 0, 1,  1,  1])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})   
        self.compareTS(tsExp, tsRes[0])
        
    def lower(self):
        exp = '@A @B << A[i] < B[i] >>'
        ts1 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])  
        ts2 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 10, 10, 10], valueDPtest=[1000, 2000, 3000, 4000])  
        tsExp=Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"],                valueDPvalue=[0,   0,  0,  0])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})   
        self.compareTS(tsExp, tsRes[0])
        
    def greaterEqual(self):
        exp = '@A @B << A[i] >= B[i] >>'
        ts1   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[ 0, 10, 20, 30], valueDPtest=[1000, 2000, 3000, 4000])  
        ts2   = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 10, 10, 10], valueDPtest=[1000, 2000, 3000, 4000])  
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"],                valueDPvalue=[ 0,  1, 1,  1])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})   
        self.compareTS(tsExp, tsRes[0])
        
    def lowerEqual(self):
        exp = '@A @B << A[i] <= B[i] >>'
        ts1 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[1000, 2000, 3000, 4000])  
        ts2 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 10, 10, 10], valueDPtest=[1000, 2000, 3000, 4000])  
        tsExp=Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"],                valueDPvalue=[1,   0,  0,  0])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})   
        self.compareTS(tsExp, tsRes[0])

    def equal(self):
        exp = '@A @B << A[i] == B[i] >>'
        ts1 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[0, 1000, 2000, 3000])
        ts2 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 10, 10, 10], valueDPtest=[0, 1000, 2000, 3000])
        tsExp=Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[ 1,  0,  0,  0])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})   
        self.compareTS(tsExp, tsRes[0])
        
    def notEqual(self):
        exp = '@A @B << A[i] != B[i] >>'
        ts1 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 20, 30, 40], valueDPtest=[0, 1000, 2000, 3000])
        ts2 = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[10, 10, 10, 10], valueDPtest=[0, 1000, 2000, 3000])
        tsExp = Helper.constructTS([0,1000,2000,3000], ["valueDPvalue"],                 valueDPvalue=[0,  1,  1,  1])
        tsRes  = Helper.evalExpression(exp, {'A': ts1, 'B': ts2})   
        self.compareTS(tsExp, tsRes[0])
        
    def ifOtherwise(self):
        exp = '@A << A[i] if A[i] >= 3 otherwise 0 >>'
        ts    = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[1, 2, 3, 4, 5], valueDPtest=[0, 1000, 2000, 3000, 4000, 5000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["valueDPvalue"]               , valueDPvalue=[0, 0, 3, 4, 5])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A @B << A[i] if A[i] < B[i] otherwise B[i] >>'
        tsA = Helper.constructTS([0, 1000, 2000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[2, 2, 2], valueDPtest=[0, 1000, 2000])
        tsB = Helper.constructTS([0, 1000, 2000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[1, 2, 3], valueDPtest=[0, 1000, 2000])
        tsExp=Helper.constructTS([0, 1000, 2000], ["valueDPvalue"]               , valueDPvalue=[1, 2, 2])
        tsRes = Helper.evalExpression(exp, {'A': tsA, 'B': tsB})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A << 1 if (A[i] > 1) otherwise 0 => value:value >>'
        ts  = Helper.constructTS([0, 1000, 2000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[0, 1, 2], valueDPtest=[0, 1000, 2000])
        tsExp=Helper.constructTS([0, 1000, 2000], ["valueDPvalue"]               , valueDPvalue=[0, 0, 1])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A << A[i]*2 if (A[i] > 2) otherwise A[i]**2 >>'
        ts    = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[0, 1, 2, 3], valueDPtest=[0, 1000, 2000, 3000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000], ["valueDPvalue"]               , valueDPvalue=[0, 1, 4, 6])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A @B @C << A[i] + C[i] if B[i] == A[i] otherwise B[i]*C[i] >>'
        tsA = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[  1,   2,   3,   4,   5], valueDPtest=[0, 1000, 2000, 3000, 4000])
        tsB = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[  3,   3,   3,   3,   3], valueDPtest=[0, 1000, 2000, 3000, 4000])
        tsC = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[100, 100, 100, 100, 100], valueDPtest=[0, 1000, 2000, 3000, 4000])
        tsExp=Helper.constructTS([0, 1000, 2000, 3000, 4000], ["valueDPvalue"]               , valueDPvalue=[300, 300, 103, 300, 300])
        tsRes = Helper.evalExpression(exp, {'A': tsA, 'B': tsB, 'C': tsC})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A << A[i] if (A[i] > 1) otherwise None >>'
        tsA = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["valueDPvalue", "valueDPtest"], valueDPvalue=[0, 1, 2, 3, 4], valueDPtest=[0, 1000, 2000, 3000, 4000])
        tsExp = Helper.constructTS([       2000, 3000, 4000], ["valueDPvalue"],                valueDPvalue=[      2, 3, 4])

        tsRes = Helper.evalExpression(exp, {'A': tsA})
        self.compareTS(tsExp, tsRes[0])
        
    def assignment(self):
        exp = '@A << A[i] => mean >>'
        ts    = Helper.constructTS([0, 1000], ["X", "Y"], X=[1.0, 1.5], Y=[0, 10])
        tsExp = Helper.constructTS([0, 1000], ["mean"],   mean=[1.0, 1.5])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A << mean(A[i-1 .. i]) => mean >>'
        ts    = Helper.constructTS([0, 1000, 2000, 3000, 4000, 5000], ["v1", "v2"], v1=[1, 2, 3, 4, 5, 6], v2=[0, 1000, 2000, 3000, 4000, 5000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000, 4000, 5000], ["mean"]    , mean=[1.0, 1.5, 2.5, 3.5, 4.5, 5.5] )
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
        
        exp = '@A << "set" if (A[i] > 10) otherwise "reset" => command >>'
        ts    = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["v1","v2"], v1=[5, 10, 15, 10, 5], v2=[0, 1000, 2000, 3000, 4000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["command"], command=["reset", "reset", "set", "reset", "reset"])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
        
    def funcCall(self):
        exp = '@A << A[i]+log(3) => value >>'   # Note: Due to current restrictions there MUST be at least one time series in the expression
        ts    = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["value", "extraValue"], value=[1, 2, 3, 4, 5], extraValue=[0, 1000, 2000, 3000, 4000, 5000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["value"]              , value=[1+math.log(3.0), 2+math.log(3.0), 3+math.log(3.0), 4+math.log(3.0), 5+math.log(3.0)])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])

    def log(self):
        exp = '@A << log(A[i]) >>'
        ts    = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["value", "extraValue"], value=[1, 2, 3, 4, 5], extraValue=[0, 1000, 2000, 3000, 4000, 5000])
        tsExp = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["value"]              , value=[0.0, 0.69314718055994529, 1.0986122886681098, 1.3862943611198906, 1.6094379124341003])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
    
    def semicolon(self):
        exp = '@A << A[i] * 2;  10 => value_test>>'
        ts    = Helper.constructTS([0, 1000, 2000], ["value", "extraValue"], value=[1, 2, 3], extraValue=[0, 1000, 2000])
        tsExp = Helper.constructTS([0, 1000, 2000], ["value", "value_test"], value=[2, 4, 6], value_test=[10, 10, 10])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
    
    
    def pipe(self):
        exp = '@A << A[i] * 2 >> | << _[i] / 2 >>'
        ts    = Helper.constructTS([0, 1000, 2000], ["values", "values_extra"], values=[1, 2, 3], values_extra=[0, 1000, 2000])
        tsExp = Helper.constructTS([0, 1000, 2000], ["values"], values=[1, 2, 3])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
        
    def count(self):
        exp = '@A << count(A[i]) >>'
        ts   = Helper.constructTS([0, 1000, 2000], ["v1", "v2"], v1=[None, 1, None], v2=[0, 1000, 2000])
        tsExp= Helper.constructTS([0, 1000, 2000], ["v1"],       v1=[0,    1,    0])
        tsRes= Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])

    def countWithEmptySlots(self):
        exp = '@A << count(A[t]) >> every 1 sec'
        ts = Helper.constructTS([0, 1000, 5000], ["x", "y"], x=[None, 1, None], y=[0, 1000, 2000])  # Note the time, there is a hole between 1000 and 5000
        tsExp = Helper.constructTS([0, 1000, 2000, 3000, 4000, 5000], ["x"], x=[0, 1, 0, 0, 0, 0])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])

        
    def count_pipe(self):
        exp = '@A << A[i] if (A[i] > 2) otherwise None >> | << count(_[i]) >>'
        ts  = Helper.constructTS([0, 1000, 2000, 3000, 4000], ["v1", "v2"], v1=[0, 1, 2, 3, 4], v2=[0, 1000, 2000, 3000, 4000])
        tsExp=Helper.constructTS([               3000, 4000], ["v1"]      , v1=[         1, 1])
        tsRes = Helper.evalExpression(exp, {'A': ts})
        self.compareTS(tsExp, tsRes[0])
    
    def testError(self):                    self.errorBehaviour()    
    def testCopyNamedTS(self):              self.copyNamedTS()
    def testCopyNamedTSAlternative(self):   self.copyNamedTSAlternative()
    def testCopyIgnoreFirstTS(self):        self.copyIgnoreFirstTS()
    def testCopyIgnoreSecondTS(self):       self.copyIgnoreSecondTS()
    def testfirstComeFirstServe(self):      self.firstComeFirstServe()
    def testEmptyTS(self):                  self.emptyTS()
    def testAlignedAddIntIndex(self):       self.alignedAddIntIndex()
    def testAlignedSubIntIndex(self):       self.alignedSubIntIndex()
    def testAlignedMultiIntIndex(self):     self.alignedMultiIntIndex()
    def testAlignedDivIntIndex(self):       self.alignedDivIntIndex()
    def testAlignedPowIntIndex(self):       self.alignedPowIntIndex()
    def testAlignedAddFloatIndex(self):     self.alignedAddFloatIndex()
    def testAlignedSubFloatIndex(self):     self.alignedSubFloatIndex()
    def testShiftForward(self):             self.shiftForward()
    def testShiftBack(self):                self.shiftBack()
    def testMultiInt(self):                 self.multiInt()
    def testMultiReal(self):                self.multiReal()
    def testAddInt(self):                   self.addInt()
    def testAddReal(self):                  self.addReal()
    def testPowAdd(self):                   self.powAdd()
    def testAddString(self):                self.addString()
    def testUminus(self):                   self.uminus()
    def testLogicalMean(self):              self.logicalMean()
    def testLogicalMax(self):               self.logicalMax()
    def testLogicalMin(self):               self.logicalMin()
    def testPhysicalMeanSimple(self):       self.physicalMeanSimple()
    def testPhysicalMeanWithEmptyTS(self):  self.physicalMeanWithEmptyTS()
    def testPhysicalMeanWithPropCopy(self): self.physicalMeanWithPropCopy()
    def testPhysicalOpenClose(self):        self.physicalOpenClose()
    def testAnd(self):                      self.tAnd()
    def testOr(self):                       self.tOr()
    def testXor(self):                      self.tXor()
    def testGreater(self):                  self.greater()
    def testLower(self):                    self.lower()
    def testGreaterEqual(self):             self.greaterEqual()
    def testLowerEqual(self):               self.lowerEqual()
    def testEqual(self):                    self.equal()
    def testNotEqual(self):                 self.notEqual()
    def testIfOtherwise(self):              self.ifOtherwise()
    def testAssign(self):                   self.assignment()
    def testLog(self):                      self.log()
    def testFuncCall(self):                 self.funcCall()
    def testSemicolon(self):                self.semicolon()
    def testPipe(self):                     self.pipe()
    def testCount(self):                    self.count()
    def testCountWithEmptySlots(self):      self.countWithEmptySlots()
    def testCountPipe(self):                self.count_pipe()
    
if __name__ == "__main__":
    unittest.main()
