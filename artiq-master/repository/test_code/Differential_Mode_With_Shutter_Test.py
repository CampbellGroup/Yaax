from artiq.experiment import*                                   #imports everything from the artiq experiment library
import time
import numpy as np

class DifferentialMode(EnvExperiment):
    """Differential Mode With 399 Shutter (Test)"""
    def build(self): #This code runs on the host device
        
        #Set up attributes
        self.setattr_device("core")                                      
        self.setattr_device("urukul1_ch0")                                                 
        self.setattr_device("ttl0")
        self.setattr_device("ttl6")      
        #self.setattr_device("oven")

        #Setting arguments
        self.setattr_argument("freq", NumberValue(default = 200*MHz, ndecimals = 7,type="float", unit="MHz"))                          #instructs dashboard to take input in MHz and set it as an attribute called freq
        self.setattr_argument("amp", NumberValue(default = 0.38, ndecimals = 7,type="float",max=0.38 ))                            #instructs dashboard to take input for the amplitude
        self.setattr_argument("attenuation", NumberValue(type="float"))                                             #instructs dashboard to take input for the attenuation
        #self.setattr_argument("flicker_time", NumberValue(ndecimals = 7, type= "float", unit = "ms"))              #instructs dashboard to tale the flicker time in ms 
        self.setattr_argument("interrogation_time",  NumberValue(default = 100*ms, ndecimals = 7, type= "float", unit = "ms" ))       #How long the counts are read
        self.setattr_argument("reps", NumberValue(default = 1000000 ,ndecimals = 0, type= "int", scale = 1, step = 1, max = 1000000 )) #How many times to repeat getting counts
        # self.setattr_argument("oven_disc", NumberValue(ndecimals = 0, type= "int", scale = 1, step = 1, max = 1000000))
        self.setattr_argument("shutter_threshold_399", NumberValue(default = 10000 ,ndecimals = 0, type= "int", scale = 1, step = 1, max = 1000000 )) # 399 shutter argument, set by user

    
    @kernel #This code runs on the FPGA
    def run(self):  
        
        self.core.reset()                                       #resets core device
        self.urukul1_ch0.cpld.init()                            #initialises CPLD on channel 0
        self.urukul1_ch0.init()                                 #initialises channel 0

        #self.oven.on()
        
        self.urukul1_ch0.set_att(self.attenuation)              #writes attenuation to urukul channel
        self.urukul1_ch0.sw.on()                                #switches urukul channel on

        self.urukul1_ch0.set(self.freq, amplitude = self.amp)   #writes frequency and amplitude variables to urukul channel thus outputting function

        self.ttl0.input()                                       #sets TTL0 as an input
        self.ttl6.output()                                      #sets TTL6 as an output

        tint = self.interrogation_time
        self.set_dataset("differential_counts", np.full((self.reps, 3), np.nan), broadcast=True, archive=True)               #sets up dataset so we can plot and save counts
    
        self.ttl6.off()

        for i in range(self.reps):

            self.urukul1_ch0.sw.off()                                             #switch off 935 AOM
            delay(2*us)                                            
            counts_off = self.ttl0.count(self.ttl0.gate_rising(tint))             #collects counts during 'tint', and then offloads them into 'counts_off'
            #print("935 off counts: ", counts_off)  
            
            delay(1*ms)     

            self.urukul1_ch0.sw.on()                                              #switch on 935 AOM 
            delay(2*us)
            counts_on = self.ttl0.count(self.ttl0.gate_rising(tint))              #collects counts during 'tint', and then offloads them into 'counts_off'
            #print("935 on counts: ", tint, counts_on)
            
            delay(1*ms)
        
            diff_counts = counts_on - counts_off                                  #gets difference between 'on' and 'off' counts

            data = np.array([counts_on, counts_off, diff_counts])/tint

            # if diff_counts > self.oven_disc:
            #     self.oven.off()

            if diff_counts/tint > self.shutter_threshold_399:
                delay(1*ms)
                self.ttl6.on()
                delay(2*us)

            self.mutate_dataset("differential_counts", [i], data)

