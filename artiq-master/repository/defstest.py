from artiq.experiment import*                                   #imports everything from the artiq experiment library
from base.base_defs import*
import base.base_experiment 
from base.base_environment import YaaxEnvironment

class DDSChannels(base.base_experiment.YaaxExperiment, YaaxEnvironment):
    """defs test"""
    def build_exp(self): #This code runs on the host devic
        self.aom935 = aom_935dp(self)
        #self.setattr_device("core") 

    #def prepare(self):
        #self.aom369 = aom_369dp(self)
        #pass
        
    
    @kernel #This code runs on the FPGA
    def run(self):     
        self._initialize()   
        self.core.break_realtime()
        self.aom935.set(freq=200*MHz, amp=0.0)
        #self.core.break_realtime()
        #at_mu(now_mu() + 125000)

        delay(5*s)
        self.urukul1_ch0.set(200*MHz, amplitude = 0.0)
        