from artiq.experiment import *
from artiq.coredevice.urukul import*
import numpy as np
from base.base_sequence import YaaxSequence
from base.base_environment import YaaxEnvironment
from base.base_defs import*

class std_loading(YaaxSequence):

    def build_seq(self):
        self.aom369 = aom_369dp(self)
        self.aom935 = aom_935dp(self)


    @kernel 
    def std_on(self):
        #This starts the prepare fucntion
        self.prepare() 
        delay(5*ms)
        self.aom369.on()
        delay(5*ms)
        self.aom935.on()
        delay(5*ms)

    @kernel 
    def std_set(self,f369,f935,amp369,amp935):
        #This starts the prepare fucntion
        self.prepare() 
        self.aom369.set(f369,amp369)
        self.aom935.set(f935,amp935)
        

    #This is an emergency off
    @kernel 
    def off(self):
        self.prepare()  
        self.aom369.off()
        self.aom935.off()