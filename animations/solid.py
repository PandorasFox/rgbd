import animations.common as common

class Anim:
	def __init__(self, length, func, config):
		self.length = length
		self.setpixel = func
		self.config = config
		self.color = common.from_hex(self.config.get("color"))

	def iter(self):
		for i in range(self.length):
			self.setpixel(i, self.color)

