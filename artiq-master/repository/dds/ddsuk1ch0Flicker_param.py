from artiq.experiment import*                                   #imports everything from the artiq experiment library
import numpy as np
import h5py


class Flicker(EnvExperiment):
    """Urukul 1 Channel 0 Flicker_param"""
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                         #sets core device drivers as attributes
        self.setattr_device("urukul1_ch0")                                                  #sets urukul0, channel 0 device drivers as attributes
        
        self.setparam()
    
    def setparam(self):
        hdf = h5py.File("D:/Yaax/testcode/parametervault_v1.hdf5", "r")
        base_items = list(hdf.items())

        x = hdf.get('Urukul')
        dds = list(x.items())

        aomdp_935 = x.get('/Urukul/u1/c0')

        keys = list(aomdp_935.attrs.keys())
        vals = list(aomdp_935.attrs.values())

        self.amp = vals[0]
        self.attenuation = vals[1]
        self.freq = vals[2] * MHz

        hdf.close()
    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul1_ch0.cpld.init()                            #initialises CPLD on channel 0
        self.urukul1_ch0.init()                                 #initialises channel 0
        
        self.urukul1_ch0.set_att(self.attenuation)              #writes attenuation to urukul channel
        self.urukul1_ch0.sw.on()                                #switches urukul channel on
 
        self.urukul1_ch0.set(self.freq, amplitude = self.amp)   #writes frequency and amplitude variables to urukul channel thus outputting function

        delay(10* ms)

        for i in range(20):

            self.urukul1_ch0.sw.off()
            delay(250*ms)
            self.urukul1_ch0.sw.on()
            delay(250*ms)
        