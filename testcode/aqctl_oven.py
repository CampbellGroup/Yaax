from sipyco.pc_rpc import simple_server_loop
import pyvisa as visa

class OvenControl():
    def command(self, cmd):
        rm = visa.ResourceManager('C:\\WINDOWS\\system32\\visa32.dll')
        prt = 'ASRL11::INSTR'
        inst = rm.open_resource(prt)
        inst.write('SYST:REM')
        inst.write('APP: CURR 7')
        inst.write('INST:COM:PAR')
        inst.write('OUTP 1')
        print("pushed ", cmd)

def main():
    simple_server_loop({"oven": OvenControl()}, "::1", 541)

if __name__ == "__main__":
    main()