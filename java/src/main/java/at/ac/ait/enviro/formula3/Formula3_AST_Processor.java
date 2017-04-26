package at.ac.ait.enviro.formula3;

import at.ac.ait.enviro.formula3.java.TimeSeriesProcessor;
import at.ac.ait.enviro.tsapi.operators.AbstractReadProcessor;
import at.ac.ait.enviro.tsapi.operators.WriteProcessor;
import at.ac.ait.enviro.tsapi.timeseries.TimeInterval;
import at.ac.ait.enviro.tsapi.timeseries.TimeSeries;

import java.util.HashMap;
import java.util.Map;

import org.python.core.PyDictionary;
import org.python.core.PyException;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyBoolean;
import org.python.util.PythonInterpreter;
import org.slf4j.LoggerFactory;
import org.slf4j.Logger;

/**
 * This class is used by {@link Formula3_AST_DataHandler}. It implements
 * evaluation of a Formula3-expressions with exactly 1 input and 1 output for
 * TimeSerieses, query intervals and event intervals.
 *
 * @see Formula3_AST_DataHandler
 */
public class Formula3_AST_Processor extends AbstractReadProcessor {

    protected final String f3Expression;
    protected final TimeSeriesProcessor tsp;
    protected final PyObject tspJython;
    
    String id="noId";
    
    Logger logger=LoggerFactory.getLogger(this.getClass().getName()+".noId");
    
    PythonInterpreter interpreter=null; 


    public Formula3_AST_Processor(String expression) {
    	logger.trace("F3 Processor created for expression: {}", expression);
        this.f3Expression = expression;
        this.id=f3Expression;
        logger=LoggerFactory.getLogger(this.getClass().getName()+"."+id);

        interpreter = new PythonInterpreter();
		
        interpreter.exec("import sys");
//        interpreter.exec("print sys.subversion");
//        interpreter.exec("print sys.path");
//        interpreter.exec("print sys.builtin_module_names");

        interpreter.exec("from formula3.TSP_AST import TSP_AST");
        
        PyObject tspClass = interpreter.get("TSP_AST");			// This is the python class object
        if (tspClass==null) {
        	throw new IllegalStateException("Unable to create a F3-python TSP");
        }
//       	PyObject tspObject = tspClass.__call__(new PyString(this.f3Expression));
        
       	tspJython = tspClass.__call__();		// This creates the object from the class. Like TSP_AST() in python

       	
       	try {
       		tspJython.invoke("compile", new PyString(this.f3Expression));
       	} catch(PyException pyx) {
       		PyObject exception=pyx.value;
       		PyObject expClass=exception.__getattr__("__class__");
       		String expName=expClass.__getattr__("__name__").asString();
       		if ("verify_exception".equals(expName)) {
       			String text=exception.__getattr__("text").asString();
       			throw new IllegalArgumentException(text);
       		}
       		Object o=tspJython.invoke("getParseLog");
       		if (! (o instanceof PyString) )
       			throw new IllegalStateException("getParseLog did not return a string.");
       		PyString s=(PyString)o;
       		logger.error("Compiling the expression {} yielded in the following error: {} ", expression, s);
            throw new IllegalArgumentException("There was a compiler Error and the compile log is:" + s);
       	}

       	try {
//       		System.out.println("Trying to import the TimeseriesImpl class object");
       		interpreter.exec("import at.ac.ait.enviro.tsapi.timeseries.impl.TimeSeriesImpl as TimeSeriesImpl");
//       		System.out.println("Succeeded");
//            interpreter.exec("print dir()");
            PyObject tsClass = interpreter.get("TimeSeriesImpl");
            tspJython.__setattr__("TSClass", tsClass);
//            System.out.println("Setting the TSClass should have succeeded");
       	} catch(PyException pyx) {
       		logger.error("Unable to set the TSClass for the python processor.", pyx);
       	}
       	
        this.tsp = (TimeSeriesProcessor)tspJython.__tojava__(TimeSeriesProcessor.class);
    }
    
    public void setId(String id) {
    	this.id=id;
        logger=LoggerFactory.getLogger(this.getClass().getName()+"."+id);        
    }
    

    @Override
    public TimeInterval evalEventInterval(TimeInterval eventInterval) {
    	
    	logger.trace("evalEventInterval called with {}", eventInterval);
    	
    	Map<String, TimeInterval> intervalMap=new HashMap<String, TimeInterval>();
    	intervalMap.put("A", eventInterval);	// The name currently is ignored but that is something that MUST change very soon
    	
    	TimeInterval result=tsp.getDataChangedInterval(intervalMap);

    	logger.trace("--> result is {}", result);
    	
    	return result;
    }

    @Override
    public TimeInterval evalQueryInterval(TimeInterval queryInterval) {

    	logger.trace("evalQueryInterval called with {}", queryInterval);
    	
    	Map<String, TimeInterval> result=tsp.getDataNeededIntervals(queryInterval);
    	// Currently we expect the result to have only one entry
    	logger.trace("--> result is {}", result);

        return result.values().iterator().next();
    }


    public void setProfiling(boolean p) {
    	PyObject pp=new PyBoolean(p);
    	tspJython.invoke("setProfiling", pp);
    }
    
    @Override
    public TimeSeries evalTimeSeries(TimeSeries original) {
    	if (logger.isTraceEnabled()) {
    		int size=original.getTimeStamps().size();
    		logger.trace("Evaluating a time series with {} slots", size);
    	}

    	
    	Map<String, String> parameters=tsp.getParameterInfo();
    	if (parameters.size()>1) {
    		throw new IllegalArgumentException("Multiple arguments to F3 not supported (yet)");
    	}

    	String paramName=parameters.keySet().iterator().next();
    	
    	PyDictionary arguments=new PyDictionary();
    	arguments.put(paramName, original);
    	
    	TimeSeries[] result=null;
    	try {
        	result = tsp.eval(arguments);
    	} catch(RuntimeException rt) {
    		logger.error("Runtimexception thrown in F3 Python eval", rt);
    		throw rt;
    	} catch(Error e) {
    		logger.error("Error thrown in F3 Python eval", e);
    		throw e;
    	}

        if (logger.isTraceEnabled()) {
    		int size=result[0].getTimeStamps().size();
    		logger.trace("The result is a time series with {} slots", size);
    	}
        
    //Workaround with Array Integration Problem in Jython (2.5.1) --> Wurde in 2.5.2 aber geloest!!!
    //Problem: ValueKeys = "Key1", "KeyN", null, null .. variable Number of Nulls
    String[] resultValKeys = (String[]) result[0].getTSProperty(result[0].VALUE_KEYS);
    int resultValKeysLen = resultValKeys.length;
    if (resultValKeys[resultValKeysLen-1] == null)
    {
      int goodValKeysLen = 0;
      for (String key : resultValKeys)
      {
        if (key != null)
        {
          goodValKeysLen++;                               //Get Length for new Array
        }
      }
      String[] goodValKeys = new String[goodValKeysLen];  //Create an Array with fixed length
      int i = 0;
      for (String key : resultValKeys)                    //Fill Array with new keys
      {
        if (key != null)
        {
          goodValKeys[i] = key;
        }
        i++;
      }
      logger.trace("Empty Value Keys found: " + resultValKeys.length+" VALUE_KEYS reduced to " + goodValKeys.length);
      result[0].setTSProperty(result[0].VALUE_KEYS, goodValKeys);  //Finally put the good Value Keys into the new TimeSeries
    }

    return result[0];
    }

	@Override
	public WriteProcessor inverseProcessor() {
		// TODO Auto-generated method stub
		return null;
	}

}
