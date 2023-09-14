from sipyco.pc_rpc import Client


def main():
    remote = Client("::1", 443, "oven")
    try:
        remote.command('Syst:loc')
    finally:
        remote.close_rpc()

if __name__ == "__main__":
    main()