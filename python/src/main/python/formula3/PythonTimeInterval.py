class TimeInterval(object):
    '''
    A lightweight class that mimics the behaviour of the java twin. It's meant to be used in testing.
    Do NOT use in production environments as it is not thoroughly tested and does only implement a subset 
    of the java functionality (just the routines needed for testing are there)
    If you (that means you. Yes YOU!) find that something is missing ...... just add it instead of moaning :-)
    '''

    class Openness:

        OPEN=True
        CLOSED=False
        
        def __init__(self, o=False):
            self.openness=o


    def __init__(self, left, start, end, right):
#    java: TimeInterval(Openness left, TimeStamp start, TimeStamp end, Openness right)
        '''
        Constructor
        '''
        self.leftOpen=left
        self.start=start
        self.rightOpen=right
        self.end=end
    
    def __eq__(self, other):
        if other==None:
            return False
        if not isinstance(other, TimeInterval):
            return False
        
        if self.leftOpen!=other.leftOpen:
            return False
        if self.rightOpen!=other.rightOpen:
            return False
        if self.start!=other.start:
            return False
        if self.end!=other.end:
            return False
        
        return True

    def __str__(self):
        result=""
        if self.leftOpen:
            result+="("
        else:
            result+="["
        
        result+=str(self.start)
        result+=","
        result+=str(self.end)

        if self.rightOpen:
            result+=")"
        else:
            result+="]"
            
        return result

    def __repr__(self):
        return self.__str__()


    def getStart(self):
        return self.start
    
    def getEnd(self):
        return self.end
