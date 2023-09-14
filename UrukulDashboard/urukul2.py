from artiq.experiment import*                                   #imports everything from the artiq experiment library
from datamanager import DataManager

class DDSChannels(EnvExperiment,DataManager):
    """Urukul 2"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                         #sets core device drivers as attributes

        #Activation of Urukul Chips
        self.setattr_device("urukul2_ch0") 
        self.setattr_device("urukul2_ch1") 
        self.setattr_device("urukul2_ch2") 
        self.setattr_device("urukul2_ch3")

        #User imputs for frequency, amplitude and attenuation                                                   
        params = self.setparams(2)
        #User imputs for frequency, amplitude and attenuation                                                   
        self.freq0 = float(params[0])*MHz
        self.freq1 = float(params[1])*MHz
        self.freq2 = float(params[2])*MHz
        self.freq3 = float(params[3])*MHz
        self.amp0 = float(params[4])
        self.amp1 = float(params[5])
        self.amp2 = float(params[6])
        self.amp3 = float(params[7])
        self.attenuation0 = float(params[8])
        self.attenuation1 = float(params[9])
        self.attenuation2 = float(params[10])
        self.attenuation3 = float(params[11])                  
    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul2_ch0.cpld.init()                            #initialises CPLD on channel 0
        self.urukul2_ch0.init()                                 #initialises channel 0
        self.urukul2_ch1.cpld.init()                            #initialises CPLD on channel 1
        self.urukul2_ch1.init()                                 #initialises channel 1
        self.urukul2_ch2.cpld.init()                            #initialises CPLD on channel 2
        self.urukul2_ch2.init()                                 #initialises channel 2
        self.urukul2_ch3.cpld.init()                            #initialises CPLD on channel 3
        self.urukul2_ch3.init()                                 #initialises channel 3

        self.urukul2_ch0.set_att(self.attenuation0)              #writes attenuation to urukul channel
        self.urukul2_ch0.sw.on()                                 #switches urukul channel on
        self.urukul2_ch1.set_att(self.attenuation1)              #writes attenuation to urukul channel
        self.urukul2_ch1.sw.on()                                 #switches urukul channel on
        self.urukul2_ch2.set_att(self.attenuation2)              #writes attenuation to urukul channel
        self.urukul2_ch2.sw.on()                                 #switches urukul channel on
        self.urukul2_ch3.set_att(self.attenuation3)              #writes attenuation to urukul channel
        self.urukul2_ch3.sw.on()                                 #switches urukul channel on

        self.urukul2_ch0.set(self.freq0, amplitude = self.amp0)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul2_ch1.set(self.freq1, amplitude = self.amp1)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul2_ch2.set(self.freq2, amplitude = self.amp2)   #writes frequency and amplitude variables to urukul channel thus outputting function
        self.urukul2_ch3.set(self.freq3, amplitude = self.amp3)   #writes frequency and amplitude variables to urukul channel thus outputting function