import serial   
from knobs.util.connect_arduino import get_port_name
from knobs.knob import Knob, ActuatedKnob
from knobs.servo import Servo270
from time import sleep


class KnobServoController:

    def __init__(self, knobs=[], port_name=None):
        # Acquire port ID
        if port_name is None:
            port_name = get_port_name()

        # Setup Arduino/Serial connection
        self.arduino = serial.Serial(port_name, 9600)   

        # Create name->knob mapping
        self.servo_map = { knob.name : knob for knob in knobs }


    def add_knob(self, knob_name, servo_id, min_position, max_position):
        knob = Knob(knob_name,
                     min_position,
                     max_position)
        servo = Servo270(servo_id)
        self.servo_map[knob_name] = ActuatedKnob(knob=knob,
                                                 servo=servo,
                                                 arduino=self.arduino)


    def move(self, knob_name, position, delay=0):
        knob = self.servo_map[knob_name]
        knob.move(position)


    def center_knobs(self):
        for aknob in self.servo_map.values():
            print(f"centering knob {aknob.knob.name}...")
            aknob.center()
            sleep(2)





if __name__ == '__main__':
    factory = KnobControllerFactory()
    controller = factory.make_controller()  #KnobServoController()
    controller.loop()






        # try:
        #     # If there's no history, move to center
        #     curr_pos = knob.last_position
        #     if knob.last_position is None:
        #         self.arduino.write(f"{knob.servo_id}:{mid_pos}".encode())
        #         curr_pos = mid_pos
        #     if curr_pos < position:
        #         print("trying something")
        #         while curr_pos < position:
        #             print(curr_pos)
        #             curr_pos += increment
        #             print(curr_pos)
        #             self.arduino.write(f"{knob.servo_id}:{curr_pos}".encode())
        #             sleep(2)
        #     if curr_pos > position:
        #         print("trying something else")
        #         while curr_pos > position:
        #             print(curr_pos)
        #             curr_pos -= increment
        #             self.arduino.write(f"{knob.servo_id}:{curr_pos}".encode())                    
        #             sleep(2)
        #     knob.last_position = position            
        # except:
        #     print(f"Error sending message to servo {knob.servo_id}.  Is it plugged in?")

    # def move(self, knob_name, knob_position):
    #     servo = self.servo_map[knob_name]
    #     pos = self.knob_to_servo_position(knob_position, knob_min, knob_max)
    #     self.move_servo(None, pos)








        # print(f"{knob.name}: -> {position}/{knob.max_position}")
        # position = 125 + (position * 40)
        # cmd = f"{knob.servo_id}:{position}" #:{delay}"
        # print(cmd)
        # print(cmd.encode())
        # self.arduino.write(cmd.encode())


    # def move_servo(self, servo, position, delay=0):
    #     print(f"Moving servo {servo} to position {position}")        
    #     command = f"{servo}:{position}:{delay}"
    #     print(command)
    #     command = command.encode()
    #     print(command)
    #     self.arduino.write(command)









    # def knob_to_servo_position(knob_position, knob_min, knob_max):
    #     servo_min = 125
    #     servo_max = 575
    #     return 350



# '/dev/cu.usbmodem14601'

# 0 == max CCW | 90 == stop | 180 == max CW

# command = str(0).encode()
# print(command)
# arduino.write(command)
# reachedPos = str(arduino.readline())
# time.sleep(4)

# #arduino.write("90".encode())
# #time.sleep(2)









#while True:                                             # create loop
 
# #        command = str(input ("Servo position: "))       # query servo position
# #        print("!" + command + "!")
#         command = str(pos) #"350"
#         command = command.encode()
#         print(command)
#         arduino.write(command)                          # write position to serial port

        # reachedPos = str(arduino.readline())            # read serial port for arduino echo
        # print(reachedPos)   


        # usbmodem1421