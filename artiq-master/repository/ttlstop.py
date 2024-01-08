from artiq.experiment import*                                   #imports everything from the artiq experiment library
import numpy as np

class TTLOFF(EnvExperiment):
    """TTL OFF"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")
         # TTL channels
        self.setattr_device("ttl1") # ttl1 = 14GHz source for EOM (DC tone)
        self.setattr_device('ttl2') # ttl2 = 2.1GHz source for EOM (Optical Pumping tone)

    @kernel #This code runs on the FPGA
    def run(self):  
        
        self.core.reset()                                       #resets core device

        # Set TTLS
        self.ttl1.output()
        self.ttl2.output()
        delay(10*ms)
        self.ttl1.on()
        delay(10*ms)
        self.ttl2.on()
        delay(10*ms)
        delay(10*ms)
        self.ttl1.off()
        delay(10*ms)
        self.ttl2.off()
        delay(10*ms)