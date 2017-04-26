from formula3.PythonTimeStamp import TimeStamp

import copy

import time

try:
    from at.ac.ait.enviro.tsapi.timeseries import TimeSeries
except ImportError:
    print "Unable to import TimeSeries from java"
    from formula3.PythonTimeSeries import TimeSeries

try:
    from at.ac.ait.enviro.tsapi.timeseries import TimeInterval
except ImportError:
    from formula3.PythonTimeInterval import TimeInterval


import formula3.ast_parser
import formula3.ast_interpreter

VALUE_VKEY = 'value:value'  # Note: This is NOT "ts:value" on purpose
TEST_VKEY = 'value:test'


# A lightweight implementation of a slot dedicated for python tests. Just what's needed and nothing more
# This is NOT derived from the java variant on purpose to not have java's overhead when debugging
class SlotForTests:
    
    def __init__(self):
        self.data={}

    def __repr__(self):
        return repr(self.data)
        
    def put(self, name, value):
        self.data[name]=value
        
    def get(self, name):
        return self.data[name]


# A lightweight implementation of a timeseries dedicated for python tests
# This is NOT derived from the java variant on purpose to not have java's overhead when debugging
class TimeSeriesForTests:
    
    def __init__(self):
        self.ts_properties={}
        self.data={}
    
    def setTSProperty(self, name, value):
        self.ts_properties[name]=value

    def setSlot(self, time, slot):
        self.data[time]=slot

    def setValue(self, timestamp, key, value):
        if not timestamp in self.data:
            slot = SlotForTests()
            self.data[timestamp]=slot
        else:
            slot=self.data[timestamp]
        
        slot.put(key, value)
        
    def getTSKeys(self):
        keys=self.ts_properties.keys()
        return keys 
    
    def getTSProperty(self, name):
        if name in self.ts_properties:
            return self.ts_properties[name]
        else:
            return None 
    
    def getTimeStampsArray(self):
        all_tss=self.data.keys()
        all_tss_sorted=sorted(all_tss) # Note, this works for some mysterious reasons but when it breaks sometimes I would not be astonished. Keep an eye on it
        return all_tss_sorted

    def getTimeStamps(self):
        return self.getTimeStampsArray()

    def getSlot(self, time):
        if time in self.data:
            return self.data[time]
        else: 
            return None
        
    def slice(self, interval):
        tsLow=interval.start
        tsHigh=interval.end
        
        result=TimeSeriesForTests()
        result.ts_properties=copy.copy(self.ts_properties)
        
        allTS=self.getTimeStampsArray()
        for ts in allTS:
            if ts.asMilis()<tsLow.asMilis():
                continue
            if ts.asMilis()>tsHigh.asMilis():
                continue
            
            slot=self.getSlot(ts)
            result.setSlot(ts, slot)
        
        return result



# A lightweight implementation of a timeseriesprocessor dedicated for python tests
# This is NOT derived from the java variant on purpose to not have java's overhead when debugging
class TSPforTests:
    pass

def constructTS(timeStamps, value_keys, **kwargs):
    '''
    Construct a TimeSeries from a given set of time stamps and values
    @param timeStamps: list of time stamps in ms
    @param data: list of values corresponding to timeStamps
    @param valueKey: value key for the value in each slot (default:  TimeSeries.VALUE)
    @additional parameters (**kwargs) -> form name=list where name is the name of the 
      additional slot property to add and list is the list of values (must fit timeStamps in length) 
    '''
    ts = TimeSeriesForTests()
    
    valueKeys=[]
    for name in value_keys:
        name=name.replace("DP", ":")    # A stupid way to write colons into the name
        valueKeys.append(name)

    ts.setTSProperty(TimeSeries.VALUE_KEYS, valueKeys)
    
    for name in value_keys:
        values=kwargs[name] 
        for i, time in enumerate(timeStamps):
            timeStamp=TimeStamp(time)
            value=values[i]
            name=name.replace("DP", ":")    # A stupid way to write colons into the name
            ts.setValue(timeStamp, name, value)
    
    return ts


def printTS(ts):
    '''
    Print a TimeSeries to the console
    
    @param ts:  Input TimeSeries
    '''
    if ts == None :
        print ("No TimeSeries, argument is not defined")
        return
#    vKeys = ts.getTSProperty(TimeSeries.VALUE_KEYS)
    for timestamp in ts.getTimeStamps():
        slot = ts.getSlot(timestamp)
        print (timestamp.toString())
        print '\t'+str(slot)
#            for key in vKeys:
#                value = slot.get(key)
#                print ('\t'+key+': '+str(value))

def evalExpression(expression, timeSeries, debug=0):
    '''
    Create a new Parser and evaluate an expression on a given list of TimeSeries
    
    @param expression:  F3 expression
    @param timeSeries:  List of input TimeSeries
    '''
    parser=formula3.ast_parser.AST_Parser()
    parser.debug=debug
    ast=parser.parse(expression)
    
    interpreter = formula3.ast_interpreter.AST_Interpreter()
    
    tResult=interpreter.evaluate(ast, timeSeries, tsClass=TimeSeriesForTests)
    return [tResult]




def getTimeIntervalFromDates(interval):
    start=interval[0]
    end=interval[1]
    startTime = time.strptime(start, "%Y-%m-%d %H:%M:%S")
    startUT = time.mktime(startTime)
    startUT-=time.timezone  # This correction is needed as the above string should be interpreted as UTC already but will be understood as "local" by the lib
    startUT*=1000
    # startUT/=60    # Use this if you want to debug in minutes. Comment the above line in this case 
    start = TimeStamp(int(startUT))

    endTime = time.strptime(end, "%Y-%m-%d %H:%M:%S")
    endUT = time.mktime(endTime)
    endUT-=time.timezone
    endUT*=1000
    # endUT/=60
    end = TimeStamp(int(endUT))

    return TimeInterval(TimeInterval.Openness.CLOSED, start, end, TimeInterval.Openness.CLOSED)

