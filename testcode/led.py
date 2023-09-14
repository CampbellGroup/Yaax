from artiq.experiment import *

def input_led_state() -> TBool:
    return input("Enter desired LED state: ") == "1"

class LED(EnvExperiment):
    """LED AND OVEN"""
    def build(self):
        self.setattr_device("core")
        self.setattr_device("led1")
        self.setattr_device("led0")
        #self.setattr_device("oven")

    @kernel
    def run(self):
        self.core.reset()
        s = input_led_state()
        self.core.break_realtime()
        if s:
            self.led1.on()
            #self.oven.command('APP:VOLT 3')
        else:
            self.led1.off()
            #self.oven.command('APP:VOLT 0')