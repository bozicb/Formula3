package at.ac.ait.enviro.formula3;

import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.Set;

import org.python.core.PyDictionary;
import org.python.core.PyException;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import at.ac.ait.enviro.formula3.java.TimeSeriesProcessor;
import at.ac.ait.enviro.tsapi.handler.DataHandler;
import at.ac.ait.enviro.tsapi.handler.DataHandler.Access;
import at.ac.ait.enviro.tsapi.handler.Datapoint;
import at.ac.ait.enviro.tsapi.poa.DeviceManager;
import at.ac.ait.enviro.tsapi.timeseries.QueryParameter;
import at.ac.ait.enviro.tsapi.timeseries.TimeInterval;
import at.ac.ait.enviro.tsapi.timeseries.TimeSeries;
import at.ac.ait.enviro.tsapi.util.AbstractDatapoint;
import at.ac.ait.enviro.tsapi.util.DatapointManager;
import at.ac.ait.enviro.tsapi.util.Formula3Expression;


/**
 * This class is internally used by the Formula3Query Datahandler.
 * It implements the basic functionality of offering F3 to the public.
 *
 */


class Formula3Datapoint extends AbstractDatapoint {

	/* The main work is done in getTimeSeries. Look there for details */
	
	static PyObject testTSP=null;	// If this field is set, it's used instead the python TSP. Intended use: dependency injection during unit testing 
	private PythonInterpreter interpreter;
	private Logger logger;
	private PyObject tspClass;
	DeviceManager dm=null;
   		


	public Formula3Datapoint(Properties filter) {
		super(filter);

		logger=LoggerFactory.getLogger(this.getClass().getCanonicalName());
		
        interpreter = new PythonInterpreter();
		
        interpreter.exec("import sys");
//        interpreter.exec("print sys.subversion");
//        interpreter.exec("print sys.path");
//        interpreter.exec("print sys.builtin_module_names");
        
        interpreter.exec("from formula3.TSP_AST import TSP_AST");
        
        tspClass = interpreter.get("TSP_AST");			// This is the python class object
        if (tspClass==null) {
        	throw new IllegalStateException("Unable to create a F3-python TSP");
        }
        
	}

	@Override
	public Map<String, Object> getProperties() {
		Map<String, Object> result=new HashMap<String, Object>();
		return result;
	}

	@Override
	public boolean canRead() {
		return true;
	}


	void setDeviceManager(DeviceManager dm) {
		this.dm=dm;
	}
	
	// This routine has been written three times now. Move it to the utils when we can squeeze the time in
	Properties parseTimeSeriesAdress2Filter(String paramAdress) {
		
		Properties parsedAdress=new Properties();
		
		String[] fields=paramAdress.split("[\\s]*;[\\s]*");
		for (String field : fields) {
			String[] parts=field.split("=");
			
			if (parts.length!=2) {
				throw new IllegalArgumentException("The field " + field + " of the address "+ paramAdress + " is mal-formed.");
			}
			
			String name=parts[0];
			String value=parts[1];
			parsedAdress.setProperty(name, value);
		}
		
		
		return parsedAdress;
	}

	private TimeSeriesProcessor setupF3Interpreter(Formula3Expression formula) {
		PyObject tspObject=null;
		this.logger.trace("Constructing the TSP_AST");
		if (testTSP==null) {
			tspObject = tspClass.__call__();		// This creates the object from the class. Like TSP_AST() in python
		} else {
			tspObject = testTSP;
		}

       	try {
    		this.logger.trace("Compiling the expression");
       		tspObject.invoke("compile", new PyString(formula.getFormula3Expression()));
       	} catch(PyException pyx) {
       		PyObject exception=pyx.value;
       		PyObject exceptionClass=exception.__getattr__("__class__");
       		String exceptionTypeName=exceptionClass.__getattr__("__name__").asString();

       		Object o=tspObject.invoke("getParseLog");
       		if (! (o instanceof PyString) )
       			throw new IllegalStateException("getParseLog did not return a string.");
       		PyString s=(PyString)o;
       		logger.error("Compiling the expression {} yielded in the following error: {} ", formula.getFormula3Expression(), s);

       		if ("Formula3LexerException".equals(exceptionTypeName)) {
       			String text=exception.invoke("__str__").asString();
       			text=text+"\nParser protocol is:\n"+s;
       			throw new IllegalArgumentException(text);
       		}
       		if ("Formula3ParserException".equals(exceptionTypeName)) {
       			String text=exception.invoke("__str__").asString();
       			text=text+"\nParser protocol is:\n"+s;
       			throw new IllegalArgumentException(text);
       		}
       		if ("verify_exception".equals(exceptionTypeName)) {
       			String text=exception.__getattr__("text").asString();
       			throw new IllegalArgumentException(text);
       		}
       		throw new IllegalArgumentException("Exception during compiling:"+formula.getFormula3Expression());
       	}

       	try {
    		this.logger.trace("Configuring the result type");
       		interpreter.exec("import at.ac.ait.enviro.tsapi.timeseries.impl.TimeSeriesImpl as TimeSeriesImpl");
            PyObject tsClass = interpreter.get("TimeSeriesImpl");
            tspObject.__setattr__("TSClass", tsClass);
       	} catch(PyException pyx) {
       		logger.error("Unable to set the TSClass for the python processor.", pyx);
       		throw new IllegalArgumentException("Unable to set the TSClass for the python processor.");
       	}
	    
		this.logger.trace("Converting the jython type to java");
       	TimeSeriesProcessor tsp = (TimeSeriesProcessor)tspObject.__tojava__(TimeSeriesProcessor.class);
       	
       	return tsp;
	}
	
	@Override
	public TimeSeries getTimeSeries(QueryParameter... params)
			throws IllegalStateException {
		
		/*
		 * This routines does the main work for F3 queries.
		 * It does the following steps:
		 * 1. Check parameters for sanity
		 * 2. Create an F3 interpreter (using Jython)
		 * 3. Parse the given expression
		 * 4. Find all datapoints that are input to the F3 expression. 
		 *    During that the given datapoint filters are also cehcked for sanity.
		 * 5. Ask the "data needed" F3 interpreter which amount is needed to calculate the 
		 *    F3 expression at hand combined with the given query interval
		 * 6. Retrieve those time series.
		 * 7. Do the F3 calculation
		 * 8. Give back the result  
		 */
		
		
		// First, check sanity of given parameters
		if (params == null || params.length!=2) {
			throw new IllegalArgumentException("F3 expecteds exactly two query parameters");
		}

		TimeInterval interval=null;
		Formula3Expression formula=null;
		
		for (QueryParameter p : params) {
			if (p instanceof TimeInterval)
				interval=(TimeInterval)p;
			if (p instanceof Formula3Expression)
				formula=(Formula3Expression)p;
		}
		
		if (interval==null)
			throw new IllegalArgumentException("F3 expects one of it's parameters to be a TimeInterval");
		if (formula==null)
			throw new IllegalArgumentException("F3 expects one of it's parameters to be a Formula3Expression");

		this.logger.info("getTimeSeries called with a formula of {} and an interval of {}", formula, interval);
		
		// Now construct a new python TSP object and set it up
       	this.logger.debug("Setting up the expression's processor");
       	TimeSeriesProcessor tsp=setupF3Interpreter(formula);


       	// Get a list of all needed intervals from the operator
       	this.logger.debug("Evaluating the needed input for the formula expression");
       	Map<String, TimeInterval> intervalNeeded=tsp.getDataNeededIntervals(interval);
       	
       	// Next walk the formula parameters and try to get datapoints and then time series
       	Map<String, String> formulaParams=tsp.getParameterInfo();
       	PyDictionary formulaArguments=new PyDictionary();

       	this.logger.debug("Looking up the input for the time series");
       	
       	for (Entry<String, String> e : formulaParams.entrySet()) {

       		// Parse the address string
       		String paramName=e.getKey();
       		String paramAdress=e.getValue();
       		if (paramAdress==null) {
       			throw new IllegalArgumentException("Parameter " + paramName + " is not bound to a datapoint");
       		}
       		
       		Properties tsAdress=this.parseTimeSeriesAdress2Filter(paramAdress);
       		String name=tsAdress.getProperty("name");
       		if (name==null) {
       			throw new IllegalArgumentException("The mandatory part \name\" has not been given in the address string "+ paramAdress);
       		}
       		tsAdress.remove("name");

       		// Get the data handler for the address string
       		DataHandler dh=dm.getHandlerbyName(name);
       		if (dh==null) {
       			throw new IllegalArgumentException("The adress " + paramAdress + " does not adress a datahandler");
       		}

       		
       		Set<Datapoint> allDatapoint=dh.getDatapoints(tsAdress, Access.READ);
       		if (allDatapoint.size()==0) {
       			throw new IllegalArgumentException("The adress " + paramAdress + " does not adress a datapoint");
       		}

       		if (allDatapoint.size()>1) {
       			// ToDo: Ausgeben aller Datenpunkt-Filter als Hilfe
       			throw new IllegalArgumentException("The adress " + paramAdress + " does adress more than one datapoint");
       		}

       		Datapoint dp=allDatapoint.iterator().next();	// This is safe as we already KNOW that there exactly one
       		
       		TimeInterval intervalNeededForThisDP=intervalNeeded.get(paramName);
       		if (intervalNeededForThisDP==null)
       			continue; 	// Looks like this formal parameter is never mentioned in the expression
       						// The 1 million dollar question is: Should we just ignore this or should we raise hell?
       						// Oh, BTW, we can save a lot of time if we don't look for a datapoint first in this special case 
       						// but then we would not get any parsing errors if this parameter is spelled wrongly
       		
       		TimeSeries ts=dp.getTimeSeries(intervalNeededForThisDP);

       		formulaArguments.put(paramName, ts);

       	}

       	this.logger.debug("Evaluating the time series now");
       	
       	TimeSeries[] results=tsp.eval(formulaArguments);
       	// evaluate the time series
       	// Give it back

		this.logger.info("getTimeSeries returns a time series as of {}", results[0]);

		return results[0];
	}

	@Override
	public boolean canWrite() {
		return false;
	}

	@Override
	public void putTimeSeries(TimeSeries data) {
		throw new UnsupportedOperationException("This datapoint can't write");
	}

	@Override
	public void dataChanged(Datapoint source, TimeInterval interval) {
		throw new UnsupportedOperationException("This datapoint does not accept changes");
	}
	
}



/**
 * This class publishes F3 as a service.
 * To do this, this datahandler publishes one datapoint (see above).
 * @author DuennebeilG
 *
 */

public class Formula3QueryDataHandler extends DatapointManager implements DataHandler {

	boolean open=false;
	
	Logger logger=LoggerFactory.getLogger(Formula3QueryDataHandler.class);
	
	PythonInterpreter interpreter=null;

	Formula3Datapoint theDatapoint;

	private DeviceManager dm;
	
	static Map<String, Object> capabilities;
	{
		capabilities=new HashMap<String, Object>();
		capabilities.put(DataHandler.capSupportsFormula3, true);
		capabilities=Collections.unmodifiableMap(capabilities);
	}
	

    @Override
    public Map<String, Object> getCapabilities() {
    	return Formula3QueryDataHandler.capabilities;
    }
	
	
	@Override
	public void open() throws IOException {
    	
		Properties filter=new Properties();
		filter.setProperty("id", "F3");
		theDatapoint=new Formula3Datapoint(filter);
		theDatapoint.setDeviceManager(dm);
		this.registerDatapoint(theDatapoint);

		open=true;
	}

	@Override
	public boolean isOpen() {
		return open;
	}

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setId(String id) throws IllegalStateException {
		// TODO Auto-generated method stub
		
	}
	
	public void setDeviceManager(DeviceManager dm) {
		this.dm = dm;
	}

	
	@Override
    public Set<Datapoint> getDatapoints(Properties filter, Access access) {
		// Overloaded for the single purpose of having a point to put a breakpoint to during debugging
		Set<Datapoint> result=super.getDatapoints(filter, access);
		return result;
	}

	
}
