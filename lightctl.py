#!/usr/bin/env python3

import sys


import dbus, dbus.exceptions
try:
	bus = dbus.SystemBus()
	lightctl = bus.get_object("fox.pandora.rgbd", "/fox/pandora/rgbd/lightctl")
except dbus.exceptions.DBusException as e:
	print("Failed to initialize D-Bus object: '%s'" % str(e))
	sys.exit(2)

# TODO: argparse

msg = float(input("brightness val?> "))
if (0 < msg and msg < 1):
	msg =int(255 * msg)
elif (msg < 0 or msg > 255):
	print("Invalid rang for brightness!")
	sys.exit(1)
result = lightctl.brightness(int(msg))
print(result)
