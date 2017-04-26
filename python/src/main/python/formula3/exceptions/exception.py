class Formula3Exception(Exception):
    '''
    Basis exception for the Formula3 package
    '''

    def __init__(self, msg):
        self.msg  = msg 
        
    def __str__(self):
        return repr(self.msg)

