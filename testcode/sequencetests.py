from artiq.experiment import*                                   #imports everything from the artiq experiment library
import time
import numpy as np

class Sequncetest(EnvExperiment):
    """Sequence Test"""

    def build(self): #This code runs on the host device
        
        #Set up attributes
        self.setattr_device("core")
        self.setattr_device("urukul1_ch0")
        self.setattr_device("ttl0")

        self.attenuation = 0.0
        self.freq = 80*MHz
        self.amp = 0.1




    
    @kernel #This code runs on the FPGA
    def run(self):  
        
        self.core.reset()                                       #resets core device
        self.urukul1_ch0.cpld.init()                            #initialises CPLD on channel 0
        self.urukul1_ch0.init()                                 #initialises channel 0
        
        self.urukul1_ch0.set_att(0.0)                           #writes attenuation to urukul channel
        self.urukul1_ch0.sw.on()                                #switches urukul channel on
 
        self.urukul1_ch0.set(80*MHz, amplitude = 0.1)           #writes frequency and amplitude variables to urukul channel thus outputting function

        self.ttl0.input()                                       #sets TTL0 as an input

