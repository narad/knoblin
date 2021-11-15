

class Servo270:
	# constants for 270 degree servo
	min_pos = 125
	max_pos = 575
	mid_pos = 350
	degrees = 270


	def __init__(self, servo_id: int) -> None:
		self.servo_id = servo_id


	def command_code(self, percent_rotation: float) -> int:
		ratio = (self.max_pos - self.min_pos) #/ 360
		new_pos = (percent_rotation * ratio) + self.min_pos # 360 * ratio) + self.min_pos
		return int(new_pos)

	def command_code_by_percent(self, percent_rotation: float) -> int:
		ratio = (self.max_pos - self.min_pos) #/ 360
		new_pos = (percent_rotation * ratio) + self.min_pos # 360 * ratio) + self.min_pos
		return int(new_pos)

	def command_code_by_angle(self, angle: float) -> int:
		percent_rotation = angle / self.degrees
		ratio = (self.max_pos - self.min_pos) #/ 360
		new_pos = (percent_rotation * ratio) + self.min_pos # 360 * ratio) + self.min_pos
		return int(new_pos)
