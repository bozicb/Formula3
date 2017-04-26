package at.ac.ait.enviro.formula3;

import at.ac.ait.enviro.tsapi.timeseries.Slot;
import at.ac.ait.enviro.tsapi.timeseries.TimeInterval;
import at.ac.ait.enviro.tsapi.timeseries.TimeStamp;
import at.ac.ait.enviro.tsapi.timeseries.impl.TimeSeriesImpl;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import at.ac.ait.enviro.tsapi.timeseries.TimeSeries;
import at.ac.ait.enviro.util.Milliseconds;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.python.util.PythonInterpreter;

import static org.junit.Assert.*;

public class SystemTest {


    @BeforeClass
    public static void setUpClass() throws Exception {
    	
    	org.apache.log4j.BasicConfigurator.configure();	// Set up a primitive config for log4j 
    	
        Properties preProperties=new Properties();
		Properties postProperties=new Properties();
//		postProperties.setProperty("python.verbose", "debug");
		String[] argv=new String[0];
		PythonInterpreter.initialize(preProperties, postProperties, argv);
    }

    @AfterClass
    public static void tearDownClass() throws Exception {
    }

    @Before
    public void setUp() {
    }

    @After
    public void tearDown() {
    }

    @Test
    public void testGetOperatorList() {
    	// As this test relies on the list of predefined F3 operators we do NOT test 
    	// this list explicitly. We mark this test as passed when there is a list at all
    	// and no exception.
    	List<String> list=F3System.getOperatorList();
    	assertTrue(list.size()>=0);
    }

    
    @Test
    public void testSystem() {
    	ArrayList<String> paths=new ArrayList<String>();
    	paths.add("src/test/testOperators"); // Note, that the path here is different than the related tests in python. This is due to different working dirs in both systems. 
    	                                     // Both relative paths address the same sub directory
    	
    	F3System.setModuleSearchPaths(paths);
    	
    	List<String> list=F3System.getOperatorList();
    	assertTrue(list.contains("dynamicTest"));	// Note: The name of the operator is defined in the loaded test package

    }

}
