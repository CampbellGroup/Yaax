from artiq.experiment import *
from base_sequence import YaaxSequence

class Sequence1(YaaxSequence):
    @host_only
    def setup(self):
        self.hi = "hi"

    @kernel 
    def run(self):
        print("hi")
    
