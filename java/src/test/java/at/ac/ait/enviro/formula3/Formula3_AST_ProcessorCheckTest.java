package at.ac.ait.enviro.formula3;

import at.ac.ait.enviro.tsapi.timeseries.Slot;
import at.ac.ait.enviro.tsapi.timeseries.TimeInterval;
import at.ac.ait.enviro.tsapi.timeseries.TimeStamp;
import at.ac.ait.enviro.tsapi.timeseries.impl.TimeSeriesImpl;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
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

public class Formula3_AST_ProcessorCheckTest {

    public Formula3_AST_ProcessorCheckTest() {
    }

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
    public void testExceptionHandlingInJava() {
    	// This test shall only exercise the checking exceptions once to proof,
    	// translation into java exceptions is done correctly 

        try {
            Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS <TS[t]>");
        	fail("Should have thrown an exception");
        } catch(IllegalArgumentException ex) {
        	// Pass
        }

    }

}
