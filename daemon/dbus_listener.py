import dbus, dbus.service, dbus.exceptions, dbus.mainloop.glib
import gi.repository.GLib
import sys
import signal

class Handler(dbus.service.Object):
	def __init__(self, queue, bus_name):
		super().__init__(bus_name, "/fox/pandora/rgbd/lightctl")
		self.queue = queue

	@dbus.service.method("fox.pandora.rgbd.lightctl",
		in_signature="s", out_signature="b")
	def command(self, command):
		print("received command: {}".format(command))
		self.queue.put({"command": str(command)})
		return True
	
	@dbus.service.method("fox.pandora.rgbd.lightctl",
		in_signature="ii", out_signature="b")
	def setpixel(self, pos, color):
		print("received setpixel: {} {}".format(pos, color))
		self.queue.put({
			"command": "setpixel",
			"data": {
				"pos": pos,
				"color": color
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
				"value": input_brightness
			}
		})
		return True

class Listener():
	def __init__(self, queue):
		self.queue = queue
		dbus_loop = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		self.loop = gi.repository.GLib.MainLoop()

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
