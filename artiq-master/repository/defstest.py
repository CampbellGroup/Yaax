from artiq.experiment import*                                   #imports everything from the artiq experiment library
from base.base_defs import*
import base.base_experiment 
from base.base_environment import YaaxEnvironment

class Defstest(base.base_experiment.YaaxExperiment, YaaxEnvironment):
    """defs test"""
    def build_exp(self): #This code runs on the host devic
        self.setattr_argument("Test_Toggle_DC", EnumerationValue(["on", "off"]),
                              group = "369_EOM_DC", tooltip = "Toggle Turn on Length")


        self.eom2Ghz = eom_2GHZ(self)
        #self.setattr_device("core") 

    #def prepare(self):
        #self.aom369 = aom_369dp(self)
        
    
    @kernel #This code runs on the FPGA
    def run(self):     
        self._initialize()   
        self.core.break_realtime()
        self.eom2Ghz.on()
        #self.core.break_realtime()
        #at_mu(now_mu() + 125000)
        print(self.Test_Toggle_DC)
        delay(5*s)

        self.eom2Ghz.off()
        