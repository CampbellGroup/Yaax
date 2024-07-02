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


        self.setattr_argument("freq0", NumberValue(default = 3070e6, ndecimals=3, step=.001, unit = 'MHz'), 
                               group = "935_EOM", tooltip = "[MHz] | Frequency output for 935_EOM")
        self.setattr_argument("att0", NumberValue(10, ndecimals=3, step=.1, unit = "dB"), 
                              group = "935_EOM", tooltip = "[dB] | Attenuation for 935_EOM")
        self.setattr_argument("t0", NumberValue(1, ndecimals=3, step=.001, unit = "s"), 
                              group = "935_EOM", tooltip = "[s] | Turn the 935EOM for testing")
        self.setattr_argument("Test_Toggle_935Repump", EnumerationValue(["on", "off"]),
                              group = "935_EOM", tooltip = "Toggle Turn on Length")
        

        self.setattr_argument("freq1", NumberValue(default = 2105e6, ndecimals=3, step=0.1, unit = 'MHz'), 
                               group = "369_EOM_OP", tooltip = "[MHz] | Frequency output for 369_EOM_OP")
        self.setattr_argument("att1", NumberValue(10, ndecimals=3, step=.1, unit = "dB"), 
                              group = "369_EOM_OP", tooltip = "[dB] | Attenuation for 369_EOM_OP")
        self.setattr_argument("t1", NumberValue(1, ndecimals=3, step=.001, unit = "s"), 
                              group = "369_EOM_OP", tooltip = "[s] | Turn the 369_EOM_OP for testing")
        self.setattr_argument("Test_Toggle_OP", EnumerationValue(["on", "off"]),
                              group = "369_EOM_OP", tooltip = "Toggle Turn on Length")

        
        self.setattr_argument("freq2", NumberValue(default = 7377e6, ndecimals=3, step=.001, unit = 'MHz'), 
                               group = "369_EOM_DC", tooltip = "[MHz] | Frequency output for 369_EOM_DC")
        self.setattr_argument("att2", NumberValue(10, ndecimals=3, step=.1, unit = "dB"), 
                              group = "369_EOM_DC", tooltip = "[dB] | Attenuation for 369_EOM_DC")
        self.setattr_argument("t2", NumberValue(1, ndecimals=3, step=.001, unit = "s"), 
                              group = "369_EOM_DC", tooltip = "[s] | Turn the 369_EOM_DC for testing")
        self.setattr_argument("Test_Toggle_DC", EnumerationValue(["on", "off"]),
                              group = "369_EOM_DC", tooltip = "Toggle Turn on Length")



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
        self.mirny0_almazny.init()                                 
        delay(10 * ms)    
        self.mirny0_ch3.cpld.init()
        self.mirny0_ch3.init()                                 
        delay(10 * ms)   

        #Collect Variables: 
        freq0 = self.freq0                                 
        att0  = self.att0       
        freq1 = self.freq1                                 
        att1  = self.att1
        freq2 = self.freq2                                 
        att2  = self.att2              

        #Mirny Channel 0 (935 eom)
        self.mirny0_ch0.set_att(att0)                   
        self.mirny0_ch0.sw.on()                                
        self.core.break_realtime()
        self.mirny0_ch0.set_frequency(freq0)                  
        self.core.break_realtime()

        #Mirny Channel 1 (369 eom OP)
        self.mirny0_ch1.set_att(att1)                   
        self.mirny0_ch1.sw.on()                                
        self.core.break_realtime()
        self.mirny0_ch1.set_frequency(freq1)                  
        self.core.break_realtime()

        #Mirny Channel 2 (369 eom DC)
        self.mirny0_ch2.set_att(att2)                   
        self.mirny0_ch2.sw.on()                                
        self.core.break_realtime()
        self.mirny0_ch2.set_frequency(freq2/2)                  
        self.core.break_realtime()
        
        #The Almazny Starts here
        self.core.break_realtime()
        self.mirny0_almazny.set_att(2, att2)
        self.mirny0_almazny.output_toggle(True)

        #IN CASE WE NEED TO TURN IT OFF
        
        if self.Test_Toggle_935Repump == "on" : 
            delay(self.t0)
            self.mirny0_ch0.sw.off() 

        if self.Test_Toggle_OP == "on" : 
            delay(self.t1)
            self.mirny0_ch1.sw.off()

        if self.Test_Toggle_DC == "on" : 
            delay(self.t2)
            self.mirny0_ch2.sw.off()
            self.mirny0_almazny.output_toggle(False)
                                   

        self.mirny0_ch3.sw.off() 