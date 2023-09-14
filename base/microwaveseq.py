from artiq.experiment import *
from artiq.coredevice.urukul import*
import numpy as np
from base_sequence import YaaxSequence
from base_environment import YaaxEnvironment

class mwave_seqs(YaaxSequence):
    # def __init__(self):
    #     YaaxSequence.build(self)

    def build_components(self):
        self.setattr_device("ttl0") # ttl0 = 12.64 GHz signal switch

    @kernel
    def microwavepulse(self,ptime=1):
        #self.ttl0.pules(ptime)]
        print(ptime*ms)