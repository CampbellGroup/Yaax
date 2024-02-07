from artiq.experiment import *
from artiq.coredevice.urukul import*
import numpy as np
from base.base_sequence import YaaxSequence


class aom_369dp(YaaxSequence):
    #@kernel
    #def prepare(self):       
        # initialize channels
       # self.urukul0_ch0.cpld.init()
       # self.urukul0_ch0.init()

       # delay(1*ms)


    @kernel
    def set(self,freq , amp ):
        self.urukul0_ch0.set(freq, amplitude = amp)

    @kernel
    def on(self,amp):
        self.urukul0_ch0.set(200*MHz, amplitude = 0.3)
    
    @kernel
    def off(self):
        self.urukul0_ch0.set(amplitude = 0.0)


class aom_935dp(YaaxSequence):
    #@kernel
    #def prepare(self):       
        # initialize channels
       # self.urukul0_ch0.cpld.init()
       # self.urukul0_ch0.init()

       # delay(1*ms)


    @kernel
    def set(self,freq , amp ):
        self.urukul1_ch0.set(freq, amplitude = amp)

    @kernel
    def on(self,amp):
        self.urukul1_ch0.set(200*MHz, amplitude = 0.3)
    
    @kernel
    def off(self):
        self.urukul1_ch0.set(amplitude = 0.0)