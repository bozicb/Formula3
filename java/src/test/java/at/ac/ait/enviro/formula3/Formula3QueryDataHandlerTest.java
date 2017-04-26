package at.ac.ait.enviro.formula3;

import static org.junit.Assert.*;

import static org.easymock.EasyMock.*;

import java.io.IOException;
import java.text.ParseException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import org.easymock.Capture;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;
import org.python.util.PythonInterpreter;

import at.ac.ait.enviro.tsapi.handler.DataHandler;
import at.ac.ait.enviro.tsapi.handler.DataHandler.Access;
import at.ac.ait.enviro.tsapi.handler.Datapoint;
import at.ac.ait.enviro.tsapi.poa.DeviceManager;
import at.ac.ait.enviro.tsapi.timeseries.TimeInterval;
import at.ac.ait.enviro.tsapi.timeseries.TimeSeries;
import at.ac.ait.enviro.tsapi.timeseries.TimeStamp;
import at.ac.ait.enviro.tsapi.timeseries.impl.TimeSeriesImpl;
import at.ac.ait.enviro.tsapi.util.Formula3Expression;
import at.ac.ait.enviro.tsapi.util.TimeUtil;

public class Formula3QueryDataHandlerTest {

	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
        Properties preProperties=new Properties();
		Properties postProperties=new Properties();
		String[] argv=new String[0];
		PythonInterpreter.initialize(preProperties, postProperties, argv);
	}

	Formula3QueryDataHandler theF3Handler=null;
	
	@AfterClass
	public static void tearDownAfterClass() throws Exception {
	}

	@Before
	public void setUp() throws Exception {
		theF3Handler=new Formula3QueryDataHandler();  
	}

	@After
	public void tearDown() throws Exception {
	}


	@Test
	public void testOpen() {
		try {
			theF3Handler.open();
		} catch (IOException e) {
			fail("Can we agree that this has never happened?");
		}
	}

	
	@Test
	public void testCapabilities() {
		Map<String, Object> caps=theF3Handler.getCapabilities();
		assertEquals(1, caps.size());
		assertTrue(caps.containsKey(DataHandler.capSupportsFormula3));
		assertTrue((Boolean)caps.get(DataHandler.capSupportsFormula3));
	}
	
	@Test
	@Ignore
	public void testIsOpen() {
		fail("Not yet implemented");
	}

	@Test
	@Ignore
	public void testGetId() {
		fail("Not yet implemented");
	}

	@Test
	@Ignore
	public void testSetId() {
		fail("Not yet implemented");
	}

	@Test
	public void testGetDatapoints() throws IOException {
		
		theF3Handler.open();	// Must open to get a data point
		
		Properties filter=new Properties();
		filter.setProperty("id", "F3");
		Access access=Access.READ;
		
		Set<Datapoint> allPoints=theF3Handler.getDatapoints(filter, access);
		assertEquals(1, allPoints.size());
	}
	

	@Test
	public void testGetFormula_errorBehaviourIllegalParameters() throws IOException {
		theF3Handler.open();	// Must open to get a data point

		Properties filter=new Properties();
		filter.setProperty("id", "F3");
		Access access=Access.READ;
		
		Set<Datapoint> allPoints=theF3Handler.getDatapoints(filter, access);
		assertEquals(1, allPoints.size());

		Datapoint dp=allPoints.iterator().next();
		
		try {
			// Not enough arguments
			dp.getTimeSeries();
			fail("Nothing happened. But something SHOULD have happened :-(");
		} catch(IllegalArgumentException ex) {
		}

		try {
			dp.getTimeSeries((Formula3Expression)null);
			fail("Nothing happened. But something SHOULD have happened :-(");
		} catch(IllegalArgumentException ex) {
		}

		try {
			// Error: Too many arguments
			dp.getTimeSeries(null, null, null);
			fail("Nothing happened. But something SHOULD have happened :-(");
		} catch(IllegalArgumentException ex) {
		}
	}

	@Test
	public void testGetFormula_errorBehaviourFaultyF3() throws IOException {
		theF3Handler.open();	// Must open to get a data point

		Properties filter=new Properties();
		filter.setProperty("id", "F3");
		Access access=Access.READ;
		
		Set<Datapoint> allPoints=theF3Handler.getDatapoints(filter, access);
		assertEquals(1, allPoints.size());

		Datapoint dp=allPoints.iterator().next();
		
		try {
			// Test. Provide all formal parameters but supply an F3 expression 
			// that is bogus in a way the lexer can recognize.
			// Note. This does not test the compiler code but the java wrapper code
			Formula3Expression f3ex=new Formula3Expression("@A %");		
			TimeStamp ts=new TimeStamp("2011-01-01 00:00:00");
			TimeInterval interval=TimeInterval.createSinglePointInTime(ts);			
			dp.getTimeSeries(f3ex, interval);
			fail("Nothing happened. But something SHOULD have happened :-(");
		} catch(IllegalArgumentException ex) {
			// System.out.print(ex);
			// Pass
		}

		try {
			// Test. Provide all formal parameters but supply an F3 expression 
			// that is bogus in a way the compiler can recognize.
			// Note. This does not test the compiler code but the java wrapper code
			Formula3Expression f3ex=new Formula3Expression("@A=\"name=DweedleDiDoo;id=id_iot\" This is an intended syntax error");		
			TimeStamp ts=new TimeStamp("2011-01-01 00:00:00");
			TimeInterval interval=TimeInterval.createSinglePointInTime(ts);			
			dp.getTimeSeries(f3ex, interval);
			fail("Nothing happened. But something SHOULD have happened :-(");
		} catch(IllegalArgumentException ex) {
			// System.out.print(ex);
			// Pass
		}

		try {
			// Test. Provide all formal parameters but supply an F3 expression 
			// that is bogus in a way the checker can recognize
			// Note. This does not test the checker code but the java wrapper code
			Formula3Expression f3ex=new Formula3Expression("@A <<A[t]>>");		
			TimeStamp ts=new TimeStamp("2011-01-01 00:00:00");
			TimeInterval interval=TimeInterval.createSinglePointInTime(ts);			
			dp.getTimeSeries(f3ex, interval);
			fail("Nothing happened. But something SHOULD have happened :-(");
		} catch(IllegalArgumentException ex) {
			System.out.println(ex);
		}
	}

	
	/* 
	 * This is a simple test which only tests passing the interval through
	 */
	@Test
	public void testGetFormulaWithN() throws IOException {
		theF3Handler.open();	// Must open to get a data point

		Properties filter=new Properties();
		filter.setProperty("id", "F3");
		Access access=Access.READ;
		
		Set<Datapoint> allPoints=theF3Handler.getDatapoints(filter, access);
		assertEquals(1, allPoints.size());

		TimeStamp ts=new TimeStamp("2011-01-01 00:00:00");
		TimeInterval interval=TimeInterval.createSinglePointInTime(ts);
		
		// We want to fake device management and datahandler for this test
		TimeSeries timeSeries=new TimeSeriesImpl();
		timeSeries.setTSProperty(TimeSeries.VALUE_KEYS, new String[] {"Hallo"});
		
		Datapoint dpMock=createStrictMock(Datapoint.class);
			expect(dpMock.getTimeSeries(eq(interval))).andReturn(timeSeries);
			
		DataHandler dhMock=createStrictMock(DataHandler.class);
		Capture<Properties> filterCapture=new Capture<Properties>();
		HashSet<Datapoint> dpContainer=new HashSet<Datapoint>(); dpContainer.add(dpMock);  
			expect(dhMock.getDatapoints(capture(filterCapture), eq(Access.READ))).andReturn(dpContainer);
			
		DeviceManager dmMock=createStrictMock(DeviceManager.class);
			expect(dmMock.getHandlerbyName("DweedleDiDoo")).andReturn(dhMock);
		
		replay(dmMock, dhMock, dpMock);
		// End mock setup
		
		
		Datapoint dp=allPoints.iterator().next();
		((Formula3Datapoint)dp).setDeviceManager(dmMock);
		
		
		Formula3Expression f3ex=new Formula3Expression("@A=\"name=DweedleDiDoo;id=id_iot\" <<A[i]>>");		
		
		dp.getTimeSeries(f3ex, interval);	// Currently the TS is ignored
		
		verify(dmMock, dhMock, dpMock);
	}

	
	/* 
	 * This is a simple test which tests the behavior with a T-slice and a bit of slice size 
	 */
	@Test
	public void testGetFormulaWithT() throws IOException, ParseException {
		theF3Handler.open();	// Must open to get a data point

		Properties filter=new Properties();
		filter.setProperty("id", "F3");
		Access access=Access.READ;
		
		Set<Datapoint> allPoints=theF3Handler.getDatapoints(filter, access);
		assertEquals(1, allPoints.size());

        TimeInterval interval = TimeUtil.parseTimeinterval("[2011-01-01 00:00:00,2011-01-01 00:00:00]");	// we put this in
        TimeInterval intervalQuery = TimeUtil.parseTimeinterval("[2011-01-01 00:00:00,2011-01-01 01:00:00]");	// this is what we expect back when the datapoint is asked for data
        
		// We want to fake device management and datahandler for this test
		TimeSeries timeSeries=new TimeSeriesImpl();
		timeSeries.setTSProperty(TimeSeries.REQUEST_INTERVAL, intervalQuery);
		timeSeries.setTSProperty(TimeSeries.VALUE_KEYS, new String[]{"value"});
		
		
		Datapoint dpMock=createStrictMock(Datapoint.class);
			expect(dpMock.getTimeSeries(eq(intervalQuery))).andReturn(timeSeries);
			
		DataHandler dhMock=createStrictMock(DataHandler.class);
		Capture<Properties> filterCapture=new Capture<Properties>();
		HashSet<Datapoint> dpContainer=new HashSet<Datapoint>(); dpContainer.add(dpMock);  
			expect(dhMock.getDatapoints(capture(filterCapture), eq(Access.READ))).andReturn(dpContainer);
			
		DeviceManager dmMock=createStrictMock(DeviceManager.class);
			expect(dmMock.getHandlerbyName("DweedleDiDoo")).andReturn(dhMock);
		
		replay(dmMock, dhMock, dpMock);
		// End mock setup
		
		
		Datapoint dp=allPoints.iterator().next();
		((Formula3Datapoint)dp).setDeviceManager(dmMock);
		
		
		Formula3Expression f3ex=new Formula3Expression("@A=\"name=DweedleDiDoo;id=id_iot\" <<A[t..t+1hour]>> every 1 hour @ 0 mins");		
		
		dp.getTimeSeries(f3ex, interval);	// Currently the TS is ignored
		
		verify(dmMock, dhMock, dpMock);
	}

	
	/* 
	 * This is a not so simple test which tests the behavior with two T-slices 
	 */
	@Test
	public void testGetFormulaWith2T() throws IOException, ParseException {
		theF3Handler.open();	// Must open to get a data point

		Properties filter=new Properties();
		filter.setProperty("id", "F3");
		Access access=Access.READ;
		
		Set<Datapoint> allPoints=theF3Handler.getDatapoints(filter, access);
		assertEquals(1, allPoints.size());

        TimeInterval interval = TimeUtil.parseTimeinterval("[2011-01-01 00:00:00,2011-01-01 00:00:00]");	// we put this in
        TimeInterval intervalQueryA = TimeUtil.parseTimeinterval("[2011-01-01 00:00:00,2011-01-01 01:00:00]");	// this is what we expect back when the datapoint A is asked for data
        TimeInterval intervalQueryB = TimeUtil.parseTimeinterval("[2011-01-01 00:00:00,2011-01-01 02:00:00]");	// this is what we expect back when the datapoint B is asked for data
        
		// We want to fake device management and datahandler for this test
		TimeSeries timeSeries=new TimeSeriesImpl();
		timeSeries.setTSProperty(TimeSeries.REQUEST_INTERVAL, intervalQueryA);
		timeSeries.setTSProperty(TimeSeries.VALUE_KEYS, new String[]{"value"});

		Properties pA=new Properties(); pA.setProperty("id", "id_iot");
		Properties pB=new Properties(); pB.setProperty("id", "e-DIOT");
		
		Datapoint dpMock=createMock(Datapoint.class);	// Note that this mock covers both datapoints A and B
			expect(dpMock.getTimeSeries(eq(intervalQueryA))).andReturn(timeSeries);
			expect(dpMock.getTimeSeries(eq(intervalQueryB))).andReturn(timeSeries);
			
		HashSet<Datapoint> dpContainerA=new HashSet<Datapoint>(); dpContainerA.add(dpMock);  
		HashSet<Datapoint> dpContainerB=new HashSet<Datapoint>(); dpContainerB.add(dpMock);  
		DataHandler dhMock=org.easymock.EasyMock.createMock(DataHandler.class);
		    expect(dhMock.getDatapoints(eq(pA), eq(Access.READ))).andReturn(dpContainerA);
		    expect(dhMock.getDatapoints(eq(pB), eq(Access.READ))).andReturn(dpContainerB);
			
		DeviceManager dmMock=createStrictMock(DeviceManager.class);
			expect(dmMock.getHandlerbyName("DweedleDiDoo")).andReturn(dhMock).times(2);
		
		replay(dmMock, dhMock, dpMock);
		// End mock setup
		
		
		Datapoint dp=allPoints.iterator().next();
		((Formula3Datapoint)dp).setDeviceManager(dmMock);
		
		
		Formula3Expression f3ex=new Formula3Expression("@A=\"name=DweedleDiDoo;id=id_iot\" @B=\"name=DweedleDiDoo;id=e-DIOT\" <<mean(A[t..t+1hour]) + mean(B[t..t+2hour])>> every 1 hour @ 0 mins");		
		
		dp.getTimeSeries(f3ex, interval);	// Currently the TS is ignored
		
		verify(dmMock, dhMock, dpMock);
	}

	
	
	@Test
	@Ignore
	public void testClose() {
		fail("Not yet implemented");
	}

	@Test
	@Ignore
	public void testGetFilterNames() throws IOException {
		theF3Handler.open();
		
		Set<String> allFilter=theF3Handler.getFilterNames(Access.READ);
		assertEquals(1, allFilter.size());
		String theName=allFilter.iterator().next();
		assertEquals("id", theName);
		
	}

	@Test
	@Ignore
	public void testMatchFilter() {
		fail("Not yet implemented");
	}

	@Test
	@Ignore
	public void testGetFilterValues() {
		fail("Not yet implemented");
	}


	@Test
	public void testCanCreateDatapoint() {
		
		Properties filter=new Properties();
		Map<String, Object> dataPointProperties=new HashMap<String, Object>();
		Access access=Access.DONT_CARE;
		
		boolean canCreate=theF3Handler.canCreateDatapoint(filter, dataPointProperties, access);
		assertFalse(canCreate);
	}

	@Test
	@Ignore
	public void testCanDropDatapoint() {
		fail("Not yet implemented");
	}

	@Test
	public void testCreateDatapoint() {
		Access access=null;
		Map<String, Object> dataPointProperties=null;
		Properties filter=null;
		try {
			theF3Handler.createDatapoint(filter, dataPointProperties, access);
			fail("Nothing thrown but expected something");
		} catch(UnsupportedOperationException ex) {
			// Fall through intended
		}
	}

	@Test
	@Ignore
	public void testDropDatapoint() {
		fail("Not yet implemented");
	}

}
