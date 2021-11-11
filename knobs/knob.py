class Knob:

    def __init__(self, name: str, min_position: int, max_position: int, last_position:int=None):
        self.name = name
        self.min_position = min_position
        self.max_position = max_position
        self.last_position = last_position

    def extent(self):
        return self.max_position - self.min_position

    def mid_position(self):
        return self.min_position + (self.extent() / 2)



class ActuatedKnob:

    def __init__(self, knob, servo, arduino):
        self.knob = knob 
        self.servo = servo 
        self.arduino = arduino 


    def move(self, position, delay=0):
        print(f"{self.knob.name}: -> {position}/{self.knob.max_position}")

        print(self.knob.extent())

        # What percent of the knob rotation is it?
        percent_rotation = (position-self.knob.min_position) / self.knob.extent()
        print("percent rotation: ", percent_rotation)

        # Get corresponding servo control command
        pos_code = self.servo.command_code(percent_rotation)
        print("position code: ", pos_code)

        # Encode and send command via Arduino
        cmd = f"{self.servo.servo_id}:{pos_code}" #:{delay}"
        print(cmd)
        print()
        self.arduino.write(cmd.encode())


    def center(self):
        self.move(self.knob.mid_position())


