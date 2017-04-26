# A lightweight implementation of Timestamp dedicated for python tests
# This is NOT derived from the java variant on purpose to not have java's overhead when debugging
class TimeStamp:
    def __init__(self, ts):
        self._ts = ts
    
    def __eq__(self, other):
        if other==None:
            return False
        if not isinstance(other, TimeStamp):
            return False
        return self._ts==other._ts

    def __ne__(self, other):
        if other==None:
            return True
        if not isinstance(other, TimeStamp):
            return True
        return self._ts!=other._ts

    def __lt__(self, other):
        if other==None:
            return False
        if not isinstance(other, TimeStamp):
            return False
        return self._ts<other._ts

    def __hash__(self):
        return self._ts

    def __str__(self):
        return str(self._ts)

    def __repr__(self):
        return repr(self._ts)
        
    def asMilis(self):
        return self._ts
