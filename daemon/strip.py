import importlib
import os
import sys
import time
# must have installed rpi_ws281x
import neopixel

""" default animation that just blanks pixels. Fallback. """
class BlankAnim:
	def __init__(self, length, func, custom=None):
		self.length = length
		self.setpixel = func

	def iter(self):
		for i in range(self.length):
			self.setpixel(i, 0)

""" defines a segment of pixels, from offset to offset+length, for an animation to run on """
class Zone:
	def __init__(self, strip, offset, anim_class, zone_conf):
		self.strip = strip
		self.offset = offset
		self.conf = zone_conf
		self.length = self.conf["length"]
		self.name = self.conf["name"]
		self.anim = anim_class(self.length, self.setpixel, self.conf.get("animation_config"))
		self.allow_dbus = self.conf.get("allow_dbus", False)
		# minimum number of milliseconds to wait before the next iteration
		# -1 = never redraw (i.e. static lighting)
		# 0 = redraw as soon as possible
		# >0 = <x> ms
		self.delay_time = self.conf.get("step_delay", 0)
		# everything is initially drawn
		self.delay_rem = 0
		self.draw = True

	def setpixel(self, i, color):
		if (i < 0 or i > (self.length - 1)):
			raise Exception("Invalid index for setpixel")
		self.strip.setPixelColor(i + self.offset, color)

	def iter(self):
		self.anim.iter()

	def deliver(self, msg):
		if (hasattr(self.anim, "deliver")):
			self.anim.deliver(msg)

class Strip:
	def __init__(self, config):
		self.config = config
		self.strip_conf = config["strip_config"]
		self.strip  = self.setup_strip()
		self.blank = BlankAnim
		# attempt to insert the animations dir into our path
		# because I'm not picky, I also try up one level (after the actually given dir)
		anim_path_str = self.config.get("animations_path", "~/.local/share/rgbd/animations")
		self.exp_path = os.path.abspath(os.path.expanduser(anim_path_str))
		self.short_path = "/".join(self.exp_path.split("/")[:-1])
		sys.path.insert(1, self.short_path)
		sys.path.insert(1, self.exp_path)

		importlib.invalidate_caches()
		self.anims_pkg = importlib.import_module("animations")
		self.zones = []
		self.setup_zones()


	def setup_strip(self):
		brightness = self.strip_conf.get("brightness")
		if ( 0 < brightness and brightness < 1):
			brightness = int(brightness * 255)
		strip_type = self.strip_conf.get("strip")
		if (strip_type == "ws281x"):
			strip_type = neopixel.ws.WS2811_STRIP_GRB
		strip = neopixel.Adafruit_NeoPixel(
			self.strip_conf.get("count"),
			self.strip_conf.get("pin"),
			self.strip_conf.get("freq"),
			self.strip_conf.get("DMA"),
			self.strip_conf.get("invert"),
			brightness,
			self.strip_conf.get("channel"),
			strip_type
		)
		strip.begin()
		return strip

	def load_anim_class(self, name):
		# name = name.lower() # maybe I shouldn't do this?
		if (name == "blank"):
			ans = self.blank
		else:
			if (name[0] != "."):
				name = "." + name
			try:
				ans = importlib.import_module(name, "animations").Anim
			except Exception as e:
				sys.stderr.write("Failed to import animation {}: {}\n".format(name, str(e)))
				sys.stderr.write("\tContinuing with Blank anim for this zone...\n")
				ans = self.blank
		return ans

	def setup_zones(self):
		offset = 0
		for z in self.config.get("zones"):
			if (int(z.get("length")) == 0):
				continue
			animName = z.get("animation", "blank")
			anim_cl = self.load_anim_class(animName)
			if (anim_cl == self.blank):
				z["step_delay"] = -1
			self.zones.append(Zone(self.strip, offset, anim_cl, z))
			offset += int(z["length"])
			if (offset > self.strip_conf.get("count")):
				print("Invalid zone info - double check count/zone sizes")
		remaining = self.strip_conf.get("count") - offset
		if (remaining > 0):
			print("{} pixels not part of a zone; creating a blank zone to cover them".format(remaining))
			self.zones.append(Zone(self.strip, offset, self.blank, {
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
				try:
					ret = self.process_msg(queue.get())
					if (ret != None):
						return ret
				except Exception as e:
					sys.stderr.write("unexpected error parsing message: {}\n".format(str(e)))

	def blank_strip(self):
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, 0)
		self.strip.show()

	def process_msg(self, msg):
		print("processing command: {}".format(msg))
		if (msg["command"] == "brightness"):
			# NOTE: maybe a gradual fade? hnn
			self.strip.setBrightness(msg["data"]["value"])
			print("Brightness adjusted to {}".format(msg["data"]["value"]))
		elif (msg["command"] == "setpixel"):
			name = msg["data"]["name"]
			pos = msg["data"]["pos"]
			col = msg["data"]["color"]
			# not gonna bother bounds checking since this is all try/caught
			for z in self.zones:
				if (z.name == name and z.allow_dbus):
					z.setpixel(pos, col)
					self.strip.show()
					print("Pixel color set.")
				elif (z.name == name):
					sys.stderr.write("Not allowed to update pixels in this zone over DBUS\n")
		elif (msg["command"] == "loadconf"):
			return msg["data"]["path"]
		elif (msg["command"] == "deliver"):
			zone_name = msg["data"]["name"]
			for z in self.zones:
				if (z.name == zone_name and z.allow_dbus):
					z.deliver(msg["data"]["info"])
		else:
			sys.stderr.write("Unknown/invalid message: {}\n".format(msg))

	def sleep_til_next(self, time_to_draw):
		# my machine takes 7ms/100 pixels, which is significant enough to take into account
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
