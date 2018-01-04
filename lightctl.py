#!/usr/bin/env python3

import os
import sys
import argparse
import daemon.controller

class LightCTL:
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		commands = self.parser.add_subparsers(dest="command")

		stop_cmd = commands.add_parser("stop")
		stop_cmd.add_argument("-c", "--config", help="give a new config file for the currently-running daemon to use", default="~/.config/rgbd/config.json")

		start_cmd = commands.add_parser("start")
		start_cmd.add_argument("-c", "--config", help="give a new config file for the currently-running daemon to use", default="~/.config/rgbd/config.json")

		restart_cmd = commands.add_parser("restart")
		restart_cmd.add_argument("-c", "--config", help="give a new config file for the currently-running daemon to use", default="~/.config/rgbd/config.json")

		brightness_cmd = commands.add_parser("set-brightness")
		brightness_cmd.add_argument("brightness_level", type=float, help="set the brightness of the strip to a value from 0 to 255 (Floats between 0 and 1 are also fine)")
		

	def get_args(self):
		self.args = self.parser.parse_args()
		return self.args

	def process_command(self):
		if (self.args.command in ["start", "stop", "restart"]):
			cfg_path = os.path.abspath(os.path.expanduser(self.args.config))
			self.daemon = daemon.controller.RGBd(cfg_path)
			func = getattr(self.daemon, self.args.command)
			func()
			sys.exit(0)
		# other commands involve DBUS.... let's init it.
		
		import dbus, dbus.exceptions
		try:
			bus = dbus.SystemBus()
			self.dbus = bus.get_object("fox.pandora.rgbd", "/fox/pandora/rgbd/lightctl")
		except dbus.exceptions.DBusException as e:
			print("Unable to initialize dbus connection. Please ensure the daemon is running with < command in the future >")
			sys.exit(2)

		if (self.command == "brightness"):
			b = args.brightness_level
			if (0 < b and b < 1):
				b = int(b*255)
			elif (0 <= b and b < 256):
				b = int(b)
			else:
				print("Invalid brightness given!")
				sys.exit(1)
			result = self.dbus.brightness(b)

if (__name__ == "__main__"):
	"""🦊🍑🍆💦😩"""
	lctl = LightCTL()
	lctl.get_args()
	lctl.process_command()
