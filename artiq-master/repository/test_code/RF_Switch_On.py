from artiq.experiment import*                                   #imports everything from the artiq experiment library
import numpy as np

from artiq.experiment import *                  #imports everything from artiq experiment library

#minimum working code for using TTL6
#turns output on, off, and then pulses it

#to view the trace from this on a scope, use a single trigger with at least 16ms measured on scope

class RF_Switch_On(EnvExperiment):
    """RF Switch ON"""
    def build(self): #This code rus on host device     

        self.setattr_device("core")             #sets core device drivers as attributes
        self.setattr_device("ttl4")             #sets ttl6 device drivers as attributes
        
    @kernel #this code runs on the FPGA
    def run(self):
    
        self.core.reset()                       #resets core device
        self.ttl4.output()                      #sets TTL6 as an output
        delay(1*us)                             #moves timestamp forward to prevent collision between ttl6.output and ttl6.on although appears not to be neccessary in this case.
        self.ttl4.on()                          #sets TTL6 output to high
        
        
        # delay(5*s)                              #5s delay
        
        # self.ttl6.off()                         #sets TTL6 output to low