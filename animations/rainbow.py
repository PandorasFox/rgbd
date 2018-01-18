import animations.common as common

import sys
import fractions

"""Draw rainbow that fades across all pixels at once."""
class Anim:
	def __init__(self, length, func, config):
		self.iters = 0
		self.length = length
		self.setpixel = func
		self.conf = config
		self.whole = self.conf.get("strip_as_whole", True)
		self.steps = self.conf.get("steps", self.length)
		self.gen_wheel(self.steps)
		self.max_iters = self.length * self.steps // fractions.gcd(self.length, self.steps)

	def gen_wheel(self, num):
		self.colors = []
		for i in range(num):
			self.colors.append(common.col_wheel(i, num))

	def iter(self):
		if (self.whole):
			for pos in range(self.length):
				self.setpixel(pos, self.colors[self.iters])
			self.iters = (self.iters + 1) % self.steps
		else:
			for pos in range(self.length):
				self.setpixel(pos, self.colors[(pos + self.iters) % self.steps])
			self.iters = (self.iters + 1) % (self.max_iters)
