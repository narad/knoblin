import serial   
from serial.tools import list_ports
from time import sleep


def move(servo, position, increment=10):
    # move to 0
    arduino.write(f"{sid}:{0}".encode())

    cur = 0
    while cur < position:
        print(cur)
        arduino.write(f"{sid}:{cur + increment}".encode())
        sleep(0.05)
        cur += increment


if __name__ == '__main__':

    # Find Arduino port
    ports = list_ports.comports()    
    for i, port in enumerate(ports):
        print(f"{i+1}) {port}")
    port_ID = int(str(input("Which port is the Arduino port? ")).lower().strip())-1
    port_name = str(ports[port_ID])
    port_name = port_name[:port_name.index(' ')]
    print(port_name)

    # create serial object for arduino control
    arduino = serial.Serial(port_name, 9600)   
    arduino.write(f"0:450".encode())


    # while True:
    #     cmd = str(input("Which port is the Arduino port? ")).lower().strip()
    #     sid,pid = cmd.split(":")
    #     move(sid, int(pid))


