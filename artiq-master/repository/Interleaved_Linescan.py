from artiq.experiment import*                            
import numpy as np

class Interleaved_Linescan(EnvExperiment):
    """Interleaved Linescan
       Performs a frequency sweep on the uk00 DDS (369nm DP setup). In between each interogation step, we apply Doppler cooling light to keep the ion cool. 
    """
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                                                  # Sets core device drivers as attributes
        self.setattr_device("urukul0_ch0")                                                                           # Activation of Urukul channel for the 369DP AOM 
        self.setattr_device("urukul1_ch0")                                                                           # Activation of Urukul channel for the 935 AOM
        self.setattr_device("ttl0")                                                                                  # Activate the PMT TTL
                                                   
        self.setattr_argument("repump_935_freq", NumberValue(ndecimals=7, type="float", unit="MHz"))                 # 935 AOM Freq
        self.setattr_argument("repump_935_amp", NumberValue(ndecimals=7, type="float", max=0.208))                   # Amplitude for the 935 AOM
        self.setattr_argument("repump_935_atten", NumberValue(type="float"))                                         # Attenuation for the 935 AOM

        self.setattr_argument("dp_369_freq", NumberValue(ndecimals=7, type="float", unit="MHz"))                     # Center frequency for 369 DP AOM
        self.setattr_argument("dopplercool_amp", NumberValue(ndecimals=7, type="float", max=0.38))                   # Amplitude for the DC pulses
        self.setattr_argument("interrogation_amp", NumberValue(ndecimals=7, type="float", max=0.38))                 # Amplitude for the interrogation pulses
        self.setattr_argument("dp_369_atten", NumberValue(type="float"))                                             # Attenuation for the 369 DP AOM

        self.setattr_argument("dopplercool_time", NumberValue(ndecimals=7, type="float", unit="us"))                 # How long the DC pulse is (5000us typical)
        self.setattr_argument("interrogation_time", NumberValue(ndecimals=7, type="float", unit="us"))               # How long the interrogation pulse is (100us typical)

        self.setattr_argument("reps", NumberValue(ndecimals=0, type="int", scale=1, step=1, max=10000))              # How many times to repeat the interrogation (100 typical)

        self.setattr_argument("dp_369_operational_freq", NumberValue(ndecimals=7, type="float", unit="MHz"))         # 369 DP AOM operational frequency
        self.setattr_argument("dp_369_operational_amp", NumberValue(ndecimals=7, type="float", max=0.38))            # 369 DP AOM operational amplitude
        self.setattr_argument("dp_369_operational_atten", NumberValue(type="float"))                                 # 369 DP AOM operational attenuation

        self.setattr_argument("scan", Scannable(default=CenterScan(200, 0.02,0.005), 
                                                global_min= 100, global_max = 300, 
                                                global_step = 1, unit = "MHz", scale = 1))

    def prepare(self):
        self.freqs = np.array([ i*MHz for i in self.scan])

    @kernel #This code runs on the FPGA
    def run(self):  

        self.core.reset()                                                                                            # Resets core device
        self.urukul0_ch0.cpld.init()                                                                                 # Initialises CPLD on channel 0
        self.urukul0_ch0.init()                                                                                      # Initialises channel 0
        self.urukul1_ch0.cpld.init()                                                                                 # Initialises CPLD on channel 1
        self.urukul1_ch0.init()                                                                                      # Initialises channel 1
        self.ttl0.input()                                                                                            # Sets TTL0 as an input (the PMT TTL)

        self.set_dataset("InterleavedLinescanFreqs", [0], broadcast=True, archive=True)        # Sets up dataset for plotting and saving
        self.set_dataset("InterleavedLinescanCounts", [0], broadcast=True, archive=True)       # Sets up dataset for plotting and saving
        #self.set_dataset("InterleavedLinescan", [0,0], broadcast=True, archive=True)

       
        # Sets the 935 AOM parameters, it doesn't change from pulse to pulse
        self.urukul1_ch0.set_att(self.repump_935_atten)                                                              # Sets attenuation for the 935 AOM
        self.urukul1_ch0.set(self.repump_935_freq, amplitude=self.repump_935_amp)                                    # Sets frequency and amplitude for the 935 AOM
        self.urukul0_ch0.set_att(self.dp_369_atten)                                                                  # Sets attenuation for the Doppler cooling pulse
        self.urukul0_ch0.set(self.dp_369_freq, amplitude=self.dopplercool_amp)                                       # Sets frequency and amplitude of the Doppler cooling AOM
        self.urukul1_ch0.sw.on()                                                                                     # Turns on 935 AOM
        self.urukul0_ch0.sw.on()                                                                                     # Turns on 369 DP AOM

        for i in range(len(self.freqs)):                                                                             # Iterates over all of the frequencies 

            dop_photons = 0                                                                                          # Collected photons to average over the reps
            int_photons = 0                                                                                          # Collected photons to average over the reps
            delay(1*ms)

            for j in range(self.reps):                                                                               # Repeats for statistics 

                # Doppler cooling section                                                                                                                   
                self.urukul0_ch0.set_att(self.dp_369_atten)                                                          # Sets attenuation for the Doppler cooling pulse
                delay(1*ms)
                self.urukul0_ch0.set(self.dp_369_freq, amplitude=self.dopplercool_amp)                               # Sets frequency and amplitude of the Doppler cooling AOM
                delay(1*ms)

                # Maybe we can do something with these photons?
                dop_counts = self.ttl0.count(self.ttl0.gate_rising(self.dopplercool_time))                           # Collect the Doppler cooling photons
                dop_photons += dop_counts                                                                            # Add Doppler cooling result of this rep to a list
                delay(1*ms)                                                                                          # Small delay to avoid overlaps

                # Interrogation section                                                                                                                        
                self.urukul0_ch0.set_att(self.dp_369_atten)                                                          # Sets attenuation for the interrogation pulse
                delay(1*ms)
                self.urukul0_ch0.set((self.freqs[i]), amplitude=self.interrogation_amp)                              # Sets frequency and amplitude of the interrogation pulse
                delay(1*ms)

                int_counts = self.ttl0.count(self.ttl0.gate_rising(self.interrogation_time))                         # Collect the interrogation photons
                int_photons += int_counts                                                                            # Add interrogation result of this rep to a list
                #print(int_photons)
                delay(1*ms)                                                                                          # Small delay to avoid overlaps

            dop_avg = dop_photons/self.reps                                                                          # Average the Doppler cooling results for this detuning 
            int_avg = int_photons/self.reps                                                                          # Average the interrogation results for this detuning

            #data = np.array([(self.dp_369_freq+self.freqs[i]*MHz), int_avg])                                         # Put the results in an array for storage
            self.append_to_dataset("InterleavedLinescanFreqs", self.freqs[i])                                         # Saves results in the Interleaved Linescan dataset
            self.append_to_dataset("InterleavedLinescanCounts", int_avg)                                              # Saves results in the Interleaved Linescan dataset
            #self.append_to_dataset("InterleavedLinescan", [self.freqs[i],int_avg])
            delay(1*ms)

        # A quick reset to operating parameters so we don't lose ions at the end of the sequences
        self.urukul0_ch0.set_att(self.dp_369_operational_atten)                                                      # Sets attenuation for the 369 DP
        self.urukul0_ch0.set(self.dp_369_operational_freq, amplitude=self.dp_369_operational_amp)                    # Sets frequency and amplitude for the 369 DP

        self.urukul0_ch0.sw.on()                                                                                     # Turns on 369 DP AOM 
        self.urukul1_ch0.sw.on()                                                                                     # Turns on 935 AOM