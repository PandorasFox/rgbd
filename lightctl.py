#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--brightness", type=float, help="set the brightness of the active strip to a value from 0 to 255. (Floats from 0-1 are also fine)")
parser.add_argument("--stop", action="store_true", help="sends a 'stop' message to the daemon")
parser.add_argument("--start", action="store_true", help="Currently does nothing. Use systemd maybe?")
parser.add_argument("-c", "--config", help="give a new config file for the currently-running daemon to use")
args = parser.parse_args()

# process commands like args.start here
if (args.start):
	if (args.config):
		# load full config path and pass in
		pass
	else:
		# cry
		pass

import dbus, dbus.exceptions
try:
	bus = dbus.SystemBus()
	lightctl = bus.get_object("fox.pandora.rgbd", "/fox/pandora/rgbd/lightctl")
except dbus.exceptions.DBusException as e:
	print("Unable to initialize dbus connection. Please ensure the daemon is running with < command in the future >")
	sys.exit(2)


if (args.brightness):
	b = args.brightness
	if (0 < b and b < 1):
		b = int(b*255)
	elif (0 <= b and b < 256):
		b = int(b)
	else:
		print("Invalid brightness given!")
		sys.exit(1)
	result = lightctl.brightness(b)

if (args.stop):
	result = lightctl.command("stop")


