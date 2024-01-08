from sipyco.pc_rpc import simple_server_loop

class Hello:
    def message(self, msg):
        print("message: " + msg)
    
    def ping(self):                 # used by the controller manager
        return True

def main():
    simple_server_loop({"hello": Hello()}, "::1", 3249)



if __name__ == "__main__":
    main()