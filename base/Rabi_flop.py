from artiq.experiment import *
import base_experiment 
from base_environment import YaaxEnvironment
from microwaveseq import*
from cmn_cooling_seqs import*

class Example1(base_experiment.YaaxExperiment, YaaxEnvironment):

    def prepare(self): 
       self.setattr_device("core")
       self.mwave = mwave_seqs(self)
       self.cbeam = cooling_seqs(self)
       

    @kernel 
    def run(self):
        self.core.reset()
        for i in range(1,5):
            for k in range(1,5):
                
                #Doppler cool
                self.cbeam.dopplercool()
                delay(1*ms)

                #Optical Pump
                self.cbeam.opticalpump()

                #Microwaves
                with parrallel:
                    self.cbeam.off()
                    self.mwave.microwavepulse(i)

                #Read Out
                self.state_det()
    