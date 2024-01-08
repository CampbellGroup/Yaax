from artiq.experiment import *
import base_experiment 
from base_environment import YaaxEnvironment
from cmn_cooling_seqs import*

class Example1(base_experiment.YaaxExperiment, YaaxEnvironment):

    def prepare(self): 
       self.setattr_device("core")
       self.sequence1 = cooling_seqs(self)
       

    @kernel 
    def run(self):
        self.core.reset()
        self.sequence1.dopplercool()
    