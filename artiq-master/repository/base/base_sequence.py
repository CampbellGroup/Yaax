import numpy as np
from artiq.experiment import *
from base.base_environment import YaaxEnvironment

from base.base_start import*



class YaaxSequence(YaaxEnvironment,YaaxStart):
    
    def build(self):
        super().build()
        self._build_components()
        self.build_seq()

    def build_seq(self):
        pass
    
    @kernel 
    def run(self):
        pass
