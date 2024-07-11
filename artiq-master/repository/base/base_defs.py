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


class eom_3GHZ(YaaxSequence):
    @kernel 
    def on(self, freq, att):
        v = freq
        at = att
        self.mirny0_ch0.set_att(at)                   
        self.mirny0_ch0.sw.on()                                
        self.core.break_realtime()

        self.mirny0_ch0.set_frequency(v)                  
        self.core.break_realtime()
    
    @kernel
    def off(self):
        self.mirny0_ch0.sw.off()

class eom_2GHZ(YaaxSequence):
    @kernel 
    def on(self, freq=4000*MHz, att=30*dB):
        v = freq
        at = att
        self.mirny0_ch1.set_att(at)                   
        self.mirny0_ch1.sw.on()                                
        self.core.break_realtime()

        self.mirny0_ch1.set_frequency(v)                  
        self.core.break_realtime()
    
    @kernel
    def off(self):
        self.mirny0_ch1.sw.off()


class eom_14GHZ(YaaxSequence):
    @kernel 
    def on(self, freq, att):
        v = freq
        at = att
        self.mirny0_ch3.set_att(at)                   
        self.mirny0_ch3.sw.on()                                
        self.core.break_realtime()

        self.mirny0_ch3.set_frequency(v)                  
        self.core.break_realtime()


        self.mirny0_almazny.init()
        self.mirny0_almazny.set_att(3, 10)
        
        self.mirny0_almazny.output_toggle(True)
    
    @kernel
    def off(self):
        self.mirny0_almazny.output_toggle(False)
