from artiq.experiment import*                                   #imports everything from the artiq experiment library

#This code outputs a single frequency at a fixed amplitude on a single channel of the urukul
#the output frequency must be inputted in MHz from the dahsboard
#The ouput persists for 2 seconds and the turns off



class linescan(EnvExperiment):
    def build(self): #This code runs on the host device
        
        self.setattr_device("core")                                                         #sets core device drivers as attributes
        self.setattr_device("urukul0_ch1")                                                  #sets urukul0, channel 1 device drivers as attributes
        self.setattr_device("core")                                                         #sets drivers for core device as attributes
        self.setattr_device("ttl0")                                                         #sets drivers for TTL0 as attributes
        self.setattr_argument("freq", NumberValue(ndecimals=0, step=1))                     #instructs dashboard to take input and set it as an attribute called freq

    def prepare(self):
        #Initialize variables
        delta = -2
        f = self.freq
        self.steps = 5
        self.fscan = [0]*self.steps

        for i in range(self.steps):
            self.fscan[i]= f + delta
            delta = delta + 1

    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul0_ch1.cpld.init()                            #initialises CPLD on channel 1
        self.urukul0_ch1.init()                                 #initialises channel 1
        self.ttl0.input()                                       #sets TTL0 as an input
                                                                #this can also be achieved with a fixed delay
        
        amp = 1.0                                               #defines amplitude variable as an amplitude scale factor(0 to 1)
        attenuation= 1.0                                        #defines attenuation variable
        
        self.urukul0_ch1.set_att(attenuation)                   #writes attenuation to urukul channel
        self.urukul0_ch1.sw.on()                                #switches urukul channel on
           
        for i in range(self.steps):
            self.urukul0_ch1.set(1*MHz, amplitude = amp)        #writes frequency and amplitude variables to urukul channel thus outputting function   
        
            self.ttl0.sample_input()                #reads current value of TTL0 
            input = self.ttl0.sample_get()          #stores value of TTL0 as input varibale
            print(input)                            #prints value of input variable

            delay(1*ms)

        self.urukul0_ch1.sw.off()                                           #switches urukul channel off


