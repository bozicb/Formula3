import cProfile
import F3Helper

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
 
cProfile.run('compute()')
