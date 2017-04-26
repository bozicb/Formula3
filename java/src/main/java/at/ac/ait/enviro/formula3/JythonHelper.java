package at.ac.ait.enviro.formula3;


/**
 *  Jython has some problems; this class provides some workarounds and other stuff. 
 */
public class JythonHelper {
	
	/**
	 * Jython can't create/clone String[]. This routine shall help.
	 * @param i
	 * @return
	 */
	public static String[] createStringArray() {
		return new String[0];
	}

}
