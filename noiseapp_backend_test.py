'''
 Unit tests for the NoiseApp class' calculation methods
 Last updated: 2/15/23
 Authors: Jake Frassinelli, Gabriel Helu
 Relevant materials:
 https://www.cdc.gov/niosh/topics/noise/reducenoiseexposure/regsguidance.html
 https://multimedia.3m.com/mws/media/91867O/3m-hearing-protection-how-to-use-the-noise-reduction-rating-nrr.pdf
'''


import unittest
from noiseapp_backend import *


class TestNoiseAppBackend(unittest.TestCase):
    app = NoiseApp() # Creates the NoiseApp object for use in all tests

    # Testing to see if the outputs of durationEqn match the expected outputs for OSHA regulations
    # retrieved from the CDC website
    def test_durationEqnOSHA(self):
        app = NoiseApp()
        app.setOSHA()
        self.assertEqual(app.durationEqn(90),8)
        self.assertEqual(app.durationEqn(95),4)
        self.assertEqual(app.durationEqn(100),2)
        self.assertEqual(app.durationEqn(105),1)
        self.assertEqual(app.durationEqn(110),.5)
        self.assertEqual(app.durationEqn(115),.25)

    # Testing to see if the outputs of durationEqn match the expected outputs for NIOSH regulations
    # retrieved from the CDC website
    def test_durationEqnNIOSH(self):
        app = NoiseApp()
        app.setNIOSH()
        self.assertEqual(app.durationEqn(85),8)
        self.assertEqual(app.durationEqn(88),4)
        self.assertEqual(app.durationEqn(91),2)
        self.assertEqual(app.durationEqn(94),1)
        self.assertEqual(app.durationEqn(97),.5)
        self.assertEqual(app.durationEqn(100),.25)

    # Testing to see if the outputs of durationEqn match the expected outputs for the equations where the
    # custom values have been substituted in
    def test_durationEqnCUSTOM(self):
        app = NoiseApp()
        app.setCUSTOM(80,4)
        self.assertEqual(app.durationEqn(80),8)
        self.assertEqual(app.durationEqn(84),4)
        self.assertEqual(app.durationEqn(88),2)
        self.assertEqual(app.durationEqn(92),1)
        self.assertEqual(app.durationEqn(96),.5)
        self.assertEqual(app.durationEqn(100),.25)

    # Testing to see if the outputs of NRRReduction are correct by comparing them to precalculated outputs
    def test_NRRReduction(self):
        app = NoiseApp()
        self.assertEqual(app.NRRReduction(7),0)
        self.assertEqual(app.NRRReduction(17),5)
        self.assertEqual(app.NRRReduction(27),10)

    # Testing to see if the outputs of percentDosageCalc are correct by comparing them to precalculated outputs
    def test_percentDosageCalc(self):
        app = NoiseApp()
        app.setOSHA()

        arr = [(90,4),(82,2),(100,.25),(85,1.75)]
        self.assertEqual(round(app.percentDosageCalc(arr,),1),81.7)
        
        arr = [(90,4),(82,2),(100,.25),(85,1.75)]
        NRR = 17
        self.assertEqual(round(app.percentDosageCalc(arr,NRR),1),40.8)
        
        arr = [(84,3),(92,3),(87,2)]
        NRR = 17
        self.assertEqual(round(app.percentDosageCalc(arr,NRR),1),41.1)

    # Testing to see if the outputs of TWACalc are correct by comparing them to precalculated outputs
    def test_TWACalc(self):
        app = NoiseApp()
        app.setOSHA()

        arr = [(84,3),(92,3),(87,2)]
        self.assertEqual(round(app.TWACalc(arr),1),88.6)

        arr = [(84,3),(92,3),(87,2)]
        NRR = 17
        self.assertEqual(round(app.TWACalc(arr,NRR),1),83.6)

        arr = [(82,1),(100,.25),(86,2.5)]
        NRR = 17
        self.assertEqual(round(app.TWACalc(arr,NRR),1),77.3)

    def test_protectionRec(self):
        app = NoiseApp()
        app.setOSHA()
        app.setThreshENGSTD()

        TWA = 83
        rec = app.protectionRec(TWA)
        self.assertTrue(TWA-app.NRRReduction(rec) <= 90)
        
        TWA = 95
        rec = app.protectionRec(TWA)
        self.assertTrue(TWA-app.NRRReduction(rec) <= 90)

        TWA = 95
        NRR = 17
        rec = app.protectionRec(TWA,NRR)
        self.assertTrue(TWA-app.NRRReduction(rec) <= 90)

        TWA = 105
        NRR = 17
        rec = app.protectionRec(TWA,NRR)
        self.assertTrue(TWA-app.NRRReduction(rec) <= 90)
        
if __name__ == '__main__':
    unittest.main()
