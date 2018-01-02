import json
import sys
import importlib

import os

import daemon
import lockfile
import signal
import multiprocessing

import dbus_listener

class LightsController:
	def __init__(self, confpath, debug):
		self.conf = self.loadconf(confpath)
		self.debug = debug

	def loadconf(self, path):
		with open(path) as conf:
			return json.load(conf)

	def run(self):
		if (sys.version_info.major < 3):
			raise Exception("must be running at least python 3")

		importlib.invalidate_caches()
		Strip = importlib.import_module("strip").Strip

		self.strip = Strip(self.conf)

		if (self.debug):
			self.queue = multiprocessing.Queue()
			self.lights = multiprocessing.Process(target=self.lightStart,)
			print("Animating...")
			self.lights.start()
			self.listener = dbus_listener.Listener(self.queue)
			self.listener.listen()
			sys.exit(0)

		self.context = daemon.DaemonContext(
			working_directory='/tmp/',
			pidfile=lockfile.FileLock('/tmp/rgbd.pid'),
			detach_process=True,
			stdout=open("/tmp/rgbd.stdout", "w+"),
			stderr=open("/tmp/rgbd.stderr", "w+"),
		)

		self.context.signal_map = {
			signal.SIGTERM: self.cleanup,
			signal.SIGHUP:  'terminate',
		}
		
		with self.context:
			self.parent_pid = os.getpid()
			print("daemon context: my pid is {}".format(os.getpid()))
			self.queue = multiprocessing.Queue()
			self.listener_thread = multiprocessing.Process(target=dbus_listener.Listener, args=(self.queue,), daemon=True)
			self.listener_thread.start()
			
			print("Animating...")
			self.strip.animate(self.queue)

	def cleanup(self, signum=None, frame=None):
		self.strip.blank_strip()
		os.kill(self.listener_thread.pid, signal.SIGINT)
		self.listener_thread.join(timeout=0.25)
		
		if (self.listener_thread.is_alive()):
			os.kill(self.listener_thread.pid, signal.SIGKILL)
			print("Had to SIGKILL child - pretty bad; potential orphans")

		sys.exit(0)

if (__name__ == "__main__"):
	"""🦊🍑🍆💦😩"""
	confpath = os.path.abspath("../config/config.json")
	debug = False
	for idx, itm in enumerate(sys.argv):
		if (itm == "--config"):
			confpath = os.path.abspath(sys.argv[idx+1])
		if (itm == "--debug"):
			debug = True
	controller = LightsController(confpath, debug)
	controller.run()
	sys.exit(0)
