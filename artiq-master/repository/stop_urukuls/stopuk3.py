from artiq.experiment import*                                   #imports everything from the artiq experiment library


class StopUrukul(EnvExperiment):
    """StopU3"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")
        self.setattr_device("urukul3_ch0")                                                         #sets core device drivers as attributes
        self.setattr_device("urukul3_ch1")
        self.setattr_device("urukul3_ch2")                                                  #sets urukul0, channel 1 device drivers as attributes
        self.setattr_device("urukul3_ch3")                                                  #sets urukul0, channel 1 device drivers as attributes
        
    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device

        self.urukul3_ch0.cpld.init()                           
        self.urukul3_ch0.init()     
        self.urukul3_ch1.cpld.init()                           
        self.urukul3_ch1.init()      
        self.urukul3_ch2.cpld.init()                           
        self.urukul3_ch2.init()     
        self.urukul3_ch3.cpld.init()                           
        self.urukul3_ch3.init()                                 #switches urukul channel off


        self.urukul3_ch0.set(200*MHz, amplitude = 0.0)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul3_ch1.set(200*MHz, amplitude = 0.0)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul3_ch2.set(200*MHz, amplitude = 0.0)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul3_ch3.set(200*MHz, amplitude = 0.0)   #writes frequency and amplitude variables to urukul channel thus outputting function

        self.urukul3_ch0.sw.off()
        self.urukul3_ch1.sw.off()
        self.urukul3_ch2.sw.off()
        self.urukul3_ch3.sw.off()