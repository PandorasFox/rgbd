import dbus, dbus.service, dbus.exceptions, dbus.mainloop.glib
import gi.repository.GLib
import sys
import signal

class Handler(dbus.service.Object):
	def __init__(self, queue, bus_name):
		super().__init__(bus_name, "/fox/pandora/rgbd/lightctl")
		self.queue = queue

	@dbus.service.method("fox.pandora.rgbd.lightctl",
			in_signature="ss", out_signature="b")
	def deliver(self, zone_name, message):
		print("received deliver command: {} => {}".format(message, zone_name))
		self.queue.put({
			"command": "deliver",
			"data": {
				"name": str(zone_name),
				"info": str(message)
			}
		})
		return True

	@dbus.service.method("fox.pandora.rgbd.lightctl",
		in_signature="sii", out_signature="b")
	def setpixel(self, zone_name, pos, color):
		print("received setpixel: {} {}".format(pos, color))
		self.queue.put({
			"command": "setpixel",
			"data": {
				"name": str(zone_name),
				"pos": int(pos),
				"color": int(color)
			}
		})
		return True

	@dbus.service.method("fox.pandora.rgbd.lightctl",
		in_signature="s", out_signature="b")
	def loadconf(self, confpath):
		print("received conf reload: {}".format(confpath))
		self.queue.put({
			"command": "loadconf",
			"data": {
				"path": str(confpath)
			}
		})
		return True

	@dbus.service.method("fox.pandora.rgbd.lightctl",
		in_signature="y", out_signature="b")
	def brightness(self, input_brightness):
		print("received brightness adjustment: {}".format(input_brightness))
		self.queue.put({
			"command": "brightness",
			"data": {
				"value": int(input_brightness)
			}
		})
		return True

class Listener():
	def __init__(self, queue):
		self.queue = queue
		dbus_loop = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		self.loop = gi.repository.GLib.MainLoop()

		# TODO: give this thread the logfile names and log to "{}.{}".format(std[out,err], getpid())
		# so that we don't clobber the reguar logging

		try:
			self.bus_name = dbus.service.BusName("fox.pandora.rgbd",
				bus=dbus.SessionBus(),
				do_not_queue=True)
		except dbus.exceptions.NameExistsException:
			print("Service is already running")
			sys.exit(1)

		try:
			self.handler = Handler(self.queue, self.bus_name)
			self.loop.run()
		except KeyboardInterrupt:
			pass
		except Exception as e:
			sys.stderr.write("Unexpected exception: {}\n".format(str(e)))
		finally:
			print("exiting dbus loop...")
			self.loop.quit()
