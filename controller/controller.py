import json
import sys
import importlib

import daemon
import lockfile
import signal

import time

def loadconf(path="../config.json"):
    with open(path) as conf:
        return json.load(conf)

def lightStart():
    conf = loadconf()
    # pass conf to the controller
    importlib.invalidate_caches()
    anim = importlib.import_module("anim")
    anim.run_strip(conf)

def main(debug=False):
    if (sys.version_info.major < 3):
        raise Exception("must be running at least python 3")
   
    if (debug):
        lightStart()
    
    importlib.invalidate_caches()
    anim = importlib.import_module("anim")


    context = daemon.DaemonContext(
        working_directory='/home/pandora/pandoras_box/controller/',
        pidfile=lockfile.FileLock('/tmp/pandoras_box.pid'),
        detach_process=True,
    )
    
    context.signal_map = {
            signal.SIGTERM: anim.cleanup,
            signal.SIGHUP:  'terminate',
    }

    with context:
        lightStart()

if (__name__ == "__main__"):
    """🦊🍑🍆💦😩"""
    main(True) # this is true for now, because dbus debugging comes next, and i definitely don't want to be running a daemon until i get the reload stuff working
    sys.exit(0)
