package at.ac.ait.enviro.formula3;

import java.util.ArrayList;
import java.util.List;

import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;

/**
 * This class is meant as an interface to configure the F3 subsystem.
 * It holds a set of static functions that allow to make some settings that 
 * influence the overall behavior of F3 in an application.
 * Note: The only option currently available is to set additionally 
 * search paths for F3 operators.
 */
public class F3System {
	
	/**
	 * This routine allows to add additional paths to the F3 system 
	 * which are used to find F3 operators. This is part of the 
	 * "F3 customer extensibility". 
	 * @param paths
	 * Note that this routine is still a stub at the moment.
	 */
	public static void setModuleSearchPaths(List<String> paths) {

        PythonInterpreter interpreter = new PythonInterpreter();
        
        interpreter.exec("import formula3.F3System");
        for (String path : paths) {
        	String cmd="formula3.F3System.addF3PackagePath('"+path+"')";
        	interpreter.exec(cmd);
        }
		
	}
	
	public static List<String> getOperatorList() {

        PythonInterpreter interpreter = new PythonInterpreter();

        interpreter.exec("import formula3.F3System");
        PyObject pyResult=interpreter.eval("formula3.F3System.getOperatorList()");
        PyList pyListResult=(PyList)pyResult;
        List<String> javaResult=new ArrayList<String>();
        javaResult.addAll(pyListResult);

        return javaResult;
	}
}
