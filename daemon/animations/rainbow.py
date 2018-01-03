import animations.common as common

"""Draw rainbow that fades across all pixels at once."""
class Anim:
	def __init__(self, zone, custom=None):
		self.zone = zone
		self.iters = 0
		self.length = zone.length
		self.gen_wheel(self.length)
		self.conf = custom
		self.whole = False
		if (self.conf != None and self.conf.get("fade_as_whole") == True):
			self.whole = True

	def gen_wheel(self, num):
		self.colors = []
		for i in range(self.length):
			self.colors.append(common.col_wheel(i, self.length))

	def iter(self):
		if (self.whole):
			for pos in range(self.length):
				self.zone.setpixel(pos, self.colors[self.iters])
			self.iters = (self.iters + 1) % len(self.colors)
		else:
			for pos in range(self.length):
				self.zone.setpixel(pos, self.colors[(pos + self.iters) % self.length])
			self.iters = (self.iters + 1) % self.length
