import AST
import ast_lexer
import ast_parser
import ast_interpreter
import ast_time_interpreter_changed_values
import ast_time_interpreter_values_needed

import logging
import logging.handlers

import sys
import traceback

if sys.prefix==None:
    sys.prefix=""   # This is a weird bug in Jython 2.5.2 which prevents importing the profiler

import profile

# os.path.join(sys.prefix, 'share', 'locale')

# The next step is the wrong way. Hiding SLF4J behind python logging would be better but I am under time pressure right now
# We fix that later
try:
   import org.slf4j.LoggerFactory as SLF4J_LoggerFactory
except ImportError:
   import formula3.utils.SLF4J2PyLogging as SLF4J_LoggerFactory
    


from formula3.exceptions.exception import Formula3Exception 

try:
    import at.ac.ait.enviro.formula3.java.TimeSeriesProcessor as TimeSeriesProcessor
except ImportError:
    print "Unable to import TimeSeriesProcessor from java"
    from TSPforTest import TimeSeriesProcessor

def mapMapFromJava(map):
    """ Convert a Map to a Dictionary. """

    if isinstance(map, dict):   # In case this was called from a python environment
        return map

    # From here on we assume this to be a java map    
    result = {}
    iter = map.keySet().iterator()
    while iter.hasNext():
        key = iter.next()
        result[key] = map.get(key)
    return result



class F3CompileHandler(logging.Handler):
    # A class to receive the compile log of the F3 parser
    def __init__(self):
        self.level=logging.DEBUG
        self.buffer=[]

    def handle(self, record):
        """
        """
        expandedMsg=record.msg % record.args
        self.buffer.append(expandedMsg)
        return True


    def getOutput(self):
        return '\n'.join(self.buffer)
    
    def reset(self):
        self.buffer=[]




class TSP_AST(TimeSeriesProcessor):
    '''
    Time Series Processor class.
    '''

    f3_handler=F3CompileHandler()
    f3_logger=logging.Logger("F3CompileHandler")
    f3_logger.addHandler(f3_handler)

    parser = ast_parser.AST_Parser(logger=f3_logger, debug=f3_logger)

    
    def __init__(self):
        '''
        Constructor
        '''
        self.parseLog="Not compiled yet"
        self.TSClass=None # The time series class that's used for the result. Must be overridden
        self.logger=SLF4J_LoggerFactory.getLogger("F3")
        
        self.profiling=False    # This is the default. Use setProfiling to switch it on at runtime

        
    
    def compile(self, expression):
        '''
        Call this to initialize the TSP before you use it
        '''
        self.debug=1 # Should be (will be) setable from the outside
        
        self.expression = expression # Kept for debugging purposes only
        self.logger.debug("Setting up the parser")
        
        TSP_AST.f3_handler.reset()  # Oh oh. I hope this will not lead to problems with multithreading
        
        try:
            self.logger.debug("Parsing the expression %s" % (expression))
            ast=self.parser.parse(self.expression)
        except Formula3Exception:
            self.parseLog=TSP_AST.f3_handler.getOutput()
            self.logger.debug("We got a formula exception during compiling.")
            self.logger.debug("The message is %s" % (self.parseLog))
            raise
        except Exception, e:
            self.logger.debug("We got an unexpected exception during compiling.")
            tb_string=traceback.format_exc()
            self.logger.debug(tb_string)
            self.parseLog=tb_string
            raise
        
        
        self.formalArgList=ast["parameters"]
        self.operator=ast


    def getParseLog(self):
        return self.parseLog

    def setProfiling(self, profiling):
        self.profiling=profiling

        
    def eval(self, tss):
        # Note, tss come in a list indexed numerically
        # the interpreter needs it in a dictionary

        # Check whether formal args and tss have the same length

        interpreter=ast_interpreter.AST_Interpreter()
        interpreter.logger=self.logger

        evaluator = lambda : interpreter.evaluate(self.operator, tss, tsClass=self.TSClass)   # Make a lambda for more convenient access to this expression a few lines down
        result=None # Define result a priori so that it's in the locals() dictionary in case we do run profiling

        if self.profiling:  # if profiling is enabled, call the function twice. Once to do the profiling, once to get the result
                            # Does anybody know of a better way?
            prof = profile.Profile()
            try:
                prof.runctx("result=evaluator()", globals(), locals())
            except SystemExit:
                pass

            import pstats
            import StringIO
            buffer=StringIO.StringIO()
            s=pstats.Stats(prof, stream=buffer)
            s.strip_dirs()
            s.sort_stats(2) # Sort by accumulated times
            s.print_stats()
            self.logger.info("The profile stats are:\n"+buffer.getvalue())

        result=evaluator()
        return (result,) # Convert to array to comply with the F3 specs. This should be done inside the interpreter though
    
     
    def getDataChangedInterval(self, intervalMap):
        
        intervalDict=mapMapFromJava(intervalMap)
        
        time_interpreter=ast_time_interpreter_changed_values.AST_time_interpreter_changed_values()
        result=time_interpreter.evaluate(self.operator, intervalDict)
        
        return result
    
    def getDataNeededIntervals(self, interval):

        time_interpreter=ast_time_interpreter_values_needed.AST_Upstream_Time_Interpreter()
        result=time_interpreter.evaluate(self.operator, interval)
        
        return result
    
    def getParameterInfo(self):
        parameters=self.operator["parameters"]
        
        return parameters
