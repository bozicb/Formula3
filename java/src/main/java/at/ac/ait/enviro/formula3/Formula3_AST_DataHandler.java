package at.ac.ait.enviro.formula3;

import java.io.IOException;
import at.ac.ait.enviro.tsapi.basic.DelayedProcessingDataHandler;
import at.ac.ait.enviro.tsapi.handler.Datapoint;
import at.ac.ait.enviro.tsapi.operators.ReadProcessor;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

/**
 * This DataHandler implementation enables Formula3 to be used as 1:1-processor 
 * within POA-Pipes.
 * <p>
 * After instantiation and opening, this DataHandler contains
 * no Datapoints. For each Pipe, where the Formula3-expression should be used,
 * a new Datapoint must first be created with {@link #createDatapoint(Properties, Map, DataHandler.Access)}.
 * <p>
 * Usage:
 * <ul>
 * <li>Use {@link #setF3Expression(String)} to configure this DataHandler. Only F3-expressions with 1 input and 1 output are supported here.</li>
 * <li>Call {@link #open()} to compile the configured F3-expression.</li>
 * <li>For each Pipe create a new POA-Processor for the currently configured F3-expression using {@link #createDatapoint(Properties, Map, DataHandler.Access)}.</li>
 * </ul>
 */
public class Formula3_AST_DataHandler extends DelayedProcessingDataHandler {

    /* Formula3 expression of this operator */
    protected String f3Expression = null;

    protected String debugName = "f3{uninitialized}";

    /**
     * number of milliseconds, for incoming events to be accumulated 
     * before forwarding them to registered listeners.
     */
    protected long eventHoldbackTime = 0;

	private Formula3_AST_Processor processor;

    public void setF3Expression(String f3Expression) {
    	if(isOpen()) {
    		throw new IllegalStateException("f3Expression cannot be set while DataHandler is opened.");
    	}
        this.f3Expression = f3Expression;
        this.debugName = String.format("F3Operator('%s')",
                f3Expression.length() > 30
                ? f3Expression.substring(0,27) + "..."
                : f3Expression);
    }


    @Override
    public long getEventHoldbackTime() {
        return eventHoldbackTime;
    }

    @Override
    protected long getIntervalMergeDistance() {
        return eventHoldbackTime;
    }

    public void setEventHoldbackTime(long eventHoldBackTime) {
        this.eventHoldbackTime = eventHoldBackTime;
    }

    public String getF3Expression() {
        return f3Expression;
    }

    @Override
    public void open() throws IOException {
        if(f3Expression == null) {
            throw new IllegalStateException("Formula3 expression not set!");
        }

        processor = new Formula3_AST_Processor(f3Expression);

    }

    @Override
    public boolean isOpen() {
        return processor != null;
    }

    @Override
    public void close() {
        super.close();
        processor = null;
    }

    @Override
    protected ReadProcessor getProcessor() {
        if(!isOpen()) {
            throw new IllegalStateException("Formula3DataHandler is not yet opened!");
        }
        return processor;
    }
    
    @Override
    public String toString() {
    	return debugName;
    }

    /**
     * Create a new Datapoint (POA-Processor) for the currently configured
     * F3-expression.
     *
     * @param filter The Datapoint filter properties can be chosen randomly but must be unique within this DataHandler.
     * @param dataPointProperties The Datapoint properties are ignored
     * @param access must be {@link Access#READ}. (Data cannot be pushed back through the processor using putTimeSeries())
     * @return the newly created Datapoint (POA-Processor)
     */
    //Overriden to allow debugging and inspection of result
    @Override
    public Datapoint createDatapoint(Properties filter, Map<String, Object> dataPointProperties, Access access) throws IllegalArgumentException, IllegalStateException, UnsupportedOperationException {
        return super.createDatapoint(filter, dataPointProperties, access);
    }

    //Overriden to allow debugging and inspection of result
    @Override
    public Set<Datapoint> getDatapoints(Properties filter , Access access) {
      Set <Datapoint> result=super.getDatapoints(filter, access);
      return result;
    }

}
