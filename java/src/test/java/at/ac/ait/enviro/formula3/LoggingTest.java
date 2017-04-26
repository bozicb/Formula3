package at.ac.ait.enviro.formula3;

import static org.junit.Assert.*;

import java.io.ByteArrayOutputStream;
import java.io.OutputStreamWriter;
import java.util.Properties;

import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.python.util.PythonInterpreter;

import org.apache.log4j.ConsoleAppender;
import org.apache.log4j.Layout;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.log4j.PatternLayout;
import org.apache.log4j.WriterAppender;

public class LoggingTest {

	PythonInterpreter interpreter;
	ByteArrayOutputStream bos=new ByteArrayOutputStream();
	OutputStreamWriter osw=new OutputStreamWriter(bos);
	
	static Logger rootLogger=Logger.getRootLogger();
	static Layout lo=new PatternLayout("%p/%m");


	@BeforeClass
	public static void setupClass() {
		rootLogger.setLevel(Level.ALL);
		
		ConsoleAppender ca=new ConsoleAppender(lo, "System.err");
		rootLogger.addAppender(ca);
		
	}
	
    @Before
    public void setUp() throws Exception {

    	rootLogger.removeAllAppenders();
    	
    	WriterAppender wa=new WriterAppender(lo, osw);

    	rootLogger.addAppender(wa);
    	
        Properties preProperties=new Properties();
 		Properties postProperties=new Properties();
//		postProperties.setProperty("python.verbose", "debug");
 		String[] argv=new String[0];
 		PythonInterpreter.initialize(preProperties, postProperties, argv);

 		interpreter = new PythonInterpreter();
 		
        interpreter.exec("import formula3.utils.SLF4J2PyLogging as javalogging");

    }
	
	@Test
	public void debugTest() {
		interpreter.exec("logger=javalogging.getLogger('my.logger')");
		interpreter.exec("logger.debug('This is debug')");
		
		String result=bos.toString();
		
		assertEquals("DEBUG/This is debug", result);
	}

	@Test
	public void infoTest() {
		interpreter.exec("logger=javalogging.getLogger('my.logger')");
		interpreter.exec("logger.info('This is info')");
		
		String result=bos.toString();
		
		assertEquals("INFO/This is info", result);
	}

	@Test
	public void warnTest() {
		interpreter.exec("logger=javalogging.getLogger('my.logger')");
		interpreter.exec("logger.warning('This is warn')");
		
		String result=bos.toString();
		
		assertEquals("WARN/This is warn", result);
	}

	@Test
	public void errorTest() {
		interpreter.exec("logger=javalogging.getLogger('my.logger')");
		interpreter.exec("logger.error('This is error')");
		
		String result=bos.toString();
		
		assertEquals("ERROR/This is error", result);
	}

	@Test
	public void criticalTest() {
		interpreter.exec("logger=javalogging.getLogger('my.logger')");
		interpreter.exec("logger.critical('This is critical')");
		
		String result=bos.toString();
		
		assertEquals("ERROR/This is critical", result);
	}

}
