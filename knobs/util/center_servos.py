import serial
from connect_arduino import get_port_name

from time import sleep

center_pos = 350

def center(arduino, num_knobs=10, tries=3):
    for i in range(num_knobs):
        for _ in range(tries):
            cmd = f"{i}:{center_pos}"
            arduino.write(cmd.encode())
            sleep(2)


if __name__ == '__main__':
    # get Arduino port name
    port_name = get_port_name(verbose=True)
    print(port_name)

    # create serial object for arduino control
    arduino = serial.Serial(port_name, 9600)  
    # print("still here") 
    # arduino.write("0:150".encode())
    # sleep(2)
    # arduino.write(f"0:450".encode())
    # sleep(2)

    # center the knobs
    center(arduino)