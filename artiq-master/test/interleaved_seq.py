from artiq.experiment import *
from artiq.coredevice.urukul import*
import numpy as np
from base_sequence import YaaxSequence
from base_environment import YaaxEnvironment

class cooling_seqs(YaaxSequence):
    # def __init__(self):
    #     YaaxSequence.build(self)

    def build_components(self):
        self.setattr_device("core")                                                                                  # Sets core device drivers as attributes
        self.setattr_device("urukul0_ch0")                                                                           # Activation of Urukul channel for the 369DP AOM 
        self.setattr_device("urukul1_ch0")                                                                           # Activation of Urukul channel for the 935 AOM
        self.setattr_device("ttl0")          

    @kernel
    def prepare(self):
        
        
        self.core.reset()                                                                                            # Resets core device
        self.urukul0_ch0.cpld.init()                                                                                 # Initialises CPLD on channel 0
        self.urukul0_ch0.init()                                                                                      # Initialises channel 0
        self.urukul1_ch0.cpld.init()                                                                                 # Initialises CPLD on channel 1
        self.urukul1_ch0.init()                                                                                      # Initialises channel 1
        

        self.ttl0.input()                                                                                            # Sets TTL0 as an input (the PMT TTL)


        self.set_dataset("InterleavedLinescanFreqs", [0], broadcast=True, archive=True)       # Sets up dataset for plotting and saving
        self.set_dataset("InterleavedLinescanCounts", [0], broadcast=True, archive=True)       # Sets up dataset for plotting and saving

        delay(1*ms)

    @kernel #This code runs on the FPGA
    def dopplercool(self):
        self.prepare() 
        self.urukul0_ch0.set(self.detuned369*MHz, self.amp369)
        self.urukul1_ch0.set(self.AOMfreq935*MHz, self.amp935)
        with parallel:
            self.urukul0_ch0.sw.on()
            self.urukul1_ch0.sw.on()
            delay(1*ms)