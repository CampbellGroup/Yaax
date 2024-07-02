from artiq.experiment import *


class ReadPMT(EnvExperiment):
    """Read PMT"""

    def build(self):
        self.setattr_device('core')
        self.setattr_device('scheduler')
        #Set up attributes
        self.setattr_device("core")                                                                                      
        self.setattr_device("ttl0")             

        #Setting arguments
        self.setattr_argument("interrogation_time",  NumberValue(ndecimals = 7, type= "float", unit = "ms" ))       #How long the counts are read

    def run(self):
        self.set_dataset("pmt_counts", [0], broadcast=True, archive=True)               #sets up dataset so we can plot and save counts

        
        try:
            while True:
                while self.scheduler.check_pause():
                    # Pause the scan
                    print('pausing')
                    self.core.comm.close()  # Close communications before pausing
                    self.scheduler.pause()  # Can raise a TerminationRequested exception
                    print('resuming')

                # Some long kernel
                PMT = self._run()

        except TerminationRequested:
            print('Gracefully terminating such that hdf5 file will be written')

    

    @kernel
    def _run(self):
        delay(10 * ms)
        
        while True:
            delay(1 * ms)
            #self.core.wait_until_mu(now_mu())

            self.core.reset()
            self.ttl0.input()                                       #sets TTL0 as an input

            tint = self.interrogation_time
            delay(1*us)                               
            counts = self.ttl0.count(self.ttl0.gate_rising(tint))             #collects counts during 'tint', and then offloads them into 'counts'
            #print("counts: ", counts)  
            delay(1*ms)                         
            self.append_to_dataset("pmt_counts", counts/tint)         #saves counts

            # Check if there is a pause condition once in a while
            if self.scheduler.check_pause():
                # Interrupt current work
                break