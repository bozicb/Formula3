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

public class ProfileTest {


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
    public void testProfiling() {
    	// Just a pass through
        Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS <<TS[i]>>");

        TimeStamp[] times = new TimeStamp[5];
        for(int i = 0; i < times.length; i++) {
            times[i] = new TimeStamp(i*1000l*60l*60l);
        }

        TimeSeries expected = new TimeSeriesImpl();
        expected.setTSProperty(TimeSeries.VALUE_KEYS, new String[]{"ts:values", "metadata"});
        for(TimeStamp t : times) {
            expected.setValue(t, "ts:values", 1);
            expected.setValue(t, "metadata", "test");
        }

        f3p.setProfiling(true);
        TimeSeries result = f3p.evalTimeSeries(expected);

        for(TimeStamp t : times) {
            assertEquals(expected.getValue(t, "ts:values"), result.getValue(t, "ts:values"));
        }
    }

}
