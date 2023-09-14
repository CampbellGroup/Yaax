from artiq.experiment import*                                   #imports everything from the artiq experiment library

#This code outputs a single frequency at a fixed amplitude on a single channel of the urukul
#the output frequency must be inputted in MHz from the dahsboard
#The ouput persists for 2 seconds and the turns off

class Urukul_Frequency_Selectable(EnvExperiment):
    """stop"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                         #sets core device drivers as attributes
        self.setattr_device("urukul1_ch0")                                                  #sets urukul0, channel 1 device drivers as attributes
        self.setattr_device("urukul1_ch1")         #instructs dashboard to take input in MHz and set it as an attribute called freq
        
    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul1_ch0.cpld.init()                            #initialises CPLD on channel 1
        self.urukul1_ch0.init()                                 #initialises channel 1                                          
        self.urukul1_ch0.sw.off()                               #switches urukul channel off

        self.urukul1_ch1.cpld.init()                            #initialises CPLD on channel 1
        self.urukul1_ch1.init()                                 #initialises channel 1                                          
        self.urukul1_ch1.sw.off()                               #switches urukul channel off