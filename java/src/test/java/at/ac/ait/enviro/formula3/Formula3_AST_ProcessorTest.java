package at.ac.ait.enviro.formula3;

import org.python.core.PyException;
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
import org.junit.Ignore;
import org.junit.Test;
import org.python.util.PythonInterpreter;

import static org.junit.Assert.*;

public class Formula3_AST_ProcessorTest {

    public Formula3_AST_ProcessorTest() {
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
    public void testTrivial() {
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

        TimeSeries result = f3p.evalTimeSeries(expected);

        Object vkeys=result.getTSProperty(TimeSeries.VALUE_KEYS);
        assertTrue(vkeys instanceof String[]);
        assertEquals(2, ((String[])vkeys).length);
        assertEquals("ts:values", ((String[])vkeys)[0]);
        assertEquals("metadata", ((String[])vkeys)[1]);
        
        for(TimeStamp t : times) {
            assertEquals(expected.getValue(t, "ts:values"), result.getValue(t, "ts:values"));
            assertEquals(expected.getValue(t, "metadata"), result.getValue(t, "metadata"));
        }
    }

    @Test
    public void testMul2() {
    	// Multiply integer with integer_const
        Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS <<TS[i] * 2>>");

        TimeStamp[] times = new TimeStamp[5];
        for(int i = 0; i < times.length; i++) {
            times[i] = new TimeStamp(i*1000l*60l*60l);
        }

        TimeSeries expected = new TimeSeriesImpl();
		expected.setTSProperty(TimeSeries.VALUE_KEYS, new String[] {"ts:values", "metadata"});
        for(TimeStamp t : times) {
            expected.setValue(t,"ts:values", 1);
            expected.setValue(t, "metadata", "test");
        }

        TimeSeries result = f3p.evalTimeSeries(expected);

        Object vkeys=result.getTSProperty(TimeSeries.VALUE_KEYS);
        assertTrue(vkeys instanceof String[]);
        assertEquals(2, ((String[])vkeys).length);
        assertEquals("ts:values", ((String[])vkeys)[0]);
        assertEquals("metadata", ((String[])vkeys)[1]);
        
        for(TimeStamp t : times) {
            assertEquals(((Number)expected.getValue(t,"ts:values")).intValue() * 2, result.getValue(t,"ts:values"));
            assertEquals(expected.getValue(t, "metadata"), result.getValue(t, "metadata"));
        }
    }

    @Test
    public void testAdd() {
    	// Add integer with integer constant
        Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS << TS[i]+1>>");

        TimeSeries ts = new TimeSeriesImpl();
        ts.setTSProperty(TimeSeries.VALUE_KEYS, new String[]{"ts:values"});
        long start = System.currentTimeMillis();
        for (int i = 0; i < 5; ++i) {
            ts.setValue(new TimeStamp(start + (i * 1000)),"ts:values", i);
        }

        TimeSeries result = f3p.evalTimeSeries(ts);
        int i = 0;
        int[] expected = {1, 2, 3, 4, 5};
        for (final TimeStamp t : result.getTimeStamps()) {
            Slot s = result.getSlot(t);
            assertEquals(expected[i], s.get("ts:values"));
            i++;
        }
    }

    @Test
    public void testDoubleType() {
    	// Add (java) float with (python) integer_constant
        Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS << TS[i]+1>>");

        TimeSeries ts = new TimeSeriesImpl();
        ts.setTSProperty(TimeSeries.VALUE_KEYS, new String[]{"ts:values"});
        long start = System.currentTimeMillis();
        for (int i = 0; i < 5; ++i) {
            ts.setValue(new TimeStamp(start + (i * 1000)),"ts:values", i*Math.PI);
        }

        TimeSeries result = f3p.evalTimeSeries(ts);
        int i = 0;
        //int[] expected = {1, 2, 3, 4, 5};
        for (final TimeStamp t : result.getTimeStamps()) {
            Slot s = result.getSlot(t);
            assertEquals((double)i++*Math.PI+1.0, (Double)s.get("ts:values"), 0.002);
        }
    }


    @Test
    public void testStringType() {
    	// Add (java) Strings with (python) string constant
        Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS << TS[i]+\"Hello\">>");

        TimeSeries ts = new TimeSeriesImpl();
        ts.setTSProperty(TimeSeries.VALUE_KEYS, new String[]{"ts:values"});
        long start = System.currentTimeMillis();
        for (int i = 0; i < 5; ++i) {
            ts.setValue(new TimeStamp(start + (i * 1000)),"ts:values", Integer.toString(i));
        }

        TimeSeries result = f3p.evalTimeSeries(ts);
        int i = 0;
        //int[] expected = {1, 2, 3, 4, 5};
        for (final TimeStamp t : result.getTimeStamps()) {
            Slot s = result.getSlot(t);
            assertEquals(Integer.toString(i++)+"Hello", (String)s.get("ts:values"));
        }
    }

	  @Test
	  @Ignore
	  public void testAssign()
	  {
	    //Copy the default value property of TS into the new property x
	    //Check if the new TS has exactly ONE more ValueKey property (x)
	    //Check if the values of the default values (ts:values) are equal to the new values (x)
	    //This test is absolutely necessary for the messageServerDatahandler!  
	    //If this one fails, formula will not be able to communicate with the messageServer!!!
	    Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS << TS[i] => x>>");
	
	    TimeSeries ts = new TimeSeriesImpl();
	    ts.setTSProperty(TimeSeries.VALUE_KEYS, new String[]
	            {
	              "ts:values"
	            });
	    long start = System.currentTimeMillis();
	    for (int i = 0; i < 5; ++i)
	    {
	      ts.setValue(new TimeStamp(start + (i * 1000)), "ts:values", i);
	    }
	
	    TimeSeries result = f3p.evalTimeSeries(ts);
	    String[] origValKeys = (String[]) ts.getTSProperty(ts.VALUE_KEYS);
	    int origValKeysLen = origValKeys.length;
	    String[] resultValKeys = (String[]) result.getTSProperty(result.VALUE_KEYS);
	    int resultValKeysLen = resultValKeys.length;
	    assertEquals(origValKeysLen + 1, resultValKeysLen); //There should be EXACTLY ONE more ValueKey in the resulted TS, and not 2, or 5 more!
	    int i = 0;
	    //int[] expected = {1, 2, 3, 4, 5};
	    for (final TimeStamp t : result.getTimeStamps())
	    {
	      Slot s = result.getSlot(t);
	      assertEquals(i, s.get("ts:values"));
	      assertEquals(i, s.get("x"));
	      i++;
	    }
	  }

    //The following Tests validate a custom Mean function (mean_status), which is defined in aggreages.py 
     @Test
  public void testMyMeanException()
  {
    Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS << mean_status(TS[i-1 .. i]) >>");

    TimeSeries ts = new TimeSeriesImpl();
    ts.setTSProperty(TimeSeries.VALUE_KEYS, new String[]
            {
              "ts:value",
              "sorry_wrong_GStat",
              "please_fail_FStat",
              "WhatEver",
              "WhatEverEver"
            });
    long start = System.currentTimeMillis();
    for (int i = 0; i < 5; ++i)
    {
      ts.setValue(new TimeStamp(start + (i * 60000l * 60l)), "ts:value", i);
      ts.setValue(new TimeStamp(start + (i * 60000l * 60l)), "sorry_wrong_GStat", 0);
      ts.setValue(new TimeStamp(start + (i * 60000l * 60l)), "please_fail_FStat", 0);
    }

    try
    {
      TimeSeries result = f3p.evalTimeSeries(ts);
    //GStat and FStat are missing -> expect a Formula3Exception
    } catch (PyException e)
    {
      String details= e.type.toString();
      if (details.contains("<class 'formula3.exceptions.exception.Formula3Exception'>"))
        return;
      else
        fail("Wrong Exception: " + e.toString());
    } catch (Exception e)
    {
      fail("Wrong Exception: " + e.toString());
    }
    fail("There should have been an Exception");
  }
 
  @Test
  public void testMyMeanSimple()
  {
    Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS << mean_status(TS[i-1 .. i]) >>");

    TimeSeries ts = new TimeSeriesImpl();
    ts.setTSProperty(TimeSeries.VALUE_KEYS, new String[]
            {
              "ts:value",
              "DevStat",
              "ErrStat",
              "IntStat"
            });
    long start = System.currentTimeMillis();
    for (int i = 0; i < 5; ++i)
    {
      ts.setValue(new TimeStamp(start + (i * 60000l * 60l)), "ts:value", i);
      ts.setValue(new TimeStamp(start + (i * 60000l * 60l)), "DevStat", 0x00);
      ts.setValue(new TimeStamp(start + (i * 60000l * 60l)), "ErrStat", 0x00);
      ts.setValue(new TimeStamp(start + (i * 60000l * 60l)), "IntStat", 0x00);
    }

    TimeSeries result = f3p.evalTimeSeries(ts);
    
    int i = 0;
    double[] expected =
    {
      0.0, 0.5, 1.5, 2.5, 3.5
    };
    int[] expectedGStat =
    {
      0x00, 0x00, 0x00, 0x00, 0x00
    };
    int[] expectedFStat =
    {
      0x00, 0x00, 0x00, 0x00, 0x00
    };
    int[] expectedIStat =
    {
      0x00, 0x00, 0x00, 0x00, 0x00
    };

    for (final TimeStamp t : result.getTimeStamps())
    {
      Slot s = result.getSlot(t);
      org.junit.Assert.assertEquals(expected[i], s.get("ts:value"));
      org.junit.Assert.assertEquals(expectedGStat[i], s.get("DevStat"));
      org.junit.Assert.assertEquals(expectedFStat[i], s.get("ErrStat"));
      org.junit.Assert.assertEquals(expectedIStat[i], s.get("IntStat"));
      i++;
    }
  }

  @Test
  public void testMyMeanStatus()
  {
    Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS << mean_status(TS[t .. t + 10 min]) >> every 10 mins");

    TimeSeries ts = new TimeSeriesImpl();
    ts.setTSProperty(TimeSeries.VALUE_KEYS, new String[]
            {
              "ts:value",
              "DevStat",
              "ErrStat",
              "IntStat"
            });
    long start = System.currentTimeMillis();
    long offset = start % (3600*1000);
    start= start-offset;                //Align TimeStamp to full hour
    for (int i = 0; i <= 10; i++)
    {
      int GStat= 0x00;
      int FStat= 0x00;
      int IStat= 0x00;
      if (i == 3)
      {
        GStat= 0x16;
        FStat= 0x03;
      }
      if (i == 10)
      {
        FStat= 0x03;
      }
      TimeStamp tStamp= new TimeStamp(start + (i * 60*1000));
      ts.setValue(tStamp, "ts:value", i);
      ts.setValue(tStamp, "DevStat", GStat);
      ts.setValue(tStamp, "ErrStat", FStat);
      ts.setValue(tStamp, "IntStat", IStat);
    }

    TimeSeries result = f3p.evalTimeSeries(ts);
    int i = 0;
    double expectedValue = 4.666666666666;
    int expectedGStat = 0x16;
    int expectedFStat = 0x03;
    int expectedIStat = 0x0200; //HMW-Availability Limit < 90% -> Bit 2 set

    for (final TimeStamp t : result.getTimeStamps())
    {
      Slot s = result.getSlot(t);
      org.junit.Assert.assertEquals(expectedValue, (double)(Double)(s.get("ts:value")), 0.00001);
      org.junit.Assert.assertEquals(expectedGStat, s.get("DevStat"));
      org.junit.Assert.assertEquals(expectedFStat, s.get("ErrStat"));
      org.junit.Assert.assertEquals(expectedIStat, s.get("IntStat"));
    }
  }
  
    @Test
    public void testMean() {
        Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS << mean(TS[i-1 .. i]) >>");

        TimeSeries ts = new TimeSeriesImpl();
        ts.setTSProperty(TimeSeries.VALUE_KEYS, new String[]{"ts:value"});
        long start = System.currentTimeMillis();
        for (int i = 0; i < 5; ++i) {
            ts.setValue(new TimeStamp(start + (i * 60000l * 60l)),"ts:value", i);
        }

        TimeSeries result = f3p.evalTimeSeries(ts);

        int i = 0;
        double[] expected = {0.0, 0.5, 1.5, 2.5, 3.5};
        for (final TimeStamp t : result.getTimeStamps()) {
            Slot s = result.getSlot(t);
            org.junit.Assert.assertEquals(expected[i], s.get("ts:value"));
            i++;
        }
    }

    @Test
    public void testTimePattern() {
        Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS << mean(TS[t - 15 mins .. t]) >> every 15 mins");

        TimeSeries ts = new TimeSeriesImpl();
        ts.setTSProperty(TimeSeries.VALUE_KEYS, new String[]{"ts:value"});
        long start = System.currentTimeMillis();
        for (int i = 0; i < 10; ++i) {	// One value per 15 mins means the mean value does effectivly...nothing :-)
            ts.setValue(new TimeStamp(start + (i * 15 * Milliseconds.MINUTES)),"ts:value", i);
        }

        TimeSeries result = f3p.evalTimeSeries(ts);

        int i = 0;
        double[] expected = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0};
        for (final TimeStamp t : result.getTimeStamps()) {
            Slot s = result.getSlot(t);
            org.junit.Assert.assertEquals(expected[i], s.get("ts:value"));
            i++;
        }
    }

  
    protected static TimeInterval createInterval(String start, String end) throws ParseException {
    	DateFormat sdf=new SimpleDateFormat("yyyy-MM-dd HH:mm:ssZ");
    	
    	Date startDate=sdf.parse(start+"+0000");
    	
    	Date endDate=sdf.parse(end+"+0000");
    	
        return TimeInterval.createClosedInterval(new TimeStamp(startDate.getTime()), new TimeStamp(endDate.getTime()));
    }


    @Test
    public void testEvalEventInterval() throws ParseException {
        Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS <<TS[t-1min..t]>> every 1 min");

        // Create a set of pairs, input <-> expected
        TimeInterval[][] tests = new TimeInterval[][] {
            {createInterval("1970-01-01 00:00:00","1970-01-01 00:00:00"), createInterval("1970-01-01 00:00:00","1970-01-01 00:01:00")},
//            {createInterval(1,1), createInterval(0,2)},
//            {createInterval(0,2), createInterval(0,2)},
//            {createInterval(1,3), createInterval(0,4)},
        };

        // Test them
        for(int i = 0; i < tests.length; i++) {
        	TimeInterval input=tests[i][0];
        	TimeInterval expected=tests[i][1];
        	Map<String, TimeInterval> tsMap=new HashMap<String, TimeInterval>();
        	tsMap.put("A", input);	// Note: This is a crude workaround. Currently only the first entry will be taken into account anyway on the pythin side
        	
        	TimeInterval result=f3p.evalEventInterval(input);
        	
            assertEquals("failed test: " + i, expected, result);
        }
    }

    @Test
    public void testEvalQueryInterval() throws ParseException {
        Formula3_AST_Processor f3p = new Formula3_AST_Processor("@TS <<TS[t-1min..t]>> every 1 hour");

        // Create a set of pairs, input <-> expected
        TimeInterval[][] tests = new TimeInterval[][] {
            {createInterval("1970-01-01 01:17:00","1970-01-01 02:34:00"), createInterval("1970-01-01 01:59:00","1970-01-01 02:00:00")},
//            {createInterval(1,1), createInterval(0,2)},
//            {createInterval(0,2), createInterval(0,2)},
//            {createInterval(1,3), createInterval(0,4)},
        };

        // Test them
        for(int i = 0; i < tests.length; i++) {
        	TimeInterval input=tests[i][0];
        	TimeInterval expected=tests[i][1];
        	
        	TimeInterval result=f3p.evalQueryInterval(input);
        	
            assertEquals("failed test: " + i, expected, result);
        }
    }

}
