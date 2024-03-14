from artiq.experiment import*                                   #imports everything from the artiq experiment library
from base.base_defs import*
import base.base_experiment 
from base.base_environment import YaaxEnvironment

class cooling_seqs(base.base_experiment.YaaxExperiment, YaaxEnvironment):

    def build_exp(self): #This code runs on the host devic
        self.aom935 = aom_935dp(self)
        self.aom369dp = aom_369dp(self)
    
    @kernel 
    def interrogation369(self,freq369,amp369,ion):
        pass

    #This is an emergency off
    @kernel 
    def off(self):
        self.prepare()  
        self.urukul0_ch0.sw.off()
        self.urukul1_ch0.sw.off()
