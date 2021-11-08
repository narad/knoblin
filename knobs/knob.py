class Knob:

    def __init__(self, name, min_position, max_position, last_position=None):
        self.name = name
        self.min_position = min_position
        self.max_position = max_position
        self.last_position = last_position


class ActuatedKnob:

    def __init__(self, knob, servo, arduino):
        self.knob = knob 
        self.servo = servo 
        self.arduino = arduino 


    def move(self, position, delay=0):
        print(f"{self.knob.name}: -> {position}/{self.knob.max_position}")
        position = 125 + (position * 40)
        cmd = f"{self.servo.servo_id}:{position}" #:{delay}"
        print(cmd)
        print(cmd.encode())
        self.arduino.write(cmd.encode())


