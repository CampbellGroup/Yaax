import numpy as np
from artiq.experiment import *
from base_environment import YaaxEnvironment



class YaaxSequence(YaaxEnvironment):
    
    def build(self):
        #Set up attributes
        self.setattr_device("core")
        self.build_components()

    def build_components():
        pass 
    
    @kernel 
    def run(self):
        pass