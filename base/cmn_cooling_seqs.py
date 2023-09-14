from artiq.experiment import *
from artiq.coredevice.urukul import*
import numpy as np
from base_sequence import YaaxSequence
from base_environment import YaaxEnvironment

class cooling_seqs(YaaxSequence):
    # def __init__(self):
    #     YaaxSequence.build(self)

    def build_components(self):
        #DDS Channels
        self.setattr_device("urukul0_ch0") # 369 double pass AOM
        self.setattr_device("urukul1_ch0") # 935 AOM     

        # TTL channels
        self.setattr_device("ttl1") # ttl1 = 14GHz source for EOM (DC tone)
        self.setattr_device('ttl2') # ttl2 = 2.1GHz source for EOM (Optical Pumping tone)
        self.setattr_device('ttl3') # ttl3 = input channel; receives output from PMT
        
        # 935 AOM on
        self.amp935 = 0.208 
        self.atten935 = 0.0
        self.AOMfreq935 = 80.0    # MHz (freqs should also be float)

        # 369 AOM values (to be changed later)
        amp369 = 0.2
        atten369 = 0.0
        AOMfreq369 = 200.0           # MHz, frequency of AOM s.t. 369 is *not* detuned
        AOMfreq369_detuned = 5.0    # MHz, frequency of AOM s.t. 369 is detuned red by 10 MHz

        # 369 AOM
        self.amp369 = amp369
        self.atten369 = atten369
        self.AOMfreq369 = AOMfreq369
        self.detuned369 = AOMfreq369 - AOMfreq369_detuned

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
        self.ttl3.input()

        delay(1*ms)

    @kernel #This code runs on the FPGA
    def dopplercool(self):
        self.prepare() 
        self.urukul0_ch0.set(self.detuned369*MHz, self.amp369)
        self.urukul1_ch0.set(self.AOMfreq935*MHz, self.amp935)
        with parallel:
            self.urukul0_ch0.sw.on()
            self.urukul1_ch0.sw.on()
            delay(1*ms)

    @kernel #This code runs on the FPGA
    def opticalpump(self):
        self.prepare()  
        self.urukul0_ch0.set(self.detuned369*MHz, self.amp369)
        self.urukul1_ch0.set(self.AOMfreq935*MHz, self.amp935)
        with parallel:
            self.urukul0_ch0.sw.on()
            self.urukul1_ch0.sw.on()
            self.ttl1.pulse(2*ms)
            self.ttl2.pulse(2*ms)

    @kernel #This code runs on the FPGA
    def off(self):
        self.prepare()  
        self.urukul0_ch0.sw.off()
        self.urukul1_ch0.sw.off()

    @kernel #This code runs on the FPGA
    def state_det(self):
        self.prepare()  
        self.urukul0_ch0.set(self.detuned369*MHz, self.amp369)
        self.urukul1_ch0.set(self.AOMfreq935*MHz, self.amp935)
        with parallel:
            self.urukul0_ch0.sw.on()
            self.urukul1_ch0.sw.on()
            self.ttl1.pulse(2*ms)