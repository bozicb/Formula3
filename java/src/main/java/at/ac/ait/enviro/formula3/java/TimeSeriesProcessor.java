package at.ac.ait.enviro.formula3.java;

import at.ac.ait.enviro.tsapi.timeseries.TimeInterval;
import at.ac.ait.enviro.tsapi.timeseries.TimeSeries;
import java.util.Map;

import org.python.core.PyDictionary;


/**
 * This interface defines how a processor should look like.
 * It is used to allow mapping from F3 python to it's java wrapper.
 * Indeed it is not clear why this is in the F3 package. There seems to be another definition somewhere that is only partly consistent
 * In the long run these different types should be melted together
 */
public interface TimeSeriesProcessor {
	
	public Map<String, String> getParameterInfo();
	
    public TimeSeries[] eval(PyDictionary arguments);
    public void configure(Map<String, ? extends Object> properties);
    public TimeInterval getDataChangedInterval(Map<String,TimeInterval> eventIntervals);
    public Map<String, TimeInterval> getDataNeededIntervals(TimeInterval queryInterval);
}
