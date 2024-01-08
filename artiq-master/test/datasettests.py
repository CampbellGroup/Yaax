from artiq.experiment import *                                                            #imports everything from the artiq experiment library
import time
import numpy as np
from base_environment import YaaxEnvironment
#from base_experiment import*
import pandas as pd 


class Datatest(Experiment, YaaxEnvironment):
    """Datatest"""
    def build(self): #This code runs on the host device
        self.setattr_device("core")                                                        #sets core device drivers as attributes
        self.reps = 100

    
    @kernel #This code runs on the FPGA
    def run(self):  
        
        self.set_dataset("differential_counts", np.full((self.reps, 3), np.nan), broadcast=True, archive=True)               #sets up dataset so we can plot and save counts

        for i in range(self.reps):
            counts_on = i
            counts_off = i-1

            diff_counts = counts_on - counts_off

            data = np.array([counts_on, counts_off, diff_counts])

            self.mutate_dataset("differential_counts", [i], data)

    