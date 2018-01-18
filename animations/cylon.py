import animations.common as common

from colour import Color


"""Cylon style light pulsing forwards and back"""
class Anim:
	iters = 0
	forwards = True

	def __init__(self, length, func, config):
		self.length = length
		self.setpixel = func
		self.color = common.from_hex(config.get("color", "#ff00ff"))
		self.fade = config.get("fade", True)
		self.dark_color = common.from_hex("#000000")
		self.atonce = config.get("at_once", 1)

		if self.fade:
			self.gen_colors(config.get("color", "#ff00ff"))

	def gen_colors(self, cfg_color):
		self.colors = [self.color]

		if self.atonce == 1:
			return

		needed = (self.atonce - 1) // 2

		color = Color(cfg_color)
		for dist in range(1, needed + 1):
			color.luminance = color.luminance / ((dist + 1)**2)
			self.colors.append(common.from_colour(color))

	def iter(self):
		if self.iters >= self.length - 1:
			self.forwards = False
		elif self.iters <= 0:
			self.forwards = True

		colored = range(self.iters - self.atonce // 2, self.iters + self.atonce // 2 + 1)

		for pos in range(self.length):
			if pos in colored:
				self.setpixel(pos, self.colors[abs(self.iters - pos)] if self.fade else self.color)
			else:
				self.setpixel(pos, self.dark_color)

		self.iters += 1 if self.forwards else -1
