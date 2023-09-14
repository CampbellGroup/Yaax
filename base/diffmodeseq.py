from artiq.experiment import *
from artiq.coredevice.urukul import*
import numpy as np
from base_sequence import YaaxSequence
from base_environment import YaaxEnvironment

class Diffmodeseq(YaaxSequence):
    # def __init__(self):
    #     YaaxSequence.build(self)

    def build_components(self):
        self.setattr_device("urukul1_ch0")      
    
    @kernel #This code runs on the FPGA
    def run(self):  
        
        self.core.reset()                                       #resets core device
        self.urukul1_ch0.cpld.init()                            #initialises CPLD on channel 0
        self.urukul1_ch0.init()                                 #initialises channel 
        self.urukul1_ch0.sw.on()                                #switches urukul channel on
 
        self.urukul1_ch0.set(80*MHz, amplitude = 0.20, profile = 0)
        self.urukul1_ch0.cpld.set_profile(0)

        delay(1*s)

        self.urukul1_ch0.set(80*MHz, amplitude = 0.0, profile = 1)
        self.urukul1_ch0.cpld.set_profile(1)

        delay(1*s)

        self.urukul1_ch0.cpld.set_profile(0)

        
        self.urukul1_ch0.sw.off()                                #switches urukul channel on