def compute(n, exp, f):
    import time, socket
    import F3Helper
    list = [1]
    list = n*list
    time_list = []
    for i in range(len(list)):
        time_list.append(1*i)
    tsA = F3Helper.constructTS(time_list, ['A'], A = list)
    tsB = F3Helper.constructTS(time_list, ['B'], B = list)
    tsC = F3Helper.constructTS(time_list, ['C'], C = list)
    start = time.time()
    tssRes  = F3Helper.evalExpression(exp, {'A': tsA, 'B': tsB, 'C': tsC})
    f.write('length: '+str(len(list))+' time: '+str(time.time()-start) + '\n')
    host = socket.gethostname()
    return (host, n)

expressions = [
            '@A << A[i] >>',
            '@A << A//.*//[i] >>',
            '@A <<  mean(A[t-10min..t]); A//.*//[i] >> every 10 mins',
            '@B @A << A[i] >>',
            '@A @B << A[i] >>',
            '@A << A[i]*2; A[i]*3 >>',
            '@A << A[t]*2 >> every 1 sec', 
            '@A @B << A[i] + B[i] >>',
            '@A @B << A[i] - B[i] >>',
            '@A @B << A[i] * B[i] >>',
            '@A @B << A[i] / B[i] >>',
            '@A @B << A[i] ** B[i] >>',
            '@A @B << A[i] + B[i] >>',
            '@A @B << A[i] - B[i] >>',
            '@A << A[i+1] >>',
            '@A << A[i-1] >>', 
            '@A << A[i] * 2 >>',  
            '@A << A[i] * 0.5 >>',  
            '@A << A[i] + 2 >>',  
            '@A << A[i] + 2.4 >>',
            '@A << A[i] ** 2 + 5 >>',
            '@A << -A[i] >>',
            '@A << mean(A[i-1 .. i]) >>',
            '@A << max(A[i-1 .. i]) >>',
            '@A << min(A[i-1 .. i]) >>',
            '@A << mean(A[t .. t + 1 sec])>> every 1 sec',
            '@A << mean(A[t .. t+1min])>> every 1 min',
            '@A << mean(A[t .. t+1min])>> every 1 min',
            '@A << mean(A[t .. t+10sec]); A//.*//[t..t+10sec]>> every 1 sec',
            '@A << mean(A[t .. t + 1 sec]) >> every 1 sec',
            '@A << mean(A]t .. t + 1 sec]) >> every 1 sec',
            '@A << mean(A[t .. t + 1 sec[) >> every 1 sec',
            '@A << mean(A]t .. t + 1 sec[)>> every 1 sec', 
            '@A @B << A[i] and B[i] >>',
            '@A @B << A[i] or B[i] >>',
            '@A @B << A[i] xor B[i] >>',
            '@A @B << (A[i] > B[i]) >>',
            '@A @B << A[i] < B[i] >>',
            '@A @B << A[i] >= B[i] >>',
            '@A @B << A[i] <= B[i] >>',
            '@A @B << A[i] == B[i] >>',
            '@A @B << A[i] != B[i] >>',
            '@A << A[i] if A[i] >= 3 otherwise 0 >>',
            '@A @B << A[i] if A[i] < B[i] otherwise B[i] >>',
            '@A << 1 if (A[i] > 1) otherwise 0 => value:value >>',
            '@A << A[i]*2 if (A[i] > 2) otherwise A[i]**2 >>',
            '@A @B @C << A[i] + C[i] if B[i] == A[i] otherwise B[i]*C[i] >>',
            '@A << A[i] if (A[i] > 1) otherwise None >>',
            '@A << A[i] => mean >>',
            '@A << mean(A[i-1 .. i]) => mean >>',
            '@A << "set" if (A[i] > 10) otherwise "reset" => command >>',
            '@A << A[i]+log(3) => value >>',  
            '@A << log(A[i]) >>', 
            '@A << A[i] * 2;  10 => value_test>>', 
            '@A << A[i] * 2 >> | << _[i] / 2 >>', 
            '@A << count(A[i]) >>', 
            '@A << count(A[t]) >> every 1 sec', 
            '@A << A[i] if (A[i] > 2) otherwise None >> | << count(_[i]) >>'
            ]


f = open('/home/bojan/Dropbox/Documents/Doktorat/Dissertation/Thesis/performance.txt', 'a')
from delegate import parallelize
for expression in expressions:
    f.write('\n' + expression + '\n')
    for n in [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000]:
        #parallelize(compute, [n])
        compute(n, expression, f)
f.close()
  
# if __name__ == '__main__':     
#     import pp
#     import F3Helper
#     job_server = pp.Server(4)
#     for n in [1, 10, 100, 1000, 10000, 100000, 1000000]:
#         job = job_server.submit(compute, (n,), (F3Helper.constructTS, F3Helper.evalExpression))
#         host, n = job()
#         print str(host) + ' ran job with ' + str(n)
#     job_server.print_stats()

# def compute(n):
#     import time, socket
#     import F3Helper
#     exp = '@A << "set" if (A[i] > 10) otherwise "reset" => command >>'
#     list = [1]
#     list = n*list
#     time_list = []
#     for i in range(len(list)):
#         time_list.append(1*i)
#     #tsOrig = Helper.constructTS(time_list, ['A'], A = list)
#     start = time.time()
#     #tssRes  = Helper.evalExpression(exp, {'A': tsOrig})
#     print 'length: '+str(len(list))+' time: '+str(time.time()-start)
#     host = socket.gethostname()
#     return (host, n)
#  
# if __name__ == '__main__':
#     import dispy, random, F3Helper
#     cluster = dispy.JobCluster(compute, depends=[F3Helper])
#     jobs = []
#     for n in range(20):
#         job = cluster.submit(random.randint(5,20))
#         job.id = n
#         jobs.append(job)
#     cluster.wait()
#     for job in jobs:
#         host, n = job()
#         print '%s executed job %s at %s with %s' % (host, job.id, job.start_time, n)
#         # other fields of 'job' that may be useful:
#         # print job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time
#     cluster.stats()
