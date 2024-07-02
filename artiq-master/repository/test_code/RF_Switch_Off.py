from artiq.experiment import *                  #imports everything from artiq experiment library

#minimum working code for using TTL4

#to view the trace from this on a scope, use a single trigger with at least 16ms measured on scope

class RF_Switch_Off(EnvExperiment):
    """RF Switch OFF"""
    def build(self): #This code rus on host device     

        self.setattr_device("core")             #sets core device drivers as attributes
        self.setattr_device("ttl4")             #sets ttl6 device drivers as attributes
        
    @kernel #this code runs on the FPGA
    def run(self):
    
        self.core.reset()                       #resets core device.
        self.ttl4.off()                         # 