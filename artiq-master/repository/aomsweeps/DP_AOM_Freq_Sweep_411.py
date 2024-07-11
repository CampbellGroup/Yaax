from artiq.experiment import*                                   #imports everything from the artiq experiment library
import numpy as np

class uk00_freq_sweep(EnvExperiment):
    """DP_AOM_Freq_Sweep_411
       Performs a frequency sweep on the uk00 DDS (411nm DP setup).
       Changes the DDS frequency in intervals of 5MHz at a frequency of 1Hz from freq0-freq_range/2 to freq0+freq_range/2.
       The idea is to be able to use this to try to minimize the angular displacement of the DP aparatus. 
    """
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                         #sets core device drivers as attributes

        #Activation of Urukul Chips
        self.setattr_device("urukul0_ch1") 

        #User imputs for frequency, amplitude and attenuation                                                   
        self.setattr_argument("freq", NumberValue(ndecimals = 7,type="float", unit="MHz"))  # center frequency
        self.setattr_argument("amp", NumberValue(ndecimals = 7,type="float", max = 0.4 )) #Max amplitude for the G&H AOM
        self.setattr_argument("attenuation", NumberValue(type="float"))               
        self.setattr_argument("reps", NumberValue(ndecimals = 0, type= "int", scale = 1, step = 1, max = 1000000 )) #How many times to repeat the sweep 

        self.freq_range = 40 # hard setting the range to 20 for now
        self.freqs = np.linspace(-self.freq_range/2, self.freq_range/2, 9) #making list of frequencies that satisfy the range
       

    @kernel #This code runs on the FPGA
    def run(self):  

        self.core.reset()                                       #resets core device
        self.urukul0_ch1.cpld.init()                            #initialises CPLD on channel 0
        self.urukul0_ch1.init()                                 #initialises channel 0
        
        for i in range(self.reps):
            for j in range(len(self.freqs)): # iterates over all of the frequencies made above 
                
                self.urukul0_ch1.set_att(self.attenuation)
                self.urukul0_ch1.sw.on()                                 #switches urukul channel on
                self.urukul0_ch1.set((self.freq+(self.freqs[j])*MHz), amplitude = self.amp)   #writes frequency and amplitude variables to urukul channel thus outputting function
                delay(0.5*s)

        self.urukul0_ch1.set(self.freq, amplitude = self.amp)   #resets the frequency/amplitude of the AOM
        self.urukul0_ch1.sw.on()                                   #switches the aom back on