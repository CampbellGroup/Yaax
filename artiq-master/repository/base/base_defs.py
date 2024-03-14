from artiq.experiment import *
from artiq.coredevice.urukul import*
import numpy as np
from base.base_sequence import YaaxSequence


class aom_369dp(YaaxSequence):

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

    @kernel
    def set(self,freq , amp ):
        self.urukul1_ch0.set(freq, amplitude = amp)

    @kernel
    def on(self,amp):
        self.urukul1_ch0.set(200*MHz, amplitude = 0.3)
    
    @kernel
    def off(self):
        self.urukul1_ch0.set(amplitude = 0.0)
 '''
class eom_14(YaaxSequence):
    @kernel 
    def set(self, freq, att):
        self.mirny0_ch1.set_att(att)                   
        self.mirny0_ch1.sw.on()                                
        self.core.break_realtime()

        self.mirny0_ch1.set_frequency(freq)                  
        self.core.break_realtime()


        self.mirny0_almazny.init()
        self.mirny0_almazny.set_att(1, 10)
        
        self.mirny0_almazny.output_toggle(True)

    def off(self):
        self.mirny0_almazny.output_toggle(False)
 '''