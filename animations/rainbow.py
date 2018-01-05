import animations.common as common

"""Draw rainbow that fades across all pixels at once."""
class Anim:
	def __init__(self, length, func, config):
		self.iters = 0
		self.length = length
		self.setpixel = func
		self.conf = config
		if (self.conf != None):
			self.whole = self.conf.get("fade_as_whole", True)
			self.steps = self.conf.get("steps", self.length)
		self.gen_wheel(self.steps)

	def gen_wheel(self, num):
		self.colors = []
		for i in range(num):
			self.colors.append(common.col_wheel(i, num))

	def iter(self):
		if (self.whole):
			for pos in range(self.length):
				self.setpixel(pos, self.colors[self.iters])
			self.iters = (self.iters + 1) % len(self.colors)
		else:
			for pos in range(self.length):
				self.setpixel(pos, self.colors[(pos + self.iters) % self.length])
			self.iters = (self.iters + 1) % self.length
