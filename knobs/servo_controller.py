import serial   
from knobs.util.connect_arduino import get_port_name
from knobs.knob import Knob, ActuatedKnob
from knobs.servo import Servo270
from time import sleep

from typing import Dict, List


class KnobServoController:

    def __init__(self, knobs: List[ActuatedKnob]=[], port_name: str=None) -> None:
        # Acquire port ID
        if port_name is None:
            port_name = get_port_name()

        # Setup Arduino/Serial connection
        self.arduino = serial.Serial(port_name, 9600)

        # Create indexes
        self.name2knob = { knob.name : knob for knob in knobs }
        self.id2knob = { knob.servo.servo_id : knob for knob in knobs }


    def knobs(self):
        print("num knobs = ", self.num_knobs)
        return [self.id2knob[i] for i in range(self.num_knobs())]


    def num_knobs(self):
        return len(self.id2knob)


    def add_knob(self, knob_name: str, knob_type: int, servo_id: int, min_position: int, max_position: int, attachment: str) -> None:
        knob = Knob(knob_name,
                    knob_type,
                    min_position,
                    max_position)
        servo = Servo270(servo_id)
        aknob = ActuatedKnob(knob=knob,
                             servo=servo,
                             attachment=attachment)
        self.name2knob[knob_name] = aknob
        self.id2knob[servo.servo_id] = aknob


    def move(self, knob_name: str, position: int, delay:int=0) -> None:
        self.move_all({knob_name: position})
        # knob = self.name2knob[knob_name]
        # knob.move(position)


    def move_all(self, name2pos: Dict[str,int], delay:int=0) -> None:
        print(name2pos)
        cmd_str = ""
        for i in range(len(self.id2knob)):
            knob = self.id2knob[i]
            try:
                pos = name2pos[knob.name]
                cmd_code = knob.command_from_position(pos)
            except:
                cmd_code = 0
            print(cmd_code)
            cmd_str += f"{cmd_code:03}"
        print(cmd_str)
        print()
        self.arduino.write(cmd_str.encode())


    def move_to_calibration(self):
        print("in move to calib")
        print(self.knobs())
        name2pos = {}
        for knob in self.knobs():
            print("  ", knob.name)
            name2pos[knob.name] = knob.calibration_position()
        print("calibration dict: ", name2pos)
        self.move_all(name2pos)


    def is_valid(self, knob_name, position):
        return self.name2knob[knob_name].is_valid(position)



# 177 701 777 017 770


        # for name, pos in sorted(name2pos.values, key=lambda tup: self.servo_map[tup[0]].servo.servo_id):
        #     knob = self.servo_map[name]
        #     print(knob.servo.servo_id)
        #     pos = knob.command_from_position(name2pos[knob.name])


    # def center_knobs(self):
    #     for aknob in self.servo_map.values():
    #         print(f"centering knob {aknob.knob.name}...")
    #         aknob.center()
    #         sleep(2)





if __name__ == '__main__':
    factory = KnobControllerFactory()
    controller = factory.make_controller()  
    controller.loop()









#KnobServoController()









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