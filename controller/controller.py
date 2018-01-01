import json
import sys
import importlib

import os

import daemon
import lockfile
import signal
import multiprocessing

import dbus_listener

# TODO: make this a class too, because why not

def loadconf(path):
	with open(path) as conf:
		return json.load(conf)

def lightStart(strip, queue):
	strip.animate(queue)

def main(path, debug=False):
	if (sys.version_info.major < 3):
		raise Exception("must be running at least python 3")

	importlib.invalidate_caches()
	Strip = importlib.import_module("strip").Strip

	conf = loadconf(path)
	strip = Strip(conf)

	if (debug):
		queue = multiprocessing.Queue()
		lights = multiprocessing.Process(target=lightStart, args=(strip, queue,))
		print("Animating...")
		lights.start()
		strip = None # destroy our copy

	context = daemon.DaemonContext(
		working_directory='/tmp/',
		pidfile=lockfile.FileLock('/tmp/pandoras_box.pid'),
		detach_process=True,
	)

	context.signal_map = {
		signal.SIGTERM: strip.cleanup, # seems to be broken - best to control over lightctl
		signal.SIGHUP:  'terminate',
	}

	with context:
		queue = multiprocessing.Queue()
		lights = multiprocessing.Process(target=lightStart, args=(strip, queue,))
		print("Animating...")
		lights.start()
		strip = None # destroy our copy

	# set up dbus stuff here
	listener = dbus_listener.Listener(queue)
	listener.listen()

if (__name__ == "__main__"):
	"""🦊🍑🍆💦😩"""
	confpath = os.path.abspath("../config/config.json")
	for idx, itm in enumerate(sys.argv):
		if (itm == "--config"):
			confpath = os.path.abspath(sys.argv[idx+1])

	main(confpath, False)
	sys.exit(0)
