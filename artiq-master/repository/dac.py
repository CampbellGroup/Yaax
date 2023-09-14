from artiq.experiment import *                  #imports everything from artiq experiment library

#This code outputs a single voltage on a single Zotino channel

class Zotino_Single_Output(EnvExperiment):
    """Zotino Single Output"""
    def build(self): #this code runs on the host device

        self.setattr_device("core")             #adds drivers for core device as attributes
        self.setattr_device("zotino0")          #adds drivers for zotino board as attributes
        self.setattr_argument("voltage0", NumberValue( type = "float"))
        self.setattr_argument("voltage1", NumberValue( type = "float"))
        self.setattr_argument("voltage2", NumberValue( type = "float"))
        self.setattr_argument("voltage3", NumberValue( type = "float"))
        


    @kernel #this code runs on the FPGA
    def run(self): 
    
        self.core.reset()                       #resets core device      
        self.core.break_realtime()              #moves timestamp forward to prevent underflow
        
        self.zotino0.init()                           #initialises zotino0
        self.zotino0.write_dac(0,self.voltage0)       #writes voltage variable to DAC, channel 0
        self.zotino0.write_dac(1,self.voltage1)       #writes voltage variable to DAC, channel 1
        self.zotino0.write_dac(2,self.voltage2)       #writes voltage variable to DAC, channel 2
        self.zotino0.write_dac(3,self.voltage3)       #writes voltage variable to DAC, channel 3
        self.zotino0.load()                           #outputs previously loaded voltage