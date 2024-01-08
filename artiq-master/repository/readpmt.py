from artiq.experiment import*                                   #imports everything from the artiq experiment library
import time
import numpy as np

class ReadPMT(EnvExperiment):
    """Read PMT Counts"""
    def build(self): #This code runs on the host device
        
        #Set up attributes
        self.setattr_device("core")                                                                                      
        self.setattr_device("ttl0")             

        #Setting arguments
        self.setattr_argument("interrogation_time",  NumberValue(ndecimals = 7, type= "float", unit = "ms" ))       #How long the counts are read
        self.setattr_argument("reps", NumberValue(ndecimals = 0, type= "int", scale = 1, step = 1, max = 1000000 )) #How many times to repeat getting counts
 
    @kernel #This code runs on the FPGA
    def run(self):  
        
        self.core.reset()                                       #resets core device
        self.ttl0.input()                                       #sets TTL0 as an input

        tint = self.interrogation_time
        self.set_dataset("pmt_counts", [0], broadcast=True, archive=True)               #sets up dataset so we can plot and save counts
        delay(10*ms)

        for i in range(self.reps):

            delay(1*us)                               
            counts = self.ttl0.count(self.ttl0.gate_rising(tint))             #collects counts during 'tint', and then offloads them into 'counts'
            #print("counts: ", counts)  
            delay(1*ms)                         

            self.append_to_dataset("pmt_counts", counts/tint)         #saves counts