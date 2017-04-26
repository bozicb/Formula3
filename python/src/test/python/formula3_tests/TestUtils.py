import unittest

import formula3
import formula3.utils.utils as utils

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testTimeValueNormalisation_base_conversions(self):
        converted=utils.normalizeTimeValue((1, "ms"))
        self.assertEquals((1, "ms"), converted)
        #
        converted=utils.normalizeTimeValue((1, "sec"))
        self.assertEquals((1000, "ms"), converted)
        #
        converted=utils.normalizeTimeValue((1, "min"))
        self.assertEquals((1000*60, "ms"), converted)
        #
        converted=utils.normalizeTimeValue((1, "hour"))
        self.assertEquals((1000*60*60, "ms"), converted)
        #
        converted=utils.normalizeTimeValue((1, "day"))
        self.assertEquals((1000*60*60*24, "ms"), converted)
        #
        converted=utils.normalizeTimeValue((1, "week"))
        self.assertEquals((1000*60*60*24*7, "ms"), converted)

    
    def testTimePatternAlignment(self):
        # A simple test just to make sure the routine is working at all
        converted=utils.normalizeTimePattern((1,"min",1,"sec"))
        self.assertEquals((1000*60, "ms", 1000, "ms"), converted)

        # A strange phase that needs modification (correct upwards) 
        converted=utils.normalizeTimePattern((1,"min", -1,"sec"))
        self.assertEquals((1000*60, "ms", 59000, "ms"), converted)
        
        # More strange things (correct downwards)
        converted=utils.normalizeTimePattern((1,"min", 121,"sec"))
        self.assertEquals((1000*60, "ms", 1000, "ms"), converted)
        


    def testTimeAlignmentUpwards(self):
        # A first trivial case
        pattern=utils.normalizeTimePattern((1, "hour", 0, "min")) # 0:00, 1:00, 2:00, 3:00, ....
        shift=utils.normalizeTimeValue((0, "min"))
        time=(2*60+30) * 60 * 1000  # 2:30.
        timeExpected=(3*60)*60*1000    # 3:00
        result=utils.findHighTimeStamp(pattern, shift, time)
        self.assertEquals(timeExpected, result)

        # trivial, too. Really!
        pattern=utils.normalizeTimePattern((1, "hour", 0, "min")) # 0:00, 1:00, 2:00, 3:00, ....
        shift=utils.normalizeTimeValue((0, "min"))
        time=(2*60) * 60 * 1000  # 2:00
        timeExpected=(2*60)*60*1000    # 2:00
        result=utils.findHighTimeStamp(pattern, shift, time)
        self.assertEquals(timeExpected, result)

        # a case where phase is used
        pattern=utils.normalizeTimePattern((1, "hour", 0, "min")) # 0:00, 1:00, 2:00, 3:00, ....
        shift=utils.normalizeTimeValue((59, "min"))                                         # 0:59, 1:59, 2:59, 3:59, ....
        time=(150)  * 60 * 1000  # 2:30.
        timeExpected=(2*60)*60*1000    # 2:00, as 2:00 + 59 min > 150
        result=utils.findHighTimeStamp(pattern, shift, time)
        self.assertEquals(timeExpected, result)
    
        # another case where phase is used. Note that this time the phase gives a value just a bit below the given time
        pattern=utils.normalizeTimePattern((1, "hour", 0, "min"))   # 0:00, 1:00, 2:00, 3:00, ....
        shift=utils.normalizeTimeValue((29, "min"))                 # 0:29, 1:29, 2:29, 3:29, ....
        time=150 * 60 * 1000  # 2:30
        timeExpected=3*60 *60*1000    # 3:00 as 3:29 is above 2:30 but 2:29 is not
        result=utils.findHighTimeStamp(pattern, shift, time)
        self.assertEquals(timeExpected, result)
    
    
    def testTimeAlignmentDownwards(self):
        # A first trivial case
        pattern=utils.normalizeTimePattern((1, "hour", 0, "min")) # 0:00, 1:00, 2:00, 3:00, ....
        shift=utils.normalizeTimeValue((0, "min"))        
        time=(2*60+30) *60*1000  # 2:30.
        timeExpected=(2*60) *60*1000    # 2:00 as 2:00 is just below 2:30
        result=utils.findLowTimeStamp(pattern, shift, time)
        self.assertEquals(timeExpected, result)

        # Another trivial case. An exact hit on a time mark
        pattern=utils.normalizeTimePattern((1, "hour", 0, "min")) # 0:00, 1:00, 2:00, 3:00, ....
        shift=utils.normalizeTimeValue((0, "min"))        
        time=(2*60) *60*1000  # 2:00.
        timeExpected=(2*60) *60*1000    # 2:00
        result=utils.findLowTimeStamp(pattern, shift, time)
        self.assertEquals(timeExpected, result)

        # a case where phase is used
        shift=utils.normalizeTimeValue((-1, "min"))       # same pattern as above --> 0:59, 1:59, 2:59, 3:59, ....
        time=(2*60+30) *60*1000  # 2:30.
        timeExpected=(2*60) *60*1000    # 2:00 as 1:59 is below 2:30
        result=utils.findLowTimeStamp(pattern, shift, time)
        self.assertEquals(timeExpected, result)
    
        # another case where phase is used. Note that this time the phase gives a value just a bit below the given time
        pattern=utils.normalizeTimePattern((1, "hour", 0, "min")) # 0:00, 1:00, 2:00, 3:00, ....
        shift=utils.normalizeTimeValue((29, "min"))       # 0:29, 1:29, 2:29, 3:29, ....
        time=(2*60+30) *60*1000             # 2:30.
        timeExpected=(2*60) *60*1000     # 2:00 as 2:29 is below 2:30
        result=utils.findLowTimeStamp(pattern, shift, time)
        self.assertEquals(timeExpected, result)
    
    def testMaterializeTimePattern(self):
        #utils.base_unit_list=("min")
        pattern=utils.normalizeTimePattern((1, "hour", 20, "min")) # 0:20, 1:20, 2:20, 3:20, ....
        shiftLow=utils.normalizeTimeValue((-1, "min"))  # [t-1 min .. 
        shiftHigh=utils.normalizeTimeValue((3, "min"))  # .. t+3 min]
        timeLow =(1*60+15) *60*1000                      # 1:15
        timeHigh=(3*60+35) *60*1000                      # 3:35
        # expected result is 1:20 (as 1:20 - 1 min is above 1:15), 2:20, 3:20 (as 3:20 +3 is below 3:35)
        expected=[80*60000, 140*60000, 200*60000]
        result=utils.materializeTimePattern(pattern, shiftLow, shiftHigh, timeLow, timeHigh)
        self.assertEquals(expected, result)
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
