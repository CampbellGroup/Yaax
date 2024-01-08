from artiq.experiment import*                                   #imports everything from the artiq experiment library
import numpy as np
import time
class Server(EnvExperiment):
    """Servertest"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")
        self.setattr_device("oven")

    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset() 
        self.oven.on()

        self.oven.current(2)
        time.sleep(10*s)
        

        self.oven.off()
        #self.oven.command('OUTP 1')
        self.oven.close_rpc()
        