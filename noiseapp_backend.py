'''
 Class object to contain the entire instance of the calculations needed for NoiseApp
 Last updated: 2/15/23
 Authors: Jake Frassinelli
 Relevant materials:
 https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.95AppA
 https://multimedia.3m.com/mws/media/91867O/3m-hearing-protection-how-to-use-the-noise-reduction-rating-nrr.pdf
'''

import math

class NoiseApp:
    # initialize variables to be modified according to the specified inputs
    def __init__(self):
        self.protocol = None # Will be used to store the name of the regulation method selected
        self.ERBase = None # OSHA (90), NIOSH (85), or CUSTOM
        self.ERMult = None # OSHA (5), NIOSH (3), or CUSTOM
        self.threshold = None # Max LEQ that can be experienced without protection safely

    # The following three methods are used to set the equation variables to the required numbers for the given
    # regulation (or custom ones if desired)
    def setOSHA(self):
        self.ERBase = 90
        self.ERMult = 5
        self.protocol = "OSHA"

    def setNIOSH(self):
        self.ERBase = 85
        self.ERMult = 3
        self.protocol = "NIOSH"

    def setCUSTOM(self, base, mult):
        self.ERBase = base
        self.ERMult = mult
        self.protocol = "CUSTOM"

    # The following three methods are used to set the threshold variable to either the engineering standard (90),
    # hearing conservation program (80), or a custom input
    def setThreshENGSTD(self):
        self.threshold = 90

    def setThreshHCP(self):
        self.threshold = 80

    def setThreshCUSTOM(self, thresh):
        self.threshold = thresh

    # Reset method to simplify transitioning between calculations
    def resetInfo(self):
        self.protocol = None
        self.ERBase = None
        self.ERMult = None
        self.threshold = None
    
    # Equation for calculating the maximum safe exposure time (in hours) at the given LEQ for the selected regulations
    def durationEqn(self, LEQ):
        return 8/(2**((LEQ-self.ERBase)/self.ERMult))

    # Reduces NRR of the inputed PPE from the "experimenter fit" to a "subject fit" following 3M's recommended formula
    def NRRReduction(self, NRR):
        return (NRR-7)/2

    # Takes in an array of tuples formated as such: (dB amount, exposure time)
    # Also takes in an NRR value for the PPE worn, if none supplied defaults to 7 to offset the reduction function to 0
    # Calculates the percent of total dosage
    def percentDosageCalc(self, arr, NRR=7):
        percentDosage = 0 # The percentage of max dosage reached using the supplied data
        
        for tup in arr:
            LEQ = tup[0]-self.NRRReduction(NRR)
            time = tup[1]
            percentDosage += time/self.durationEqn(LEQ)
        percentDosage *= 100
        
        return percentDosage
        
        
    # Takes in an array of tuples formated as such: (dB amount, exposure time)
    # Also takes in an NRR value for the PPE worn, if none supplied defaults to 7 to offset the reduction function to 0
    # and a time weighted average LEQ
    def TWACalc(self, arr, NRR=7):
        TWA = 0 # Time Weighted Average
        percentDosage = self.percentDosageCalc(arr, NRR)

        TWA = (16.61*math.log(percentDosage/100,10))+90
        
        return round(TWA,1)

    # This takes in the calculated time weighted average LEQ and the NRR of PPE worn and
    # returns the recomended increase in NRR of your PPE
    def protectionRec(self, TWA, NRR=0):
        if (TWA <= self.threshold):
            return 0
        else:
            return ((TWA-self.threshold)*2)+7

