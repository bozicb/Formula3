class TimeSeries(object):
    '''
    This class is a replacement for the TSAPI timeseries and meant to
    allow pure java operations instead of depending from the TSAPI
    Note: It is intended that the keys look differently to the java implementation to find the use of explicit literals
    with at least SOME tests 
    '''
    
    VALUE_KEYS="ts:valuekeys_for_test"
    REQUEST_INTERVAL="requestInterval"
    DEFAULT="DefaultValueIndex"


    def __init__(self):
        '''
        Constructor
        '''
        
