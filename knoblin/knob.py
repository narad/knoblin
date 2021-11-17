class Knob:
    """
    The Knob class represents a physical knob or potentiometer, with 
    physical parameters, such as the degree of rotation possible.  It
    can be combined with a Servo in an ActuatedKnob object to support
    control.
    """

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
    """
    An ActuatedKnob class supports control methods for a physical knob.
    It handles annoying aspects of the physical coupling, like mismatches
    between maximum rotation sweeps between the servo and knob, and 
    computes appropriate servo position codes for specific knob settings
    regardless of such mismatches.
    """

    def __init__(self, knob, servo, attachment):
        self.knob = knob 
        self.servo = servo 
        self.attachment = attachment
        self.name = knob.name



    def knob2servo_degrees(self, knob_degree: int) -> int:
        """
        Given the degree of the knob rotation, return the corresponding
        degree of the attached servo.

        Args:
            knob_degrees (int): a knob position expressed in degrees.
        Returns:
            int: the degree of the servo
        """
        degree_diff = self.knob.degrees - self.servo.degrees
        if self.attachment == "max":
            return knob_degree - degree_diff
        elif self.attachment == "min":
            return knob_degree
        else: # centered
            return knob_degree - int(degree_diff / 2)


    def servo2knob_degrees(self, servo_degree) -> int:
        """
        Given the degree of the servo rotation, return the corresponding
        degree of the attached knob.

        Args:
            servo_degree (int): a servo position expressed in degrees.
        Returns:
            int: the degree of the knob
        """
        degree_diff = self.knob.degrees - self.servo.degrees
        if self.attachment == "max":
            return servo_degree + degree_diff
        elif self.attachment == "min":
            return servo_degree
        else: # centered
            return servo_degree + int(degree_diff / 2)



    def command_from_position(self, position):
        """
        Computes the command code, the str which will direct 

        Args:
            position (int): the positon of the knob
        Returns:
            str: the appropriate command code to move the knob to
                 the given position.
        """
        # print(f"{self.knob.name}: -> {position}/{self.knob.max_position}")
        # print(self.knob.extent())

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

        print("position code: ", pos_code)
        return pos_code


    def calibration_position(self):
        """
        Returns the calibration position of the knob.  For instance if
        the knob is valued 0-10, and the attachment type is 'center',
        it will return 5.

        Returns:
            str: the appropriate command code to move the knob to
                 the given position.
        """
        if self.attachment == "max":
            return self.knob.max_position
        elif self.attachment == "min":
            return self.knob.min_position
        else: # centered
            return self.knob.center_position


    def is_valid(self, position):
        """
        Tests if the knob position is valid.  Positions become invalid
        when the servo is incapable of turning the knob to those
        positions (because of range limitation mismatch).

        Args:
            position (int): the knob position.
        Returns:
            bool: whether the servo can turn the knob to the position.
        """
        cmd = self.command_from_position(position)
        return cmd >= self.servo.min_pos and cmd <= self.servo.max_pos
