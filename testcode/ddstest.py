from artiq.experiment import*                                   #imports everything from the artiq experiment library


class DDSU1C0(EnvExperiment):
    """Urukul test"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                         #sets core device drivers as attributes
        self.setattr_device("urukul1_ch0")                                                  #sets urukul0, channel 0 device drivers as attributes
        self.setattr_device("urukul1_ch1")                                                  #sets urukul0, channel 0 device drivers as attributes
        self.setattr_argument("freq", NumberValue(ndecimals = 7,type="float", unit="MHz"))  #instructs dashboard to take input in MHz and set it as an attribute called freq
        self.setattr_argument("amp", NumberValue(ndecimals = 7,type="float",max=0.32 ))              #instructs dashboard to take input for the amplitude
        self.setattr_argument("attenuation", NumberValue(type="float"))                     #instructs dashboard to take input for the attenuation
    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul1_ch0.cpld.init()                            #initialises CPLD on channel 0
        self.urukul1_ch0.init()                                 #initialises channel 0
        self.urukul1_ch1.cpld.init()                            #initialises CPLD on channel 0
        self.urukul1_ch1.init()                                 #initialises channel 0
        
        self.urukul1_ch1.set_att(self.attenuation)              #writes attenuation to urukul channel
        self.urukul1_ch1.sw.on()                                #switches urukul channel on
 
        self.urukul1_ch1.set(self.freq, amplitude = self.amp)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul1_ch0.sw.off()                               #switches urukul channel off