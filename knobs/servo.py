
# constants for 270 degree servo
min_pos = 125
max_pos = 575
mid_pos = 350

class Servo270:

	def __init__(self, servo_id):
		self.servo_id = servo_id


	def command_code(self, percent_rotation):
		ratio = (max_pos - min_pos) / 360
		return min_pos + (percent_rotation * ratio)


# in gui change a dial
# dial sends the knob value
# knob-value -> servo-command