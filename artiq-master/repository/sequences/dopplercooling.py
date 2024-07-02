from artiq.experiment import*                                   #imports everything from the artiq experiment library
from base.base_defs import*
import base.base_experiment 
from base.base_environment import YaaxEnvironment

class cooling_seqs(base.base_experiment.YaaxExperiment, YaaxEnvironment):
    """doppler_cooling"""
    def build_exp(self):
        #Define all the aoms you need for the experiment
        self.aom935 = aom_935dp(self)     
        self.aom369dp = aom_369dp(self)
    '''
    def prepsettings(self,amp935,att935,amp369,att369,freq369, detune369, ion):
        # 935 AOM on
        self.amp935 = amp935
        self.atten935 = att935
        self.AOMfreq935 = 200.0 * MHz              # MHz (freqs should also be float)

        # 369 AOM values (to be changed later)
        atten369 = att369
        AOMfreq369 = freq369                # MHz, frequency of AOM s.t. 369 is *not* detuned
        AOMfreq369_detuned = detune369      # MHz, frequency of AOM s.t. 369 is detuned red by 10 MHz

        # 369 AOM
        self.amp369 = amp369
        self.atten369 = atten369
        self.AOMfreq369 = AOMfreq369
        self.detuned369 = AOMfreq369 - AOMfreq369_detuned

        #This is the isotope selection
        self.ion = ion
        #print(amp935,att935,amp369,att369,freq369, detune369, ion)
    '''
    @kernel 
    def dopplercool(self,detuned369,amp369,freq935,amp935):    
        self._initialize()   
        self.core.break_realtime()

        with parallel:
            self.aom369dp.set(freq = detuned369, amp = amp369)
            self.aom935.set(freq = freq935, amp = amp935)


        
        
        