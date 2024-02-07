import numpy as np
from artiq.experiment import *
from base.base_environment import YaaxEnvironment

from base.base_start import*



class YaaxSequence(YaaxEnvironment,YaaxStart):
    
    def build(self):
        super().build()
        self._build_components()
        self.build_seq()

    """
    #This class starts all of the "science" components
    def _build_components(self):
        self.setattr_device("core")
        
        #Place urukuls here 
        self.setattr_device("urukul0_ch0")  #369nmdp
        self.setattr_device("urukul0_ch1")  #411nmdp
        self.setattr_device("urukul1_ch0")  #935nmdp
        self.setattr_device("urukul1_ch1")  #?
        
        #Place ttls here 
        self.setattr_device("ttl0")  #PMT TTL
    """

    def build_seq(self):
        pass
    
    @kernel 
    def run(self):
        pass