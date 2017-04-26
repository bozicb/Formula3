'''
This package has two usages.
When used in a pure python environment (or one that does not supply SLF4J)
it will give you a pure python logger.
When SLF4J is available, it will instatiate an SLF4J logger.
That way logging will integrate into an existing java application.
'''

try:
    import org.slf4j.LoggerFactory as factory
except ImportError:
    print "Unable to import slf4j from java"
    factory = None # Define the name anyway

import logging

def getLogger(name):
    # print "slf4j is "+str(factory)
    # print "logging is "+str(logging)
    if factory==None:
        return logging.getLogger(name)

    logger=SLF4JPyLogger()
    logger.slf4jlogger=factory.getLogger(name)
    
    return logger


class SLF4JPyLogger:
    '''
    The final goal for this is to support the complete interface of 
    the logging package from python.
    Currently only a subset of functions is implemented.
    Please bear with me and have patience. Or help yourself.
    I am merely the initiator of this class, not it's single owner.
    '''
    
    def __init__(self):
        slf4jlogger=None
        levelTranslation={}
    
    def setLevel(self, level):
        print "Level is about to be set to "+level
        
    
    def debug(self, msg, *args, **kwargs):
        # print "debug called with a message of "+msg 
        return self.slf4jlogger.debug(msg)

    def info(self, msg, *args, **kwargs):
        # print "debug called with a message of "+msg 
        return self.slf4jlogger.info(msg)

    def warning(self, msg, *args, **kwargs):
        # print "debug called with a message of "+msg 
        return self.slf4jlogger.warn(msg)
    
    def error(self, msg, *args, **kwargs):
        # print "debug called with a message of "+msg 
        return self.slf4jlogger.error(msg)

    def critical(self, msg, *args, **kwargs):
        # Note: error and critical are treated the same
        # print "debug called with a message of "+msg 
        return self.slf4jlogger.error(msg)




