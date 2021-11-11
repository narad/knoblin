

class Servo270:
	# constants for 270 degree servo
	min_pos = 95
	max_pos = 600
	mid_pos = 350


	def __init__(self, servo_id: int) -> None:
		self.servo_id = servo_id


	def command_code(self, percent_rotation: float) -> int:
		ratio = (self.max_pos - self.min_pos) / 360
		new_pos = (percent_rotation * 360 * ratio) + self.min_pos
		return int(new_pos)
