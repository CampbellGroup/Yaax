from artiq.experiment import *
import base.base_experiment 
from base.base_environment import YaaxEnvironment
from sequences.dopplercooling import*

class Example2(base.base_experiment.YaaxExperiment, YaaxEnvironment):

    def build(self):
        #Setting arguments
        
        #935nm
        self.setattr_argument("amp935", NumberValue(ndecimals = 7,type="float",max=0.208 ))                           #instructs dashboard to take input for the amplitude
        self.setattr_argument("att935", NumberValue(type="float"))                                            #instructs dashboard to take input for the attenuation
        
        #369 nm
        self.setattr_argument("freq369", NumberValue(ndecimals = 7,type="float", unit="MHz"))                         #instructs dashboard to take input in MHz and set it as an attribute called freq
        self.setattr_argument("amp369", NumberValue(ndecimals = 7,type="float",max=0.38 ))                            #instructs dashboard to take input for the amplitude
        self.setattr_argument("att369", NumberValue(type="float"))                                            #instructs dashboard to take input for the attenuation
        self.setattr_argument("detuning369", NumberValue(ndecimals = 7,type="float", unit="MHz")) 
        
        self.setattr_argument("ion", NumberValue(ndecimals = 7,type="auto")) 

    
    def prepare(self): 
        self.setattr_device("core")
        #print(self.__dict__)
        self.sequence1 = cooling_seqs(self)

        self.detuned369 = self.freq369 - self.detuning369
        self.freq935 = 200*MHz
       

    @kernel 
    def run(self):
        self.core.reset()
        self.sequence1.dopplercool(self.detuned369,self.amp369, self.freq935, self.amp935)
        