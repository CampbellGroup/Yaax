from artiq.experiment import *


class YaaxStart():
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
        
        

    @kernel
    def _initialize(self):
        self.core.reset() 
        self.urukul0_ch0.cpld.init()
        self.urukul0_ch0.init()
        self.urukul1_ch0.cpld.init()
        self.urukul1_ch0.init()

        # Set TTLS
        self.ttl0.input()
        #print("devices are on")