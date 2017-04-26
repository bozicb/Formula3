/**
 * This package is part of the maven module Formula3.
 * It has three classes:
 * <dl>
 *  <dd>Formula3_AST_Processor
 *  <dd>This class in the main worker bee for F3 inline processing.<br>
 *      It wrappes the F3 TSP class and gives access to it's capabilities.
 *  <dt>Formula3_AST_DataHandler
 *  <dd>Currently the processor interface is not well defined and a TimeSeries Processor
 *      is treated the same way as a Datahandler is. This class wrappes the F3 processor for the (long?) time being
 *  <dt>Formula3QueryDataHandler
 *  <dd>An interface that allows to send queries to F3.<br>
 * </dl>
 */

package at.ac.ait.enviro.formula3;

