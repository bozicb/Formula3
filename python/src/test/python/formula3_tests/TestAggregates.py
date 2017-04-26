#!/usr/bin/python
# -*- coding: utf-8 -*-

#///////////////////////////////////////////////////////////////
# $Archive: /TestAggregates.py$
# $Author: Schabauer $
# $Date: $
# $Revision: 1 $
#
#  Testet Aggregate, insbesondere die Funktion calc_my_mean (cmm)
#
#/////////////////////////////////////////////////////////////////
 

import unittest
import math
import formula3.exceptions.exception as exc
import formula3.aggregates as aggregates
import logging


class Test(unittest.TestCase):

    logging.basicConfig(level= logging.INFO)
    bitLimit1= aggregates.calc_my_mean().HMWBit_availLimit1
    bitLimit2= aggregates.calc_my_mean().HMWBit_availLimit2
    
            
    def calc_n_compare(self, testName, valueKey, inputValues, expectedValues):
    #{
        '''calc_n_compare: Basisroutine für parametrierte Mittelwertberechnung'''
        print("\n*** " + testName + " ***")
        #Create TimeSeries
        slotList=[]
        for v in inputValues:
        #{
          inputValueDic= {valueKey: v[0], "DevStat": v[1], "ErrStat": v[2], "IntStat": v[3]}
          slotList.append(inputValueDic)
        #}
        
        cmm= aggregates.calc_my_mean()
        result = cmm.calc((slotList, valueKey, None, None))
        if (math.isnan(expectedValues[valueKey])):
            self.assertTrue(math.isnan(result[valueKey]))
        else:
            self.assertAlmostEqual(expectedValues[valueKey], result[valueKey])
        self.assertEquals(expectedValues["DevStat"], result["DevStat"])
        self.assertEquals(expectedValues["ErrStat"], result["ErrStat"])
        self.assertEquals(expectedValues["IntStat"], result["IntStat"])
        pass
    #}
    
    def setUp(self):
        pass


    def tearDown(self):
        pass
    

    def testMeanWithEmptySlice(self):
        '''testMeanWithEmptySlice: Wenn ein leerer Slice kommt, wird der Wert "nan" zurückgegeben und die Verfügbarkeitsschwellen gesetzt.'''
        print("\n*** testMeanWithEmptySlice ***")
    	cmm=aggregates.calc_my_mean()
        valueKey="value:anotherkey" # This is done intentionally to show misuse of the previously fixed string "value:value"
        slice= {}
        
        result= cmm.calc((slice, valueKey, None, None))
        self.assertIsInstance(result, dict)

        value= result[valueKey]
        self.assertTrue(math.isnan(value))

        intstat= result["IntStat"]
        expectedHMW= cmm.HMWBit_availLimit1 | cmm.HMWBit_availLimit2
        self.assertEquals(expectedHMW, intstat)

 
    def testMeanWithEmptySlot(self):
        '''testMeanWithEmptySlot: Wenn ein leerer Slot kommt (= keine Messwerte), wird der Wert "nan" zurückgegeben und die Verfügbarkeitsschwellen gesetzt.'''
        print("\n*** testMeanWithEmptySlot ***")
        cmm= aggregates.calc_my_mean()
        valueKey= "value:anotherkey" # This is done intentionally to show misuse of the previously fixed string "value:value"
        slot= {}
        slice= [slot]
        
        result = cmm.calc((slice, valueKey, None, None))
        self.assertIsInstance(result, dict)

        value=result[valueKey]
        self.assertTrue(math.isnan(value))

        intstat=result["IntStat"]
        expectedHMW= cmm.HMWBit_availLimit1 | cmm.HMWBit_availLimit2
        self.assertEquals(expectedHMW, intstat)

 
    def testMeanWithMissingStatusBytes(self):
        '''testMeanWithMissingStatusBytes: wenn keine StatusBytes verfügbar sind, wird eine F3-Exception erwartet'''
        print("\n*** testMeanWithMissingStatusBytes ***")
        cmm=aggregates.calc_my_mean()
        valueKey="value:anotherkey" # This is done intentionally to show misuse of the previously fixed string "value:value"
        slot={valueKey:1.0}
        try:
            result = cmm.calc(([slot], valueKey, None, None))
            self.fail("Expected exception missing")
        except exc.Formula3Exception, e:
            pass
           
 
    def testMeanWithAllValuesValid(self):
        '''testMeanWithAllValuesValid: Primitive Mittelwertberechnung über einen Slot'''
        print("\n*** testMeanWithAllValuesValid ***")
        cmm=aggregates.calc_my_mean()
        valueKey="value:anotherkey" # This is done intentionally to show misuse of the previously fixed string "value:value"
        inputValues=    {valueKey:1.0, "DevStat":0, "ErrStat":0, "IntStat":0}
        expectedValues= {valueKey:1.0, "DevStat":0, "ErrStat":0, "IntStat":0}
        slice=[inputValues]
        
        result = cmm.calc((slice, valueKey, None, None))
        self.assertAlmostEqual(expectedValues[valueKey], result[valueKey])
        self.assertEquals(expectedValues["DevStat"], result["DevStat"])
        self.assertEquals(expectedValues["ErrStat"], result["ErrStat"])
        self.assertEquals(expectedValues["IntStat"], result["IntStat"])
    
    # Hier kommen die parametrierbaren Tests
    # Dabei wird nur eine Eingangszeitreihe(inputValues) definiert und das erwartete Erbegnis.
    # Die Struktur der Einganszeitreihe ist  (valueKey, "DevStat", "ErrStat", "IntStat")
    # Mittelwerte mit Excel nachrechnen!
    
    def testMean_000(self):
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat") 
        inputValues=     ((0.0, 0x01, 0x00, 0x00), 
                          (0.0, 0x00, 0x00, 0x00),
                          (0.0, 0x01, 0x00, 0x00),
                          (0.0, 0x00, 0x00, 0x00),
                          (0.0, 0x01, 0x00, 0x00))
        expectedValues= {valueKey:0.0, "DevStat":0x01, "ErrStat":0x00, "IntStat":0x00}           
        self.calc_n_compare("testMean_000", valueKey, inputValues, expectedValues)

    def testMean_001(self):
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat") 
        inputValues=     ((0.0, 0x07, 0x00, 0x00), 
                          (1.0, 0x00, 0x00, 0x00),
                          (2.0, 0x01, 0x00, 0x00),
                          (3.0, 0x00, 0x00, 0x00),
                          (4.0, 0x10, 0x00, 0x00))
        expectedValues= {valueKey:2.0, "DevStat":0x17, "ErrStat":0x00, "IntStat":0x00}           
        self.calc_n_compare("testMean_001", valueKey, inputValues, expectedValues)
 
    def testMean_001(self):
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat") 
        inputValues=     ((0.0, 0x07, 0x00, 0x00), 
                          (1.0, 0x00, 0x00, 0x00),
                          (2.0, 0x01, 0x00, 0x00),
                          (3.0, 0x00, 0x00, 0x00),
                          (4.0, 0x10, 0x00, 0x00))
        expectedValues= {valueKey:2.0, "DevStat":0x17, "ErrStat":0x00, "IntStat":0x00}           
        self.calc_n_compare("testMean_001", valueKey, inputValues, expectedValues)
        
    def testMean_002(self):
        '''Test for HMW Bit Limit 2 (50% < availability < 90%)'''
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat") 
        inputValues=     ((0.0, 0x00, 0x00, 0x00), 
                          (1.0, 0x00, 0x01, 0x00),
                          (2.0, 0x00, 0x00, 0x00),
                          (3.0, 0x00, 0x00, 0x00),
                          (4.0, 0x00, 0x10, 0x00))
        expectedValues= {valueKey:1.66666667, "DevStat":0x00, "ErrStat":0x11, "IntStat": self.bitLimit2}           
        self.calc_n_compare("testMean_002", valueKey, inputValues, expectedValues)
        
    def testMean_003(self):
        '''Test for HMW Bit Limit 1 ( availability < 50%)'''
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat") 
        inputValues=     ((0.0, 0x00, 0x00, 0x00), 
                          (1.0, 0x00, 0x01, 0x00),
                          (2.0, 0x00, 0x10, 0x88),
                          (3.0, 0x00, 0x00, 0x00),
                          (4.0, 0x00, 0x10, 0x00))
        expectedValues= {valueKey:1.5, "DevStat":0x00, "ErrStat":0x11, "IntStat": 0x88 | self.bitLimit1 | self.bitLimit2}           
        self.calc_n_compare("testMean_003", valueKey, inputValues, expectedValues)  
        
    def testMean_004(self):
        '''Test for HMW availability = 0)'''
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat") 
        inputValues=     ((0.0, 0x00, 0x01, 0x00), 
                          (1.0, 0x00, 0x01, 0x00),
                          (2.0, 0x00, 0x10, 0x88),
                          (3.0, 0x00, 0x01, 0x00),
                          (4.0, 0x00, 0x10, 0x00))
        expectedValues= {valueKey:float('nan'), "DevStat":0x00, "ErrStat":0x11, "IntStat": 0x88 | self.bitLimit1 | self.bitLimit2}           
        self.calc_n_compare("testMean_004", valueKey, inputValues, expectedValues)    
        
    def testMean_005(self):
        '''Test with negative Values)'''
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat") 
        inputValues=     ((-98.0, 0x00, 0x00, 0x00), 
                          (-97.0, 0x00, 0x00, 0x00),
                          (112.3, 0x00, 0x00, 0x00),
                          (113.0, 0x00, 0x00, 0x00),
                          (38.77, 0x00, 0x00, 0x00))
        expectedValues= {valueKey:13.814, "DevStat":0x00, "ErrStat":0x00, "IntStat": 0}           
        self.calc_n_compare("testMean_005", valueKey, inputValues, expectedValues)    
        
    def testMean_006(self):
        '''Test with negative Values and ErrStat)'''
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat") 
        inputValues=     ((-98.0, 0x00, 0x00, 0x00), 
                          (-97.0, 0x00, 0x00, 0x00),
                          (112.3, 0x00, 0x00, 0x00),
                          (113.0, 0x00, 0x00, 0x00),
                          (38.77, 0x00, 0x70, 0x00))
        expectedValues= {valueKey:7.575, "DevStat":0x00, "ErrStat":0x70, "IntStat": 0x00 | self.bitLimit2}           
        self.calc_n_compare("testMean_006", valueKey, inputValues, expectedValues)     
        
    def testMean_007(self):
        '''Test with a big timeseries'''
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat")
        inputValues=[] 
        for i in range(0, 100):  #100 ist nicht mehr dabei
           inputValues.append((i, 0x00, 0x00, 0x00))
        
        inputValues= (tuple)(inputValues)
        expectedValues= {valueKey:49.5, "DevStat":0x00, "ErrStat":0x00, "IntStat": 0x00}           
        self.calc_n_compare("testMean_007", valueKey, inputValues, expectedValues) 
        
    def testMean_008(self):
        '''Test with a very big timeseries (anual mean value out of 10-minute values, 6*24*365=52560'''
        valueKey="value:anotherkey"
        #inputValueKey=   (valueKey, "DevStat", "ErrStat", "IntStat")
        logging.basicConfig(level= logging.INFO)
        inputValues=[] 
        for i in range(0, 52560):  #der letzte ist nicht mehr dabei
           inputValues.append((i, 0x00, 0x00, 0x00))
        
        inputValues= (tuple)(inputValues)
        expectedValues= {valueKey: 26279.5, "DevStat":0x00, "ErrStat":0x00, "IntStat": 0x00}           
        self.calc_n_compare("testMean_008", valueKey, inputValues, expectedValues)
        logging.basicConfig(level= logging.INFO)         