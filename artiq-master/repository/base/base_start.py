from artiq.experiment import *


'''THIS IS PART OF THE START SEQUENCE OF EVERY YAAX EXPERIMENT'''

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

        '''
        #Place all Mirnies here 
        #self.setattr_device("mirny0_ch0")
        self.setattr_device("mirny0_ch1")
        self.setattr_device("mirny0_almazny") 
        '''

    @kernel
    def _initialize(self):
        
        #This is the only core reset in your experiment
        self.core.reset() 

        #Initialize all the science urukuls here 
        self.urukul0_ch0.cpld.init()
        self.urukul0_ch0.init()
        self.urukul1_ch0.cpld.init()
        self.urukul1_ch0.init()

        #Initialize all the science TTLS
        self.ttl0.input()
        '''
        #Initializa all the Mirnies 
        self.mirny0_ch0.cpld.init()
        self.mirny0_ch0.init()   
        self.mirny0_ch1.cpld.init()
        self.mirny0_ch1.init()   
        '''
        #print("devices are on")