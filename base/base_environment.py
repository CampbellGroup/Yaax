import numpy as np
from artiq.experiment import *



class YaaxEnvironment(HasEnvironment):
    
    
    def prepare(self):
        self.call_child_method("prepare")