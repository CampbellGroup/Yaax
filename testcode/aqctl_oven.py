from sipyco.pc_rpc import simple_server_loop
import pyvisa as visa

class OvenControl:
    def command(self, cmd):
        rm = visa.ResourceManager('C:\\WINDOWS\\system32\\visa32.dll')
        prt = 'ASRL6::INSTR'
        inst = rm.open_resource(prt)
        inst.write('SYST:REM')
        inst.write(cmd)

def main():
    simple_server_loop({"oven": OvenControl()}, "::1", 443)

if __name__ == "__main__":
    main()