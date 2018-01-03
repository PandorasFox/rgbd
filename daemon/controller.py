#!/usr/bin/env python3

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
		if (self.conf.get("blank_on_exit") == True):
			self.blank_on_exit = True
		else:
			self.blank_on_exit = False

	def loadconf(self, path):
		with open(path) as conf:
			return json.load(conf)

	def run(self):
		if (sys.version_info.major < 3):
			raise Exception("must be running at least python 3")
		if (os.getuid() == 0 or os.getgid() == 0):
			raise Exception("cannot run as root - please use SPI instead of PWM")

		importlib.invalidate_caches()

		if (self.debug):
			self.strip = importlib.import_module("strip").Strip(self.conf, self)
			self.queue = multiprocessing.Queue()

			self.listener_thread = multiprocessing.Process(target=dbus_listener.Listener, args=(self.queue,), daemon=True)
			self.listener_thread.start()

			try:
				print("animating...")
				self.strip.animate(self.queue)
			except Exception:
				pass
			finally:
				# if sent a DBUS 'stop' command, cleanup is triggered twice during debugging.
				# maybe we let it die gracefully,
				# or bind a signal and just os.kill(os.getpid(), signal.SIGTERM) ?
				# since sigterm *should* bypass finally blocks - maybe a bit bad, dunno.
				# it's just extra output during debugging for now =)
				self.cleanup()

		self.context = daemon.DaemonContext(
			working_directory='/tmp/',
			pidfile=lockfile.FileLock('/tmp/rgbd.pid'),
			detach_process=True,
			stdout=open("/tmp/rgbd.stdout", "w+"),
			stderr=open("/tmp/rgbd.stderr", "w+"),
		)

		self.context.signal_map = {
			signal.SIGTERM: self.cleanup,
			signal.SIGINT:  self.cleanup,
			signal.SIGHUP:  'terminate',
		}

		with self.context:
			self.strip = importlib.import_module("strip").Strip(self.conf, self)
			self.queue = multiprocessing.Queue()
			self.listener_thread = multiprocessing.Process(target=dbus_listener.Listener, args=(self.queue,), daemon=True)
			self.listener_thread.start()
			self.strip.animate(self.queue)

	def cleanup(self, signum=None, frame=None):
		# NOTE: possibly allow for exiting without blanking, if we received a restart command
		# maybe a restart --noblank?
		if (self.blank_on_exit):
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
