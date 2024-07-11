from artiq.experiment import*                                   #imports everything from the artiq experiment library
import numpy as np

class Server(EnvExperiment):
    """Servertest2"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")
        self.setattr_device("hello")

    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset() 
        self.hello.message("Hello world!")
        self.hello.close_rpc()
               