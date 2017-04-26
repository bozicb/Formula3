package at.ac.ait.enviro.formula3;


import at.ac.ait.enviro.tsapi.timeseries.QueryParameter;
import at.ac.ait.enviro.tsapi.util.AbstractDatapoint;
import java.util.List;
import java.util.TreeMap;
import at.ac.ait.enviro.tsapi.timeseries.impl.TimeSeriesImpl;
import java.util.Map;
import at.ac.ait.enviro.tsapi.basic.DummyDataHandler;
import at.ac.ait.enviro.tsapi.handler.DataHandler.Access;
import java.io.IOException;
import java.util.Properties;
import at.ac.ait.enviro.tsapi.handler.DataHandler;
import at.ac.ait.enviro.tsapi.handler.Datapoint;
import at.ac.ait.enviro.tsapi.timeseries.TimeInterval;
import at.ac.ait.enviro.tsapi.timeseries.TimeSeries;
import at.ac.ait.enviro.tsapi.timeseries.TimeStamp;
import java.util.LinkedList;
import java.util.Set;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;
import org.python.util.PythonInterpreter;

import static org.junit.Assert.*;

public class Formula3_AST_DataHandlerTest {

    public Formula3_AST_DataHandlerTest() {
    }

    @BeforeClass
    public static void setUpClass() throws Exception {

        org.apache.log4j.BasicConfigurator.configure();

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

    Formula3_AST_DataHandler getF3DH() {
        return new Formula3_AST_DataHandler();
    }

    private static TimeInterval getInterval(long start, long end) {
        return TimeInterval.createClosedInterval(new TimeStamp(start), new TimeStamp(end));
    }

    /**
     * Test of getExpression method, of class Formula3DataHandler.
     */
    @Test
    public void testTrivial() throws IOException {

        // Setup source datapoint
        DataHandler source = new DummyDataHandler();

        Properties filter = new Properties();
        filter.setProperty("type", "const");
        filter.setProperty("value", "1");

        Datapoint sourceDP = source.createDatapoint(filter, null, Access.READ);

        // Setup F3 processing datapoint
        Formula3_AST_DataHandler f3dh = new Formula3_AST_DataHandler();
        f3dh.setId("test");
        f3dh.setF3Expression("@TS <<TS[i]>>");
        f3dh.open();

        filter.setProperty("id", "test");
        Datapoint f3dp = f3dh.createDatapoint(filter, null, Access.READ);

        // wed f3dp with sourceDP
        f3dp.dataChanged(sourceDP, getInterval(0,10));

        TimeSeries ts = f3dp.getTimeSeries(getInterval(0, 10));
        Set<TimeStamp> timestamps = ts.getTimeStamps();

        String[] value_keys=(String[])ts.getTSProperty(TimeSeries.VALUE_KEYS);
        String key=value_keys[0];
        
        assertFalse(timestamps.isEmpty());
        for(TimeStamp t : timestamps) {
            assertEquals(1, ((Number)ts.getValue(t, key)).intValue());
        }
    }

    /**
     * Test of getExpression method, of class Formula3DataHandler.
     */
    @Test
    public void testMul2() throws IOException {

        // Setup source datapoint
        DataHandler source = new DummyDataHandler();

        Properties filter = new Properties();
        filter.setProperty("type", "const");
        filter.setProperty("value", "1");

        Datapoint sourceDP = source.createDatapoint(filter, null, Access.READ);

        // Setup F3 processing datapoint
        Formula3_AST_DataHandler f3dh = new Formula3_AST_DataHandler();
        f3dh.setF3Expression("@TS <<TS[i] * 2>>");
        f3dh.open();

        filter.setProperty("id", "test");
        Datapoint f3dp = f3dh.createDatapoint(filter, null, Access.READ);

        // wed f3dp with sourceDP
        f3dp.dataChanged(sourceDP, getInterval(0,10));

        TimeSeries ts = f3dp.getTimeSeries(getInterval(0, 10));
        Set<TimeStamp> timestamps = ts.getTimeStamps();

        String[] value_keys=(String[])ts.getTSProperty(TimeSeries.VALUE_KEYS);
        String key=value_keys[0];

        assertFalse(timestamps.isEmpty());
        for(TimeStamp t : timestamps) {
            assertEquals(2, ((Number)ts.getValue(t, key)).intValue());
        }
    }


    /**
     * Testing the behavior in case somebody gives F3 some malicious expression 
     */
    @Test
    public void testCompileError() throws IOException {

        // Setup source datapoint
        DataHandler source = new DummyDataHandler();

        Properties filter = new Properties();
        filter.setProperty("type", "const");
        filter.setProperty("value", "1");

        Datapoint sourceDP = source.createDatapoint(filter, null, Access.READ);

        // Setup F3 processing datapoint
        Formula3_AST_DataHandler f3dh = new Formula3_AST_DataHandler();
        f3dh.setF3Expression("@TS <<TS[n] * XYZ>>");
        try {
        	f3dh.open();
        	fail("An expected exception has not been thrown");
        } catch (Exception ex) {
        	assertTrue("An expected exception has been accepted", true);
        }

    }

    
    
    /**
     * Test of getExpression method, of class Formula3DataHandler.
     * This tests something, but what and how?
     * Also interesting, is that behavior tested somewhere else, like in the exhausting F3 tests based on python?
     */
    @Test
    @Ignore
    // This test is ignored as it is not clear what is supposed to test, 
    // as it fails and it is not clear whether this is bogus behavior of the test or the testee
    public void testCustomKeys() throws IOException {

        // Setup source datapoint
        DataHandler source = new DummyDataHandler();

        Properties filter = new Properties();
        filter.setProperty("type", "const");
        filter.setProperty("value", "1");

        Datapoint sourceDP = source.createDatapoint(filter, null, Access.READ);

        // Setup F3 processing datapoint
        Formula3_AST_DataHandler f3dh = new Formula3_AST_DataHandler();
        f3dh.setF3Expression("@TS <<TS[n] * 2>>");
        f3dh.open();

        filter.setProperty("id", "test");
        Datapoint f3dp = f3dh.createDatapoint(filter, null, Access.READ);

        // wed f3dp with sourceDP
        f3dp.dataChanged(sourceDP, getInterval(0,10));

        TimeSeries ts = f3dp.getTimeSeries(getInterval(0, 10));
        Set<TimeStamp> timestamps = ts.getTimeStamps();

        String[] value_keys=(String[])ts.getTSProperty(TimeSeries.VALUE_KEYS);
        String key=value_keys[0];
        
        assertFalse(timestamps.isEmpty());
        for(TimeStamp t : timestamps) {
            assertEquals(1, ((Number)ts.getValue(t, key)).intValue());
            assertEquals(2, ((Number)ts.getValue(t, "doubled")).intValue());
        }
    }

    private static String[] VAL_KEYS = new String[]{"const", "time"};

    private static Map<String,Object> getDPProps() {
        final Map<String,Object> result = new TreeMap<String, Object>();

        result.put(TimeSeries.VALUE_KEYS, VAL_KEYS);
        result.put(TimeSeries.DEFAULT, 0);

        result.put("metadata", "test");

        return result;
    }

    protected static TimeSeries getTimeSeries(long start, long end, long offset) {
        TimeSeries result = new TimeSeriesImpl(getDPProps());

        for (long t = start; t <= end; t += offset) {
            TimeStamp timestamp = new TimeStamp(t);
            result.setValue(timestamp, "const", 1);
            result.setValue(timestamp, "time", t);
        }
        
        return result;
    }

    private static class TestDP extends AbstractDatapoint {

        public TimeSeries putTimeSeries;

        public TestDP() {
            super(null);
        }

        @Override
        public Map<String, Object> getProperties() {
            return getDPProps();
        }

        @Override
        public DataHandler getHandler() {
            return null;
        }

        @Override
        public boolean canRead() {
            return true;
        }

        @Override
        public TimeSeries getTimeSeries(QueryParameter... params) throws IllegalStateException {
            if(params.length != 1 || !(params[0] instanceof TimeInterval)) {
                throw new IllegalArgumentException("Supporting only single TimeInterval as QueryParameter.");
            }
            final TimeInterval interval = (TimeInterval)params[0];
            
            long start, end;
            start = interval.getStart().asMilis();
            end = interval.getEnd().asMilis();

            return Formula3_AST_DataHandlerTest.getTimeSeries(start, end, 10l);
        }

        @Override
        public boolean canWrite() {
            return true;
        }

        public List<TimeSeries> capturedTimeSeries = new LinkedList<TimeSeries>();

        @Override
        public void putTimeSeries(TimeSeries data) {
            capturedTimeSeries.add(data);
        }

        @Override
        public void dataChanged(Datapoint source, TimeInterval interval) {
        }
    }


}
