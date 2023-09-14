from artiq.experiment import*                                   #imports everything from the artiq experiment library


class AOM_Frequency_Selector(EnvExperiment):
    """AOM Frequency Selector"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                         #sets core device drivers as attributes
        self.setattr_device("urukul0_ch2")                                                  #sets urukul0, channel 2 device drivers as attributes
        self.setattr_argument("freq", NumberValue(ndecimals = 7,type="float", unit="MHz"))  #instructs dashboard to take input in MHz and set it as an attribute called freq
        self.setattr_argument("amp", NumberValue(ndecimals = 7, type="float",max = 0.16 ))  #instructs dashboard to take input for the amplitude
        self.setattr_argument("attenuation", NumberValue(type="float"))                     #instructs dashboard to take input for the attenuation
        self.setattr_device("oven")

    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul0_ch2.cpld.init()                            #initialises CPLD on channel 2
        self.urukul0_ch2.init()                                 #initialises channel 2

        self.oven.command('APP:VOLT 3')
        
        self.urukul0_ch2.set_att(self.attenuation)              #writes attenuation to urukul channel
        self.urukul0_ch2.sw.on()                                #switches urukul channel on
           
            
        self.urukul0_ch2.set(self.freq, amplitude = self.amp)   #writes frequency and amplitude variables to urukul channel thus outputting function