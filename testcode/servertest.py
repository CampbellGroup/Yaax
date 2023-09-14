from artiq.experiment import*                                   #imports everything from the artiq experiment library


class hellotest(EnvExperiment):
    """hellotest"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                         #sets core device drivers as attributes
        self.setattr_device("hello")

    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        try:
            remote.message("SYST:REM")
        finally:
            remote.close_rpc()