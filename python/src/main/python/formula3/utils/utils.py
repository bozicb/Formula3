import copy
import array


import formula3.AST as AST


try:
    from at.ac.ait.enviro.formula3 import JythonHelper 
#    print "Imported JythonHelper from java"
except ImportError:
#    print "Unable to import JythonHelper from java"
    JythonHelper=None    
            # We only need this package when we run in a java environment. 
            # In this case we don't expect this exception
            # Otherwise: just ignore

try:
    from at.ac.ait.enviro.tsapi.timeseries import TimeSeries
except ImportError:
#    print "Unable to import TimeSeries from java"
    from formula3.PythonTimeSeries import TimeSeries

from formula3.exceptions.exception import Formula3Exception

import formula3.utils.SLF4J2PyLogging
logger=formula3.utils.SLF4J2PyLogging.getLogger("F3_utils")

def isTimeSeries(obj):
    '''
    Returns if the input parameter is a TimeSeries object
    @param obj: object to check 
    @return: True, if the parameter is a TimeSeries object
    '''
    return isinstance(obj, TimeSeries)

def isSlice(obj):
    '''
    Returns if the input parameter is a TimeSeries slice
    @param obj: object to check 
    @return: True, if the parameter is a TimeSeries slice
    '''
    
    # well, a slice should be a dict. this should be more sophisticated in the future
    if isinstance(obj, tuple) and len(obj)==2:
        return True
    return isinstance(obj, list) or isinstance(obj, dict)   # This is old-style. TODO: find out if still in use and remove 



def isNumber(obj):
    '''
    Returns if the input parameter is a number 
    @param obj: object to check 
    @return: True, if the parameter is a number
    '''    
    return isinstance( obj, (int,long,float) )


def deepcopy(x):
    '''Using an own deepcopy method here as the provided one breaks under some circumstances
       Approach: copy.deepcopy everything but arrays (array.array)
                 copy.deepcopy those too, if the type code is NOT java.lang.string  
    '''    
    
    #print "about to deepcopy an object of type "+str(type(x))
    if not isinstance(x, array.array):
        return copy.deepcopy(x)

    tc=x.typecode
    #print "About to copy an array with a typecode of "+tc
    if tc!="java.lang.String":
        return copy.deepcopy(x)

    result=JythonHelper.createStringArray()
    for o in x:
        #print "About to copy a list --> copying a "+str(type(x))
        result.append(deepcopy(o))
    
    return result
    

def createTimeSeries(ts, tsClass):
    '''
    Creates a TimeSeries with the same properties as the input TimeSeries. The class created is based on tsClass 
    @param ts: basis TimeSeries
    '''   
    newTS = None   
    if tsClass == None:
        raise Formula3Exception("tsClass MUST be defined")
    else :
        newTS = tsClass()
        
    tsKeys = ts.getTSKeys()
    if tsKeys != None:
        for key in tsKeys :
            value = ts.getTSProperty(key)
            # print "About to clone a key of "+key+" with a value of "+str(value)
            value1=deepcopy(value)
            newTS.setTSProperty(key, value1)
    return newTS
   

def copyTimeSeries(ts):
    '''
    Copies all properties of a TimeSeries into a new one
    @param ts: basis TimeSeries
    '''     
    newTS = createTimeSeries(ts)
    for timestamp in ts.getTimeStampsArray():
        newTS.setSlot(timestamp, ts.getSlot(timestamp))
    return newTS

     
def createSlot(slot, ts, valueKey):
    '''
    Creates a Slot with the same properties as the input slot (except value)
    @param slot: basis Slot
    @param ts: basis TS
    @param valueKey: key of the "value" 
    @return: A new Slot
    '''  
    newSlot = {}
    valueKeys = ts.getTSProperty(TimeSeries.VALUE_KEYS)
    if valueKeys != None:
        for key in valueKeys:
            if (valueKey != None and valueKey != key):
                newSlot.put(key, slot.get(key))
    return newSlot


def getSlotFromTSAsDic(timeStamp, ts):
    '''
    Creates a dictionary with the values of the slot associated with the input TimeStamp
    @param timeStamp: TimeStamp of basis Slot
    @param ts: basis TS
    @return: A new dict
    '''  
    slot = ts.getSlot(timeStamp)
    
    return getSlotAsDic(slot, ts)

def getSlotAsDic(slot, ts):
    '''
    Creates a dictionary with the values of the input slot 
    @param slot:  basis Slot
    @param ts: basis TS
    @return: A new dict
    '''  
    slotDic = dict()
    valueKeys = ts.getTSProperty(TimeSeries.VALUE_KEYS)
    if valueKeys != None:
        for key in valueKeys:
            slotDic[key] = slot.get(key)
    return slotDic


def setSlot(resultTS, slotDic, ts):
    ''' Fills in a ts' slot from a dictionary.
        It is assumed that the timeSeries is prepared to accept all entries 
        from slotDic.
        Note that we do NOT set the slot directly to allow the time series to 
        choose the best slot implementation to use 
    '''

    value_keys=resultTS.getTSProperty(TimeSeries.VALUE_KEYS)
    if value_keys==None:
        value_keys=[]   # This fallback should be avoided as it will not work with the java framework

    # First step, find out which keys are in the new slot that are missing in the time series' value keys
    changed=False
    i=0;
    for key in slotDic.iterkeys():
        i += 1
        if not key in value_keys:   # This usually happens when the first slot of a new virgin time series is written
            logger.debug("setSlot appended key " + str(key) + " at position " + str(i))
            #value_keys=list(value_keys)
            #logger.debug("Value keys type changed to "+str(type(value_keys))
            value_keys.append(key) 
            changed=True
            # print "setSlot has new Length: " + str(len(value_keys))

    # Second step. If there are any missing, write the new keys to the TS 
    if changed:
        logger.debug("Writing back a value keys array of " + str(value_keys))
        resultTS.setTSProperty(TimeSeries.VALUE_KEYS, value_keys)

    # 3. Step and this is the essence of this routine:
    # Write the values 
    for key, value in slotDic.iteritems():
        resultTS.setValue(ts, key, value)



def updateDictDecently(existingDict, newValue, newName):
    '''Set all values (or the one) from newValue but only if the name does not exist already.
       newValue is either a dict; in this case newName is ignored and names are taken from newValue 
       otherwise the newValue is written to newName
    '''
    
    if isinstance(newValue, dict):
        for name, value in newValue.iteritems():
            if not (name in existingDict):
                existingDict[name]=value
        
        return

    if not (newName in existingDict):
        existingDict[newName]=newValue

    return


def updateListDecently(existingList, newList):
    '''Add all values of a list to another list
       but only if the value does not exist already.
       Note: Does in-place modification of the existing list
       '''
    for e in newList:
        if not e in existingList:
            existingList.append(e)

    return existingList



def findBestValidSlotInSlice(slice, t):
    ''' 
        Find the slot for t (t=timestamp). If that slot is not available for some reason...
        ...find the best valid slot (i.e. the first slot with a defined time stamp) in a dict of slices'''

    secondBestSC=None    
    for sc in slice:
        if sc.timeStamp==t:
            return sc
        if secondBestSC==None and sc.timeStamp!=None:
            secondBestSC=sc
    return secondBestSC
    

def findFirstTS(node):
    '''
     Tries to find the first node with 'SLICE'
     @param node: AST node (tuple)
    '''

    if not isinstance(node, dict):
        typeName=str(type(node))
        raise Formula3Exception("findFirstTS called with a datatype of %s" % (typeName))

    nodeType=node["type"]

    if nodeType == AST.TYPE_SLICE or nodeType=='PROPCOPY':
        return node

    if nodeType == 'generator' :
        for expressionInfo in node["expressions"]:
            expression=expressionInfo[0]
            TS=findFirstTS(expression)
            if TS!=None:
                return TS

    if nodeType == 'BINOP':
        TS=findFirstTS(node["left"])
        if TS == None:
            return findFirstTS(node["right"])
        return TS

    if nodeType == 'IFOT':
        TS = findFirstTS(node["condition"])
        if TS == None:
            TS = findFirstTS(node["true"])
        if TS == None:
            TS = findFirstTS(node["false"])
        return TS

    if nodeType == 'ASSIGN':
        TS=findFirstTS(node["left"])
        return TS

    if nodeType == 'UMINUS':
        TS=findFirstTS(node['operand'])
        return TS

    if nodeType == 'SEMICOLON':
        leftNode=node['left']
        TS=findFirstTS(leftNode)
        if TS!=None:
            return TS
        rightNode=node['right']
        TS=findFirstTS(rightNode)
        return TS
    
    if nodeType == AST.TYPE_FUNCCALL:
        argument_list=node[AST.ARG_LIST]
        for arg in argument_list:
            TS=findFirstTS(arg)
            if TS!=None:
                return TS
        return None

    raise Formula3Exception("findFirstTS called with an unknown node type of %s" % (nodeType))
 


def findFirstTSName(node):
    '''
    Tries to find the first node that mentions a TS name.
    Currently this is either a TS access node or a property copy operator.
    @param node: AST node (tuple) 
    '''
    
    if not isinstance(node, dict):
        return None

    nodeType=node["type"]
        
    if nodeType == AST.TYPE_SLICE :
        name=node["id"]
        return name

    if nodeType == 'PROPCOPY' :
        name=node["id"]
        return name

    if nodeType == 'generator' :
        for expressionInfo in node["expressions"]:
            expression=expressionInfo[0]
            TS=findFirstTSName(expression)
            if TS!=None:
                return TS

    if nodeType == 'BINOP':
        TS=findFirstTSName(node["left"])
        if TS == None:
            return findFirstTS(node["right"])
        return TS
    
    if nodeType == 'IFOT':
        TS = findFirstTSName(node["condition"])
        if TS == None:
            TS = findFirstTSName(node["true"])
        if TS == None:
            TS = findFirstTSName(node["false"])
        return TS

    if nodeType == AST.TYPE_FUNCCALL:
        TS = None
        arg_list=node[AST.ARG_LIST]
        for arg in arg_list:
            TS = findFirstTSName(arg)
            if TS!=None:
                break
        return TS

    
    if nodeType == 'ASSIGN':
        TS=findFirstTS(node["left"])
        return TS
    
    if nodeType == 'UMINUS':
        TS=findFirstTSName(node['operand'])
        return TS
    
    if nodeType == 'SEMICOLON':
        leftNode=node['left']
        TS=findFirstTS(leftNode)
        if TS!=None:
            return TS
        rightNode=node['right']
        TS=findFirstTS(rightNode)
        return TS


    raise Formula3Exception("findFirstTSName called with an unknown node type of %s" % (nodeType))

    

def isNumTS(node):
    '''
    Tries to evaluate if the given TS has a "numerical" boundary 
    @param node: AST node (tuple) 
    '''
    if node["type"] == "PROPCOPY":
        return False;
    
    if node["type"] != AST.TYPE_SLICE :
        raise Formula3Exception('Expecting TS node! Received '+`node[0]`)
    
    boundary = getBoundary(node)           
    return True if isinstance(boundary, (int, long)) else False


def getBoundary(node):
    '''
    Returns the  boundary of an AST TS node 
    @param node: AST node (tuple) 
    '''
    if node["type"] != AST.TYPE_SLICE :
        raise Formula3Exception('Expecting TS node! Received '+`node[0]`)
    
    return node["interval"]
    
def getValueKey(ts_access_node, ts):
    '''
    Returns the  valueKey of an AST TS node 
    @param node: AST node (tuple) 
    '''
    type_name=ts_access_node["type"]
    
    if not type_name in (AST.TYPE_SLICE, 'PROPCOPY') :
        raise Formula3Exception('Expected a TS or PROPCOPY node! Received '+`ts_access_node`)
    
    
    if ts_access_node["property"]!='':
        return ts_access_node["property"]
    else:
        value_keys=ts.getTSProperty(TimeSeries.VALUE_KEYS)
        if value_keys==None:
            raise Formula3Exception('The time series has no VALUE_KEYS property')

        type_of_vk=type(value_keys)
        type_of_vk_name=type_of_vk.__name__
        
        if not type_of_vk_name in ('list', 'array'):
            raise Formula3Exception("The time series' VALUE_KEYS property is not a list/array but a " + type_of_vk)

        if len(value_keys)==0:
            raise Formula3Exception('The time series has an empty VALUE_KEYS property')
            
        return value_keys[0]
    
def createTimeSeriesList(node):        
    '''
    Creates a list with the slices nodes from an AST
    @param node: AST node
    @return: A new list
    '''  
    tsList = []
    findTS(node, tsList)
    return tsList
    
def findTS(node, tsList):
    '''Subroutine for createTimeSeriesList(node)'''
#    print "findTS called with " + str(node)
    
    if isinstance(node, dict) and (node["type"] == AST.TYPE_SLICE or node["type"]=='PROPCOPY'):
        tsList.append(node)
        return
    
    if isinstance(node, (tuple, list)):
        for entry in node:
            if isinstance(entry, (tuple, dict)):   
                findTS(entry, tsList)    

    if isinstance(node, dict):
        for key, entry in node.items():
            if isinstance(entry, (tuple, dict, list)):   
                findTS(entry, tsList)    
 

#    if (isinstance( node[1], tuple )): 
#        findTS(node[1], tsList)    
#    if (len(node)>2) and isinstance( node[2], tuple):
#        findTS(node[2], tsList)

def indexInRange(index, list):
    ''' Returns if a index lies in an array (without negative indexes) '''
    return True if len(list) > index and 0 <= index else False

def indexInRangeNeg(index, list):
    ''' Returns if a index lies in an array (with negative indexes) '''
    return True if len(list) < index and len(list) <= (- index) else False


def getTSInterval(timeSeries):
    '''
    Find the time range covered by a time series.
    The preferred method to do so is using the property REQUEST_INTERVAL.
    If that is not available, fall back to getting the time stamps from TS itself
    '''
    interval=timeSeries.getTSProperty(TimeSeries.REQUEST_INTERVAL)
    if interval!=None:          # This should do some more sanity checking but the next line will fail disgraceful anyway if the object is not a TimeInterval
        start=interval.getStart()
        end=interval.getEnd()
        return (start, end) 

    allTSFromData=timeSeries.getTimeStampsArray()
    if len(allTSFromData)==0:
        return (None, None)
    
    firstTS=allTSFromData[0]
    lastTS=allTSFromData[-1]
    
    return (firstTS, lastTS)


def getEmptySlot(TS):
    ''' Get an "empty slot" from a time series
        Get a simple replacement if the time series does not provide one
    '''
    
    valueKeys=TS.getTSProperty(TimeSeries.VALUE_KEYS)
    
    emptySlot={}
    for key in valueKeys:
        emptySlot[key]=0    # Even better: Get the "empty" values from the TS itself
    
    return emptySlot


def intervalDescFromAST(ast):
    '''Creates a text from the interval part of an ast.
       This is a convenience method and also used for key generation in a slice dictionary during
       expression evaluation
    '''
    brackets={("left", "CLOSED"): "[", ("right", "CLOSED"): "]", ("left", "OPEN"): "(", ("right", "OPEN"): ")"}
    intType=ast["type"]
    left=ast["left"]
    right=ast["right"]
    leftType =left["type"]
    rightType=left["type"]
    leftOffset=left["offset"]
    rightOffset=right["offset"]
    lBracket=brackets[("left", leftType)]
    rBracket=brackets[("right", rightType)]

    if intType=="LOGICAL":
        # Index "n", offsets integers
        leftText="n+%d" % (leftOffset)
        rightText="n+%d" % (rightOffset)
    else:
        # Index t, offset time diffs
        leftText="t+%d%s" % leftOffset
        rightText="t+%d%s" % rightOffset
    
    result="%s%s..%s%s" % (lBracket, leftText, rightText, rBracket)
    
    return result
##########################################
## Time Series Patterns  #################
##########################################

# TS Patterns are dictionaries (indeed quadrupels as the numbers have units) of values that define a regular 
# pattern of points in time that span from -INFINITY to + INFINITY. 
# The way to describe these is to choose an arbitrary point in time defined as 0. 
# We choose the very common UNIX 1970 epoch for that.
# Starting at this point a pattern is defined by a period (the distance between to points)
# and a phase (the offset from zero to the first point)

# Patterns can have many units to accommodate to the way users think
# Internally each unit but months and years can be expressed as a multiple of milliseconds.
# We use that to "normalize" the patterns to make further processing easier
#
# A thought about the implementation. This is a pure python implementation. 
# Do we have a java implementation for this as well?
# Decision (gd 4.2.2011: We first implement and test the algorithms and AFTERWARDS look
# for enhancements and re-use of existing java stuff. The java stuff is in the way anyway when we want to
# make coverage analysis 
      

# Define the factors for different units as well as the base unit
# This list iteratively used until a unit is broken down to one of the base units 
# Note, that this list should be kept in sync with the units defined by the F3 lexer
time_unit_factors = {
            "ms": (1, "ms"),
            "secs": (1000, "ms"),
            "sec" : (1000, "ms"),
            "min" : (60, "sec"),
            "mins": (1, "min"),
            "hours": (60, "min"), 
            "hour": (60, "min"),
            "days": (24, "hour"),
            "day" : (24, "hour"),
            "weeks": (7, "day"),
            "week": (7, "day"),
            # Note: Units Month and year are not implemented yet
                    } 

base_unit_list=("ms", "month", "year")

def normalizeTimeValue(timeValue):
    ''' Convert a pair (value, unit) to the base unit.
    '''
    value=timeValue[0]
    unit=timeValue[1]
    
    while (not unit in base_unit_list):
        if not unit in time_unit_factors:
            raise Formula3Exception("unknown unit %s . This is an internal programming error" % (unit))
        conversion=time_unit_factors[unit]
        value*=conversion[0]
        unit=conversion[1]

    return (value, unit)




def normalizeTimePattern(pattern):
    ''' Get a time series pattern with any unit and reduce it to the base unit (milliseconds))
        parameter pattern: a dict is expected here with the members periodValue, periodUnit, phaseValue, phaseUnit
    '''
    period=(pattern[0], pattern[1])
    period_norm=normalizeTimeValue(period)
    
    phase=(pattern[2], pattern[3])
    phase_norm=normalizeTimeValue(phase)
    
    if period_norm[1]!=phase_norm[1]:
        raise Formula3Exception("Phase and period are not compatible") # To be discussed. Is it a good idea to check this here?

    # Now make sure that the phase is positive and smaller than the period
    # The while loops are a fast and simple approach. Please don't torture them with very large numbers. 
    # It will work but might take painfully long.
    # BTW, it is not a clever idea to call this with a period of <=0. Besides....what would that mean anyway?
    phase_corrected=phase_norm[0]
    while phase_corrected<0:
        phase_corrected+=period_norm[0]

    while phase_corrected>period_norm[0]:
        phase_corrected-=period_norm[0]
    
    return (period_norm[0], period_norm[1], phase_corrected, phase_norm[1])



def findBestTimeStamp(timePattern, shift, timestamp, upper):
    '''Find the largest point in time determined by <pattern> and <shift> that is smaller than <timestamp>
       timePattern: A tuple of period and phase, each of them being a pair of value and unit
       shift: an integer value + a unit
       timestamp: an integer value that holds time since time "0"
       Note: this assumes all values to be in the same unit, preferable normalized time patterns and times
    '''
    #  Pattern:  0  ppppppppp  t0+sssss      t1+sssss           t2           t3 (p=phase, s=shift)
    #  time                                            t
    #                                        ^   We look for this timestamp as t is just below t1+ssssss
    
    # Then we shift everything by p:
    
    #  Pattern:  t0+sssss      t1+sssss     t2           t3 (Note: t0 is 0 now)
    #  time                             t    <-- t corrected by sssss
    #                          ^   We look for this timestamp as t is just below t1+ssssss

    # Next we take shift into account
    
    #  Pattern:  t0      t1     t2           t3 (Note: t0 is 0 now)
    #  time                 t  <- t now corrected by sssss
    #                    ^   We look for this timestamp as t is just below t1

    period=timePattern[0]
    phase=timePattern[2]
    
    t_corrected=timestamp-(phase+shift[0])         # change our frame of reference by offsetting everything by <phase> explicitly here, implicitly for the pattern
    nPeriods=int(t_corrected/period)    # Gives the number of complete periods for timestamp
                                        # This relies on int() truncating. Side note: what happens for values <0?

    subPeriods=t_corrected % period
    
    if upper and (subPeriods!=0):       # If we look for the upper border we need one period more but only if the aren't right on spot anyway
        nPeriods+=1
    
    t_largestLower=nPeriods*period  # This is the time when the period happened
    t_largestLower+=phase # revert the change of the reference point but not the shift

    return t_largestLower
    

def findLowTimeStamp(timePattern, shift, timestamp):
    ts=findBestTimeStamp(timePattern, shift, timestamp, False)
    return ts

def findHighTimeStamp(timePattern, shift, timestamp):
    '''Much like findLowTimeStamp but finds the smallest point in time that is larger than <timestamp>'''
    ts=findBestTimeStamp(timePattern, shift, timestamp, True)
    return ts



def materializeTimePattern(timePattern, shiftLow, shiftHigh, tsLow, tsHigh):
    '''Gives back the list of time stamps created by <timePattern> that are between tsLow and tsHigh.
        shiftLow and shiftHigh thereby define the region of interest for each time stamp
    '''
    lowestFromTS =findHighTimeStamp(timePattern, shiftLow, tsLow)
    highestFromTS=findLowTimeStamp(timePattern, shiftHigh, tsHigh) # No, the swap is intended and not a flaw. Make a diagram
    
    result=[]
    t=lowestFromTS
    while t<=highestFromTS:
        result.append(t)
        ####
        t+=timePattern[0]   # +=period
    
    return result

def shift_left(time, time_stamp):
    return time_stamp.asMilis()+time[0]

def shift_right(time, time_stamp):
    return time_stamp.asMilis()+time[0]

#############################################################################################
def F3TreeFormatter(f3Tree, indent):
    result=[]
    
    if isinstance(f3Tree, dict) and "type" in f3Tree and f3Tree["type"]==AST.TYPE_SLICE:
        id=f3Tree["id"]
        property=f3Tree["property"]
        if property!='':
            property="."+property
        intervalInfo=f3Tree["interval"]
        intervalText=intervalDescFromAST(intervalInfo)
        line=(3*indent*' ')+id+property+intervalText
        result.append(line)
        resultString="\n".join(result)
        return resultString

#    if isinstance(f3Tree, dict) and AST.TYPE in f3Tree and f3Tree[AST.TYPE]==AST.TYPE_FUNCCALL:
#        id=f3Tree[AST.ID]
#        arg_list=f3Tree(AST.ARG_LIST)
#    work not finished        
        
    
    if isinstance(f3Tree, dict):        
        for (key, value) in f3Tree.iteritems():
            if isinstance(value, (dict, list, tuple) ):
                continue    # ignore collections in the first pass. Print out values first
            line=3*indent*' '+"%s / %s" % (key, value)
            result.append(line)   
        for (key, value) in f3Tree.iteritems():
            if isinstance(value, (dict, list, tuple) ):
                line=3*indent*' '+key+":"
                result.append(line)
                line=F3TreeFormatter(value, indent+1)
                result.append(line)
                
    if isinstance(f3Tree, (list, tuple)):
        for e in f3Tree:
            line=F3TreeFormatter(e, indent+1)
            result.append(line)
                
    
    resultString="\n".join(result)
    return resultString

def getEmptyStringArray():
    if JythonHelper!=None:
        return JythonHelper.createStringArray()
    
    return []   # Fall back to Python

