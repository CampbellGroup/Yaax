from artiq.experiment import Experiment
from artiq.experiment import* 
from base.base_start import*


class YaaxExperiment(Experiment, YaaxStart):
       
    def build(self):
        super().build()
        self._build_components()
        self.build_exp()
    
     #This is class will get over written by the experiment
    def build_exp(self):

        '''User accessible function'''

        pass 

    def prepare(self):
        delattr(Experiment, "prepare")
        super().prepare()
