from artiq.experiment import *
import numpy as np

class Rabi_Flopping( EnvExperiment):
    '''
    Rabi Flopping Experiment

    1) Doppler cooling subseq
        - 369 on, detuned by 10MHz red
            - also with Doppler Cooling tone on (14GHz)
        - 935 on

    2) State Prep
        - 369 on, no detuning
            - Optical pumping tone on (2.1GHz)
        - 935 on

    3) Apply Microwave
        - 12.64GHz on, fixed power
        - variable pulse time (changes per loop)

    4) State Detection
        - 369 on, no tones or detuning
        - collect PMT data
    
    5) Repeat steps 1) - 4), with different pulse time in 3).

    7/6/23 - don't worry about the DDS in the microwave system for now.
    '''
    def build(self):
        self.setattr_device("core")
        
        ### Double check the channels used
        
        # DDS channels
        self.setattr_device("urukul0_ch0") # 369 double pass AOM
        self.setattr_device("urukul1_ch0") # 935 AOM
        # self.setattr_device("urukul2_ch0") # u2_ch0 = 600 MHz signal output

        # TTL channels
        self.setattr_device("ttl0") # ttl0 = 12.64 GHz signal switch
        self.setattr_device("ttl1") # ttl1 = 14GHz source for EOM (DC tone)
        self.setattr_device('ttl2') # ttl2 = 2.1GHz source for EOM (Optical Pumping tone)
        self.setattr_device('ttl3') # ttl3 = input channel; receives output from PMT

        # Timings (need to be int!)
        self.time_DC = 10   # ms; Doppler Cooling time
        self.time_SP = 50   # us; state prep time
        self.time_SD = 10   # us; state detection time, which is also the same as the interrogation time for PMT counts
        self.time_BTWN = 10  # ms; pause time between each cycle

        # Microwave times: vary microwave pulse lengths per loop
        start = 0           # us
        end = 1000          # us
        stepsize = 2        # us
        self.times_MW = np.arange(start, end + stepsize, stepsize)  # (end-inclusive)


        ### DDS channel settings. Using arbitrary values for 369 for now because we don't have one yet.
        
        # 935 AOM on
        self.amp935 = 0.208 
        self.atten935 = 0.0
        self.AOMfreq935 = 80.0*MHz    # MHz (freqs should also be float)

        # 369 AOM values (to be changed later)
        amp369 = 0.2
        atten369 = 0.0
        AOMfreq369 = 200.0*MHz            # MHz, frequency of AOM s.t. 369 is *not* detuned
        AOMfreq369_detuned = 75.0*MHz     # MHz, frequency of AOM s.t. 369 is detuned red by 10 MHz

        # 369 AOM
        self.amp369 = amp369
        self.atten369 = atten369
        self.AOMfreq369 = AOMfreq369
        self.AOMfreq369_detuned = AOMfreq369_detuned    

        # Number of repetitions *per* microwave pulse time:
        self.reps = 100

    @kernel
    def run(self):
        
        # Initialize here
        self.core.reset()

        # initialize channels
        self.urukul0_ch0.cpld.init()
        self.urukul0_ch0.init()
        self.urukul1_ch0.cpld.init()
        self.urukul1_ch0.init()

        self.ttl0.output()
        self.ttl1.output()
        self.ttl2.output()
        self.ttl3.input()
        
        # initialize PMT dataset
        self.set_dataset("Rabi_Exp_Counts", np.full((len(self.times_MW), self.reps), np.nan), 
                         broadcast = True, archive = True)

        delay(1*ms)        # a delay is needed after .set_dataset() to prevent underflow error

        ### Experiment/Core Loop ###

        for i in range(len(self.times_MW)):
            
            time_MW = self.times_MW[i]
            current_counts = np.full(self.reps, 0)    # .mutate_dataset() needs the input to be the same datatype as the dataset, so need a list/array to hold and then append
 
            # Sample each pulse time for a set amount of repetitions:
            for j in range(0, self.reps):
                
                
                # print("Currently on loop: ", j)

                # delay(10 * ms)

                ### Doppler Cooling

                # 369 on, 10MHz detuned
                self.urukul0_ch0.set_att(self.atten369)
                self.urukul0_ch0.sw.on()
                self.urukul0_ch0.set(self.AOMfreq369_detuned, amplitude = self.amp369)

                # add DC tone
                #self.ttl1.on()

                # 935 on
                self.urukul1_ch0.set_att(self.atten935)
                self.urukul1_ch0.sw.on()
                self.urukul1_ch0.set(self.AOMfreq935, amplitude = self.amp935)

                delay(150 * ms)    # leave on for DC time

                #self.ttl1.off()              
                
                # End of Doppler Cooling section

                ### State Preparation
                
                # 369 stays on, but no detuning
                self.urukul0_ch0.set(self.AOMfreq369, amplitude = self.amp369)

                # add OP tone
                #self.ttl2.on()

                # 935 stays on

                delay(150 * ms)    # leave on for SP time

                #self.ttl2.off()
                self.urukul0_ch0.sw.off()   # turn off 369 before microwave section
                self.urukul1_ch0.sw.off()   # turn off 935 before microwave section

                # End of State Prep

                ### Apply microwave pulse - variable time goes here

                # pulse microwave; yes there is a .pulse() for TTLs, but it's nice to just work with delay blocks
                #self.ttl0.on()
                delay(150 * ms)
                #self.ttl0.off()

                # End of microwave pulse

                ### State Detection

                # 369 on, no detuning, no tones:
                self.urukul0_ch0.set_att(self.atten369)
                self.urukul0_ch0.sw.on()
                self.urukul0_ch0.set(self.AOMfreq369, amplitude = self.amp369)

                # collect data from PMT:
                counts = self.ttl3.count(self.ttl3.gate_rising(self.time_SD * us))
    
                delay(150 * ms)     # delay time between repetitions

                print("Counts for pulse length ", time_MW, "us, rep #", j, ":", counts)
                current_counts[j] = counts     # collecting and adding to dataset need to be separated by a delay I guess?

            # add to dataset and delay: Careful with the indices
            # Likely have to deal with np.array dim issue here

            self.mutate_dataset("Rabi_Exp_Counts", [i, 0], current_counts)  # ith pulse length, jth rep 
            delay(1 * ms)


        # Shut off
        delay(1 * ns)
        self.urukul0_ch0.sw.off()
        self.urukul1_ch0.sw.off()
        self.ttl0.off()
        self.ttl1.off()
        self.ttl2.off()
        self.ttl3.off()




