from sipyco.pc_rpc import Client


def main():
    remote = Client("::1", 541, "oven")
    try:
        remote.command('OUTP 0')
    finally:
        remote.close_rpc()

if __name__ == "__main__":
    main()