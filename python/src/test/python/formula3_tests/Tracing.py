import trace
import F3Helper
import sys

def compute():
    n = 1000000
    exp = '@A << mean(A[t .. t+10sec]); A//.*//[t..t+10sec] >> every 1 sec'

    timeStamps = []
    for i in range(n):
        timeStamps.append(1*i)
        list = [1]
        list *= n

    ts = F3Helper.constructTS(timeStamps, ['A'], A = list)
    tssRes = F3Helper.evalExpression(exp, {'A': ts})
    
tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], trace=0)
tracer.run('compute()')
r = tracer.results()
r.write_results(show_missing=True, coverdir='tracing')
