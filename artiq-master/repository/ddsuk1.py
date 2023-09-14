from artiq.experiment import*                                   #imports everything from the artiq experiment library


class DDSChannels(EnvExperiment):
    """Urukul 1"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                         #sets core device drivers as attributes

        #Activation of Urukul Chips
        self.setattr_device("urukul1_ch0") 
        self.setattr_device("urukul1_ch1") 
        self.setattr_device("urukul1_ch2") 
        self.setattr_device("urukul1_ch3")

        #User imputs for frequency, amplitude and attenuation                                                   
        self.setattr_argument("freq0", NumberValue(ndecimals = 7,type="float", unit="MHz"))  
        self.setattr_argument("amp0", NumberValue(ndecimals = 7,type="float",max = 0.208))  
        self.setattr_argument("attenuation0", NumberValue(type="float"))                     
        self.setattr_argument("freq1", NumberValue(ndecimals = 7,type="float", unit="MHz"))  
        self.setattr_argument("amp1", NumberValue(ndecimals = 7,type="float" ))              
        self.setattr_argument("attenuation1", NumberValue(type="float"))                     
        self.setattr_argument("freq2", NumberValue(ndecimals = 7,type="float", unit="MHz"))  
        self.setattr_argument("amp2", NumberValue(ndecimals = 7,type="float" ))             
        self.setattr_argument("attenuation2", NumberValue(type="float"))                     
        self.setattr_argument("freq3", NumberValue(ndecimals = 7,type="float", unit="MHz"))  
        self.setattr_argument("amp3", NumberValue(ndecimals = 7,type="float"))    
        self.setattr_argument("attenuation3", NumberValue(type="float"))                    
    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul1_ch0.cpld.init()                            #initialises CPLD on channel 0
        self.urukul1_ch0.init()                                 #initialises channel 0
        self.urukul1_ch1.cpld.init()                            #initialises CPLD on channel 1
        self.urukul1_ch1.init()                                 #initialises channel 1
        self.urukul1_ch2.cpld.init()                            #initialises CPLD on channel 2
        self.urukul1_ch2.init()                                 #initialises channel 2
        self.urukul1_ch3.cpld.init()                            #initialises CPLD on channel 3
        self.urukul1_ch3.init()                                 #initialises channel 3

        self.urukul1_ch0.set_att(self.attenuation0)              #writes attenuation to urukul channel
        self.urukul1_ch0.sw.on()                                 #switches urukul channel on
        self.urukul1_ch1.set_att(self.attenuation1)              #writes attenuation to urukul channel
        self.urukul1_ch1.sw.on()                                 #switches urukul channel on
        self.urukul1_ch2.set_att(self.attenuation2)              #writes attenuation to urukul channel
        self.urukul1_ch2.sw.on()                                 #switches urukul channel on
        self.urukul1_ch3.set_att(self.attenuation3)              #writes attenuation to urukul channel
        self.urukul1_ch3.sw.on()                                 #switches urukul channel on

        self.urukul1_ch0.set(self.freq0, amplitude = self.amp0)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul1_ch1.set(self.freq1, amplitude = self.amp1)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul1_ch2.set(self.freq2, amplitude = self.amp2)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul1_ch3.set(self.freq3, amplitude = self.amp3)   #writes frequency and amplitude variables to urukul channel thus outputting function