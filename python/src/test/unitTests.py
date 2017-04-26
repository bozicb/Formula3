import unittest


def printResult(results, indent=""):
    if isinstance(results, unittest.TestSuite):
        for result in results:
            printResult(result, indent+"   ")
        return
    
    print dir(results)
    print indent+str(results)+res
        

testRunner = unittest.defaultTestLoader

suites = testRunner.discover("python", "test*.py", "python")

printResult(suites)
