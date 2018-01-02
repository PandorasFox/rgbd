import importlib
import sys
import time
import neopixel

""" default animation that just blanks pixels. Fallback. """
class BlankAnim:
	def __init__(self, zone, conf=None):
		self.zone = zone
		self.length = zone.length

	def iter(self):
		for i in range(self.length):
			self.zone.setpixel(i, 0)

""" defines a segment of pixels, from offset to offset+length, for an animation to run on """
class Zone:
	def __init__(self, strip, offset, anim_class, zone_conf):
		self._strip = strip
		self._offset = offset
		self.conf = zone_conf
		self.length = self.conf["length"]
		self.name = self.conf["name"]
		self._anim = anim_class(self, self.conf.get("animation_config"))
		# minimum number of milliseconds to wait before the next iteration
		# -1 = never redraw (i.e. static lighting)
		# 0 = redraw as soon as possible
		# >0 = <x> ms
		self.delay_time = self.conf.get("step_delay")
		if (self.delay_time == None):
			self.delay_time = 0
		# everything is initially drawn
		self.delay_rem = 0
		self.draw = True

	def setpixel(self, i, color):
		if (i < 0 or i > self.length):
			raise Exception("Invalid index for setpixel")
		self._strip.setPixelColor(i + self._offset, color)

	def iter(self):
		self._anim.iter()

class Strip:
	def __init__(self, config):
		self.config = config
		self.strip  = self.setup_strip()
		self.blank = BlankAnim
		# TODO: get the animations location from config, add to path, then import
		# NOTE: in the interest of security, since this script runs as root, the animation location
		#       should also be like /etc/lightctl/animations/ or something else owned by root
		importlib.invalidate_caches()
		self.anims_pkg = importlib.import_module("animations")
		self.zones = []
		self.setup_zones()


	def setup_strip(self):
		brightness = self.config.get("brightness")
		if ( 0 < brightness and brightness < 1):
			brightness *= 255
		strip_type = self.config.get("strip")
		if (strip_type == "ws281x"):
			strip_type = neopixel.ws.WS2811_STRIP_GRB
		strip = neopixel.Adafruit_NeoPixel(
				self.config.get("count"),
				self.config.get("pin"),
				self.config.get("freq"),
				self.config.get("DMA"),
				self.config.get("invert"),
				brightness,
				self.config.get("channel"),
				strip_type
		)
		strip.begin()
		return strip

	def load_anim_class(self, name):
		# name = name.lower() # maybe I shouldn't do this?
		if (name == None or name == "blank"):
			ans = self.blank
			if (name == None):
				print("No animation name specified - continuing with Blank anim..")
		else:
			if (name[0] != "."):
				name = "." + name
			try:
				ans = importlib.import_module(name, "animations").Anim
			except Exception as e:
				print("Failed to import animation {}: {}".format(name, str(e)))
				print("\tContinuing with Blank anim for this zone...")
				ans = self.blank
		return ans


	def setup_zones(self):
		offset = 0
		for z in self.config.get("zones"):
			if (int(z.get("length")) == 0):
				continue
			animName = z.get("animation")
			anim_cl = self.load_anim_class(animName)
			if (anim_cl == self.blank):
				z["step_delay"] = -1
			self.zones.append(Zone(self.strip, offset, anim_cl, z))
			offset += int(z["length"])
			if (offset > self.config.get("count")):
				print("Invalid zone info - double check count/zone sizes")
		remaining = self.config.get("count") - offset
		if (remaining > 0):
			print("{} pixels not part of a zone; creating a blank zone to cover them".format(remaining))
			zones.append(Zone(self.strip, offset, self.blank, {
				"name": "dummy",
				"length": remaining,
				"step_delay": -1
			}))

	def animate(self, queue):
		first = True
		while True:
			start = time.time()
			for z in self.zones:
				if (z.draw or first):
					z.iter()
					z.draw = False
			self.strip.show()
			end = time.time()
			self.sleep_til_next(end - start)
			first = False
			while (not queue.empty()):
				self.process_msg(queue.get())
	
	def blank_strip(self):
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, 0)
		self.strip.show()

	def process_msg(self, msg):
		# NOTE: maybe break out into a <commands> module, like <animations>?
		if (msg["command"] == "brightness"):
			# TODO: maybe a gradual fade? hnn
			self.strip.setBrightness(msg["data"]["value"])
			print("Brightness adjusted to {}".format(msg["data"]["value"]))
		else:
			print("Unknown/invalid message: {}".format(msg))

	def sleep_til_next(self, time_to_draw):
		# my machine takes ~9.7ms per draw iteration, which is significant enough that it should be taken into account
		# this func is insignificant enough to ignore (also, it'd be a pain to take care of properly)
		# 3 cases:
		# delay_time == -1 : do nothing (drawn once, then z.draw => false
		# delay_time == 0  : set z.draw back to true, stick "0" into the times arr
		# delay_time >  0  : either a) set it to max (just drew it) or b) decrement it, then check if it's <= 0
		times = []
		for zone in self.zones:
			if (zone.delay_time < 0):
				continue
			elif (zone.delay_time == 0):
				times.append(0)
				zone.draw = True
			else:
				if (zone.delay_rem == 0):
					zone.delay_rem = zone.delay_time - (time_to_draw * 1000)
				else:
					zone.delay_rem -= (time_to_draw * 1000)
				if (zone.delay_rem <= 0):
					zone.delay_rem = 0
					zone.draw = True
				times.append(zone.delay_rem)

		if (len(times) != 0):
			sleeptime = min(times)
			if (sleeptime <= 0):
				return
			time.sleep(sleeptime / 1000.0)

			for zone in self.zones:
				if (zone.delay_rem > 0):
					zone.delay_rem -= sleeptime
					if (zone.delay_rem <= 0):
						zone.delay_rem = 0
						zone.draw = True
		else:
			# all animations are currently static
			# however, I might eventually have to change this if I do the "different animations based off wall-clock time" stuff
			print("No animations to animate - exiting, I guess")
			# with it being a daemon, it should wait for a message over dbus
			sys.exit(1)
