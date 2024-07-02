from artiq.experiment import*                                   #imports everything from the artiq experiment library
import time
import numpy as np

import math

class ReadPMT(EnvExperiment):
    """Read PMT Counts"""
    def build(self): #This code runs on the host device
        
        #Set up attributes
        self.setattr_device("core")                                                                                      
        self.setattr_device("ttl0")             

        #Setting arguments
        self.setattr_argument("interrogation_time",  NumberValue(ndecimals = 7, type= "float", unit = "ms" ))       #How long the counts are read
        self.setattr_argument("reps", NumberValue(ndecimals = 0, type= "int", scale = 1, step = 1, max = 1000000 )) #How many times to repeat getting counts

        self.etr = 0

    """
    def firstNan(self):
        etr = 0
        holder = self.get_dataset("pmt_counts")
        for item in holder:
            etr = etr + 1
            if math.isnan(item) == True:
                print(etr)
                return etr-1
    """       
    """
    @rpc(flags={"async"})
    def handoff(self):
        h = self.get_dataset("pmt_counts")
        hempt = np.full((1000000 - (h.size)), np.nan)
        self.holder = np.concatenate((h,hempt), axis =0 )
        print(self.holder)

        self.set_dataset("pmt_counts",self.holder, broadcast=True, persist = True, archive=True)
        print(self.firstNan(self.holder))
        self.etr = self.firstNan(self.holder)
    """

    @rpc(flags={"async"})
    def collect_data(self, datapoint):
        
        self.mutate_dataset("pmt_counts",self.etr, datapoint)         #saves counts
        self.etr = self.etr + 1
 
    @kernel #This code runs on the FPGA
    def run(self):  
        
        self.core.reset()                                       #resets core device
        self.ttl0.input()                                       #sets TTL0 as an input

        tint = self.interrogation_time

        self.set_dataset("pmt_counts", np.full((self.reps), np.nan), broadcast=True, persist= True,archive=True)               #sets up dataset so we can plot and save counts
        #self.handoff()
        delay(10*ms)

        for k in range(self.reps):
            delay(1*us)                               
            counts = self.ttl0.count(self.ttl0.gate_rising(tint))             #collects counts during 'tint', and then offloads them into 'counts'
            datapoint = counts/tint
            #print("counts: ", counts)  
            delay(1*ms)        
            self.collect_data(datapoint)        
      

