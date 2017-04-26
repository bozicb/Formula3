from formula3.exceptions.exception import Formula3Exception
import math
import formula3.utils.SLF4J2PyLogging


al= formula3.utils.SLF4J2PyLogging.getLogger("formula3.aggregates")


class none_aggregate():
    ''' A special aggregate that does *nothing' '''
    
    def getValueKeys(self, valueKey):
        ''' Communicate to F3 whether this operator will return a dict and if yes, which names it will have.
            return a string if only one value is given back.
            return an array if a dict will be given back 
        '''
        return valueKey

    
    def calc(self, sliceInfo):
        ''' A simple "aggregate" which is used, when no aggregate is given.
            Simply get back the value under the valueKey currently'''
        
        tsSlice=sliceInfo[0]
        valueKey=sliceInfo[1]
        t=sliceInfo[2]
        TS=sliceInfo[3]
        
        if len(tsSlice)==0:
            return None

        sl=tsSlice[0]
        ts=sl.timeStamp
        if ts==None:        # for some reason this signals an invalid slice. We should make this more clear
            return None
        slot=sl.slot
        try:
            result=slot[valueKey]
        except:
            raise Formula3Exception("TimeSeries does not contain the value key " + valueKey)

        return result
            



class calc_mean():

    def getValueKeys(self, valueKey):
        ''' Communicate to F3 whether this operator will return a dict and if yes, which names it will have'''
        return valueKey
    
    # slice: The list of all slots needed for the aggregate
    # t: the time of the result
    def calc(self, sliceInfo):

        tsSlice=sliceInfo[0]
        valueKey=sliceInfo[1]
        t=sliceInfo[2]
        TS=sliceInfo[3]

        
    #    print("calculating the mean for " + str(t))
    
        if tsSlice==None or len(tsSlice)==0:
            return None   # This will signal the caller that there is no result
        
        sum=0
        count=0
        for slot in tsSlice:
            if valueKey in slot:
                op=slot[valueKey]
            else:
                op=None
            
            if op!=None:
                sum+=op
                count+=1
        
        sum=sum/(count * 1.0) if count>0 else None  # ... * 1.0 --> force count to be a float so that the div is float arithmetic
    
        return sum 

    def calcAsFunction(self, argument):
        return argument







#calc_my_mean calculates the meanValue WITH Status Bits
#In addition to the default ValueKey (ts:value), it requires
# "GStat" and "FStat"
#Statusbits are bitwise ORed, values with FStat != 0 are not used for meanValues.
#JCS: This is what I need to do if I want to do it my way:
#Just copy calc_mean, change whatever I need to, and
#make the new operator (or aggregate) public in globales.py
#Very simple.
class calc_my_mean():
#{

    #define required valueKeys
    vKGStat = "DevStat"
    vKFStat = "ErrStat"
    vKIStat = "IntStat"
    vKValue = "None"       # e.g. ts:value, or default
    availLimit1= 50         #less than 50% of the values in a slice are valid (e.g. ErrStat = IntStat = 0)
    availLimit2= 90         #more than 90% of the values in a slice are valid 
    HMWBit_availLimit1= 0x0100
    HMWBit_availLimit2= 0x0200
    
    tsName = "Who_am_I?"


    def getValueKeys(self, valueKey):
    #{
        return valueKey + [calc_my_mean.vKGStat, calc_my_mean.vKFStat, calc_my_mean.vKValue]
    #}
    
    def calc(self, sliceInfo):
    #{
        tsName = "Who_am_I?"
    
        tsSlice=sliceInfo[0]
        valueKey=sliceInfo[1]
        t=sliceInfo[2]
        TS=sliceInfo[3]

    
        # Now start with calculation.
        # Assumption: Structure of Slots does not change
        sum = 0
        goodValues = 0
        badValues = 0
        meanValue = 0
        currentValue = 0
        currentGStat = 0
        currentFStat = 0
        meanGStat = 0     #DeviceStatus
        meanFStat = 0     #ErrorStatus
        meanIStat = 0     #Internal Processing Status
    
        #Step through every Slot
        for currentSlot in tsSlice:               # slice is a list of slots
        #{
            if currentSlot == None:
            #{
                al.debug("currentSlot was None!")
                continue
            #}
            if not valueKey in currentSlot:
            #{
                al.debug("currentSlot was empty!")
                continue
            #}
            al.debug("currentSlot is " + str(currentSlot))
        
            #Here is Error Checking
            try:
                currentValue = currentSlot[valueKey]  # op= operand (15degC)
            except KeyError:
                raise Formula3Exception("TimeSeries " + tsName + " does not contain required ValueKey " + valueKey)
            
            try:
                currentGStat = currentSlot[calc_my_mean.vKGStat]   # e.g. 0x01
            except KeyError:
                raise Formula3Exception("TimeSeries " + tsName + " does not contain required ValueKey " + calc_my_mean.vKGStat)
        
            try:    
                currentFStat = currentSlot[calc_my_mean.vKFStat]   # e.g. 0x00
            except KeyError:
                raise Formula3Exception("TimeSeries " + tsName + " does not contain required ValueKey " + calc_my_mean.vKFStat)
            
            try:    
                currentIStat = currentSlot[calc_my_mean.vKIStat]   # e.g. 0x00
            except KeyError:
                raise Formula3Exception("TimeSeries " + tsName + " does not contain required ValueKey " + calc_my_mean.vKIStat)

            #Here starts the actual meanvalue processing
            al.debug("CurrentValues: " + str(currentValue) + " " + str(currentGStat) + " " + str(currentFStat) + "; sum: " + str(sum) + " / " + str(goodValues))
            if currentFStat == 0:                # only good values are used for building mean values
            #{
                sum += currentValue
                goodValues += 1
            #}
            else:
            #{
                badValues += 1
            #}
            meanGStat |= currentGStat                #Bitwise OR for Error and Device Status
            meanFStat |= currentFStat
            meanIStat |= currentIStat
        #}
      
        totalValues= goodValues + badValues
        if (goodValues < 1):
        #{
            al.info("TimeSeries " + tsName + " does not contain any valid values for the requested interval! Availability is 0")
            availability= 0 
            meanValue=float('nan')
        #}
        else:     #There are some good Values -> Calculate meanValue
        #{
            availability= (goodValues*100) / totalValues  #Percentage of useful values
            meanValue = sum / (goodValues * 1.0) if goodValues > 0 else None  # ... * 1.0 --> force goodValues to be a float so that the div is float arithmetic
        #}
      
        #Set HMW Bytes
        if availability < calc_my_mean.availLimit1:     # typ: 50%
        #{
            meanIStat |= calc_my_mean.HMWBit_availLimit1
        #}
        if availability < calc_my_mean.availLimit2:     # typ: 90%
        #{
            meanIStat |= calc_my_mean.HMWBit_availLimit2
        #}
        al.debug ("TimeSeries %s %.2f | GStat 0x%x | FStat 0x%x | IStat 0x%x | %3.1f%% (%d/%d)" %(tsName, meanValue, meanGStat, meanFStat, meanIStat, availability, goodValues, totalValues)) 
#      meanIStat |= (0xFF000000 & (byte(availability)*0x1000000))
      
        #Pack everything into one Slot and return it in a container
        #(Yes, input is many slots, but out goes only one.)
        resultSlot = dict()
        resultSlot[valueKey] = meanValue
        resultSlot[calc_my_mean.vKFStat] = meanFStat
        resultSlot[calc_my_mean.vKGStat] = meanGStat
        resultSlot[calc_my_mean.vKIStat] = meanIStat
        return (resultSlot, valueKey) 





class calc_max():
    
    def getValueKeys(self, valueKey):
        ''' Communicate to F3 whether this operator will return a dict and if yes, which names it will have'''
        return valueKey

    def calc(self, sliceInfo):
    
    
        tsSlice=sliceInfo[0]
        valueKey=sliceInfo[1]
        t=sliceInfo[2]
        TS=sliceInfo[3]

        if len(tsSlice)==0:
            return None   # This will signal the caller that there is no result
        
        maxValue=None
        firstSlot=None                  # Very pragmatic: Use the first slot that's not None as a template for the result
        for slot in tsSlice:
            if valueKey in slot:
                op=slot[valueKey]
                if firstSlot==None:
                    firstSlot=slot
            else:
                op=None
            
            if op==None:
                continue
            
            maxValue=max(maxValue, op)
                
        return maxValue  


class calc_min():
    
    def getValueKeys(self, valueKey):
        ''' Communicate to F3 whether this operator will return a dict and if yes, which names it will have'''
        return valueKey

    
    def calc(self, sliceInfo):

        tsSlice=sliceInfo[0]
        valueKey=sliceInfo[1]
        t=sliceInfo[2]
        TS=sliceInfo[3]
        
        if len(tsSlice)==0:
            return None   # This will signal the caller that there is no result
    
        minValue=None
        firstSlot=None                  # Very pragmatic: Use the first slot that's not None as a template for the result
        for slot in tsSlice:
            if valueKey in slot:
                op=slot[valueKey]
                if firstSlot==None:
                    firstSlot=slot
            else:
                op=None
            
            if op==None:
                continue
            
            minValue= min(minValue, op) if minValue!=None else op
            
        return minValue 



class calc_sum():
    
    def getValueKeys(self, valueKey):
        ''' Communicate to F3 whether this operator will return a dict and if yes, which names it will have'''
        return valueKey

    def calc(self, sliceInfo):
        return


class calc_count():
    
    def getValueKeys(self, valueKey):
        ''' Communicate to F3 whether this operator will return a dict and if yes, which names it will have'''
        return valueKey

    
    def calc(self, sliceInfo):


        tsSlice=sliceInfo[0]
        valueKey=sliceInfo[1]
        t=sliceInfo[2]
        TS=sliceInfo[3]

        if tsSlice==None:
            return 0
    
        count=0
        for slot in tsSlice:
            if valueKey in slot:
                op=slot[valueKey]
            else:
                op=None
            
            if op==None:
                continue
            
            count=count+1
        
        return count 


class calc_log():

    def getValueKeys(self, valueKey):
        ''' Communicate to F3 whether this operator will return a dict and if yes, which names it will have'''
        return valueKey

    def calc(self, sliceInfo):
        
        tsSlice=sliceInfo[0]
        valueKey=sliceInfo[1]
        t=sliceInfo[2]
        TS=sliceInfo[3]

        
        if len(tsSlice) != 1:
            raise Formula3Exception("Log calculation of interval not possible!")
        slot = tsSlice[0]
        value=slot[valueKey]
        return math.log(value) 


    def calcAsFunction(self, argument):
        # Note: This is hairy. No type checking or anything. This will surely break once we are beyond the prototype phase of function calls. 
        return math.log(argument)
