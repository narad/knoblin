class Knob:

    def __init__(self, name: str, degrees: int, min_position: int, max_position: int, last_position:int=None):
        self.name = name
        self.min_position = min_position
        self.max_position = max_position
        self.last_position = last_position
        self.center_position = min_position + ((max_position- min_position) / 2)
        self.degrees = degrees

    def extent(self):
        return self.max_position - self.min_position

    def mid_position(self):
        return self.min_position + (self.extent() / 2)



class ActuatedKnob:

    def __init__(self, knob, servo, attachment):
        self.knob = knob 
        self.servo = servo 
        self.attachment = attachment
        self.name = knob.name



    def knob2servo_degrees(self, knob_degree):
        # ratio between extent of servo and knob
        degree_diff = self.knob.degrees - self.servo.degrees

        # min attach
        # servo degree = 270 (kn)
        # servo degree = 10 (knob degree should be)

#        servo_percent = (servo_degree / servo.rotation)

        if self.attachment == "max":
            return knob_degree - degree_diff
        elif self.attachment == "min":
            return knob_degree
        else: # centered
            return knob_degree - int(degree_diff / 2)


    def servo2knob_degrees(self, servo_degree):
        # ratio between extent of servo and knob
        degree_diff = self.knob.degrees - self.servo.degrees

        # min attach
        # servo degree = 270 (kn)
        # servo degree = 10 (knob degree should be)

#        servo_percent = (servo_degree / servo.rotation)

        if self.attachment == "max":
            return servo_degree + degree_diff
        elif self.attachment == "min":
            return servo_degree
        else: # centered
            return servo_degree + int(degree_diff / 2)



    def command_from_position(self, position):
#        print(self.is_reachable_position(position))

        print(f"{self.knob.name}: -> {position}/{self.knob.max_position}")

        print(self.knob.extent())

        # # ratio between extent of servo and knob
        # degree_diff = knob.rotation - servo.rotation
        # assert degree_diff >= 0, "Servo rotation exceeds knob rotation, not currently supported"

        # if self.attachment == "max":
        #     print("max attachment")
        # elif self.attachment == "min":
        #     pass
        # else: # centered
        #     pass


        # What percent of the knob rotation is it?
        knob_percent = (position-self.knob.min_position) / self.knob.extent()
        print("knob percent: ", knob_percent)

        # How many degrees does that relate to in the knob
        knob_rotation = knob_percent * self.knob.degrees
        print("knob rotation: ", knob_rotation)

        # What percent of the servo rotation corresponds to that knob rotation?
        servo_rotation = self.knob2servo_degrees(knob_rotation)
        print("servo rotation: ", servo_rotation)

        # Get corresponding servo control command
        pos_code = self.servo.command_code_by_angle(servo_rotation)

#        pos_code = self.servo.command_code(servo_rotation)
#        pos_code = self.servo.command_code(percent_rotation)
        print("position code: ", pos_code)
        return pos_code


    def calibration_position(self):
        if self.attachment == "max":
            return self.knob.max_position
        elif self.attachment == "min":
            return self.knob.min_position
        else: # centered
            return self.knob.center_position


    def is_valid(self, position):
        cmd = self.command_from_position(position)
        return cmd >= self.servo.min_pos and cmd <= self.servo.max_pos















    # def is_reachable_position(self):
    #     # ratio between extent of servo and knob
    #     degree_diff = knob.rotation - servo.rotation
    #     if degree_diff <= 0:
    #         return True


    #     if self.attachment == "max":
    #         print("max attachment")
    #     elif self.attachment == "min":
    #         pass
    #     else: # centered
    #         pass












#     def move(self, position, delay=0):
#         pos_code = self.command_from_position(position)

#         # Encode and send command via Arduino


# #        cmd = f"{self.servo.servo_id}:{pos_code}" #:{delay}" # old-style non-synchronous arduino code
#         cmd = ""
#         for i in range(10):
#             if i == self.servo.servo_id:
#                 cmd += f"{pos_code:03}"
#             else:
#                 cmd += "000"
#         print(cmd)
#         print()
#         self.arduino.write(cmd.encode())


#     def center(self):
#         self.move(self.knob.mid_position())


