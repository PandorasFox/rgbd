import animations.common as common

"""Animation template
Must have a parent class Anim, that has an __init__ and an iter() function"""

class Anim:
	def __init__(self, length, func, config):
		self.length
		self.setpixel = func
		self.conf = config

	def iter(self):
		for i in range(self.length):
			self.setpixel(i, common.rgb(255, 0, 255))
