from artiq.experiment import *
from artiq.coredevice.urukul import*
import numpy as np
from base.base_sequence import YaaxSequence
from base.base_environment import YaaxEnvironment

class cooling_seqs(YaaxSequence):

    def build_components(self):
        #DDS Channels
        self.setattr_device("urukul0_ch0") # 369 double pass AOM
        self.setattr_device("urukul1_ch0") # 935 AOM     

        # TTL channels
        self.setattr_device("ttl1") # ttl1 = 14GHz source for EOM (DC tone)
        self.setattr_device('ttl2') # ttl2 = 2.1GHz source for EOM (Optical Pumping tone)
        self.setattr_device('ttl0') # ttl0 = input channel; receives output from PMT
        
    def prepsettings(self,amp935,att935,amp369,att369,freq369, detune369, ion):
        # 935 AOM on
        self.amp935 = amp935
        self.atten935 = att935
        self.AOMfreq935 = 80.0 * MHz              # MHz (freqs should also be float)

        # 369 AOM values (to be changed later)
        atten369 = att369
        AOMfreq369 = freq369                # MHz, frequency of AOM s.t. 369 is *not* detuned
        AOMfreq369_detuned = detune369      # MHz, frequency of AOM s.t. 369 is detuned red by 10 MHz

        # 369 AOM
        self.amp369 = amp369
        self.atten369 = atten369
        self.AOMfreq369 = AOMfreq369
        self.detuned369 = AOMfreq369 - AOMfreq369_detuned

        #This is the isotope selection
        self.ion = ion
        #print(amp935,att935,amp369,att369,freq369, detune369, ion)
        

    @kernel
    def prepare(self):       
        # initialize channels
        self.urukul0_ch0.cpld.init()
        self.urukul0_ch0.init()
        self.urukul1_ch0.cpld.init()
        self.urukul1_ch0.init()

        # Set TTLS
        self.ttl1.output()
        self.ttl2.output()
        self.ttl0.input()

        delay(1*ms)


    #This function should only be called if you are working with 171 or 173
    @kernel 
    def prebuild_spinful(self):
        self.ttl1.on()
        print("ITS ON")
        delay(5*ms)

    
    @kernel 
    def dopplercool(self,detuned369,amp369,freq935,amp935,ion):
        #This starts the prepare fucntion
        self.prepare() 
        
        #Check the isotope
        if ion == 171 or ion == 173 :
            self.prebuild_spinful()
        
        #Set the DDS's
        self.urukul0_ch0.set(detuned369, amplitude = amp369)
        self.urukul1_ch0.set(freq935, amplitude = amp935) 
        delay(0.5*ms)

        #print(detuned369,amp369,AOMfreq935,amp935,ion)

        #Turn on both the DDS channels
        with parallel:
            self.urukul0_ch0.sw.on()
            self.urukul1_ch0.sw.on()
            delay(0.5*ms)

    #This is an emergency off
    @kernel 
    def off(self):
        self.prepare()  
        self.urukul0_ch0.sw.off()
        self.urukul1_ch0.sw.off()
