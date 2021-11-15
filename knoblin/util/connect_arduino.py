from serial.tools import list_ports


def get_port_name(keyword: str='usbmodem', guess: bool=True, verbose: bool=True) -> str:
    # print("Arduino port not specified.  Attempting to identify...")
    ports = list_ports.comports()
    port_id = None

    # Try to guess
    if guess:
        try:
            port_id = [i for i,p in enumerate(ports) if keyword in str(p)][0]
            if verbose:
                print(f"Guessing port: {ports[port_id]}")
        # Force user to choose
        except:
            print("Could not guess.  Please specify manually.")

    # Prompt user for port selection
    if port_id is None:
        for i, port in enumerate(ports):
            print(f"{i+1}) {port}")
        port_id = int(str(input("choice:")).lower().strip())-1
    port_name_str = str(list_ports.comports()[port_id])
    return port_name_str[:port_name_str.index(' ')]


if __name__ == '__main__':
    print(f"Found Arduino Port Name: {get_port_name()}")
