class Knob:

    def __init__(self, name, servo_id, min_position, max_position, last_position=None):
        self.name = name
        self.servo_id = servo_id
        self.min_position = min_position
        self.max_position = max_position
        self.last_position = last_position
