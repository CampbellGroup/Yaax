from artiq.experiment import *
import base.base_experiment 
from base.base_environment import YaaxEnvironment
from sequences.standardloading import*

class standardlaunch(base.base_experiment.YaaxExperiment, YaaxEnvironment):
    """Standard Launch"""
    def build(self):
        self.s1 = std_loading(self)
    
    def prepare(self): 
        self.setattr_device("core")

    @kernel 
    def run(self):
        self.core.reset()
        
        #self.sequenc1e1.dopplercool(self.detuned369,self.amp369, self.freq935, self.amp935, self.ion)
        self.s1.std_on()