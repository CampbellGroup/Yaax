from sipyco.pc_rpc import simple_server_loop
import pyvisa as visa

class Oven:
    def __init__(self):
        self.rm = visa.ResourceManager('C:\\WINDOWS\\system32\\visa32.dll')
        self.prt = 'ASRL10::INSTR'
        self.inst = self.rm.open_resource(self.prt)
        self.inst.write('SYST:REM')

    def command(self, cmd):
        self.inst.write(cmd)
        print(cmd)

    def on(self):
        self.inst.write('OUTP 1')

    def off(self):
        self.inst.write('OUTP 0')

    def current(self, cmd):
        msg = 'APP:CURR ' + str(cmd)
        print(msg)
        self.inst.write(msg)
    
    def ping(self):                 # used by the controller manager
        return True

def main():
    simple_server_loop({"oven": Oven()}, "::1", 499)

if __name__ == "__main__":
    main()