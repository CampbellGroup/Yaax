from artiq.experiment import*                                   

class Almazny_Frequency_TEST(EnvExperiment):
    """Y TEST V1.2 Almazny Single Frequency"""
    def build(self): 
        self.setattr_device("core")
        self.setattr_device("mirny0_ch0")                           
        self.setattr_device("mirny0_ch1")
        self.setattr_device("mirny0_ch2")
        self.setattr_device("mirny0_ch3")
        self.setattr_device("mirny0_almazny")                

        self.setattr_argument("Frequency", NumberValue(default = 4000e6, ndecimals=3, step=.001, unit = 'MHz'), group = "Almazny TEST", tooltip = "[MHz] | Frequency output on Almazny0 CH0")
        self.setattr_argument("Attenuation", NumberValue(10, ndecimals=3, step=.001, unit = "dB"), group = "Almazny TEST", tooltip = "[dB] | Attenuation on Almazny0 CH0")
        self.setattr_argument("Turn_on_length", NumberValue(1, ndecimals=3, step=.001, unit = "s"), group = "Almazny TEST", tooltip = "[s] | Turn on Almazny0 CH0 for this long for testing")

    @kernel 
    def run(self):  
        self.core.reset()                                      

        self.mirny0_ch0.cpld.init()
        self.mirny0_ch0.init()                                 
        delay(10 * ms)                                        
        self.mirny0_ch1.cpld.init()
        self.mirny0_ch1.init()                                 
        delay(10 * ms)    
        self.mirny0_ch2.cpld.init()
        self.mirny0_ch2.init()                                 
        delay(10 * ms)    
        self.mirny0_ch3.cpld.init()
        self.mirny0_ch3.init()                                 
        delay(10 * ms)    
        freq = self.Frequency                                  
        attenuation= self.Attenuation                       

        
        self.mirny0_ch1.set_att(attenuation)                   
        self.mirny0_ch1.sw.on()                                
        self.core.break_realtime()

        self.mirny0_ch1.set_frequency(freq)                  
        self.core.break_realtime()

        self.mirny0_ch1.set_att(30*dB)


        #self.mirny0_almazny.init()
        #self.mirny0_almazny.set_att(2, attenuation)
        
        #self.mirny0_almazny.output_toggle(True)

        delay(self.Turn_on_length)                         
        self.mirny0_almazny.output_toggle(False)

        self.mirny0_ch0.sw.off()     
        self.mirny0_ch1.sw.off() 
        self.mirny0_ch2.sw.off() 
        self.mirny0_ch3.sw.off() 