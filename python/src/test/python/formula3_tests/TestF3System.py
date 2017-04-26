import formula3.F3System as F3System # we will test this module

import formula3.globals

import os
import os.path

import unittest
import logging

def testOperator(self):
    'This is just an operator to test the registry'
    pass


class Test(unittest.TestCase):
    
    def setUp(self):
        logging.basicConfig()
        self.testOperatorPath="testOperators"
        for i in xrange(10): # if somebdy everys made the directory structure that complex ... hit him
            self.testOperatorPath="../"+self.testOperatorPath
            if os.path.exists(self.testOperatorPath):
                break
            
            

    # This test executes the functions to extend the F3 system with custom
    # operators. 
    def testOperatorRegistry(self):
        F3System.addF3Operator("test", testOperator)
        
        known_operators=F3System.getOperatorList()
        
        self.assertIn("test", known_operators)
        op=formula3.globals.aggregates["test"]
        self.assertEquals(testOperator, op)

    def testAddPath(self):
        # print os.getcwd() # should point to the directory of the test.
        print os.listdir(self.testOperatorPath)
        F3System.addF3PackagePath(self.testOperatorPath)
        
        known_operators=F3System.getOperatorList()
        self.assertIn("dynamicTest", known_operators) # Note: the name of the inserted test is determined in the loaded package's __init__.py
