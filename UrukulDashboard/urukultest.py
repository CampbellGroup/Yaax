from artiq.experiment import*                                   #imports everything from the artiq experiment library
import pandas as pd
from datamanager import DataManager


class Urukultest(EnvExperiment, DataManager):
    """Urukul 1 Channel 0 Flicker"""
    def build(self): #This code runs on the host device

        self.setattr_device("core")                                                         #sets core device drivers as attributes
        #Activation of Urukul Chips
        self.setattr_device("urukul1_ch0") 

        params = self.setparams(1)
        #print(params)
        self.freq = float(params[0])*MHz
        self.attenuation = float(params[4])
        self.amp = float(params[8])
        
        #print(self.freq,self.amp,self.attenuation)
    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul1_ch0.cpld.init()                            #initialises CPLD on channel 0
        self.urukul1_ch0.init()                                 #initialises channel 0
        
        self.urukul1_ch0.set_att(self.attenuation)              #writes attenuation to urukul channel
        self.urukul1_ch0.sw.on()                                #switches urukul channel on

        self.urukul1_ch0.set(self.freq, amplitude = self.amp)   #writes frequency and amplitude variables to urukul channel thus outputting function