from artiq.experiment import *                                                            #imports everything from the artiq experiment library
import time
import numpy as np
from base_sequence import YaaxSequence
import pandas as pd 


class Datatest(YaaxSequence):
    """Datatest"""
    @kernel #This code runs on the FPGA
    def run(self):  
        for i in range(100):
            counts_on = i
            counts_off = i-1

            diff_counts = counts_on - counts_off

            data = np.array([counts_on, counts_off, diff_counts])
            print(data)

    