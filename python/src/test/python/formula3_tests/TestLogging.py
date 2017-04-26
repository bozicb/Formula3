import unittest

import formula3.utils.SLF4J2PyLogging as javalogging
import logging

class Test(unittest.TestCase):


    def setUp(self):
        logging.basicConfig()

    def tearDown(self):
        pass


    def testTimeValueNormalisation_base_conversions(self):
        logger=javalogging.getLogger("my.logger")
        logger.setLevel(logging.DEBUG)
        logger.debug("This is debug")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
