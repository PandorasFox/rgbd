import json
import sys
import importlib

import os

import daemon
import lockfile
import signal


def loadconf(path):
    with open(path) as conf:
        return json.load(conf)

def lightStart(path):
    conf = loadconf(path)
    # pass conf to the controller
    importlib.invalidate_caches()
    anim = importlib.import_module("anim")
    anim.run_strip(conf)

def main(path, debug=False):
    if (sys.version_info.major < 3):
        raise Exception("must be running at least python 3")
   
    if (debug):
        lightStart(path)
    
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
        lightStart(path)

if (__name__ == "__main__"):
    """🦊🍑🍆💦😩"""
    confpath = os.path.abspath("../config.json")
    for idx, itm in enumerate(sys.argv):
        if (itm == "--config"):
            confpath = os.path.abspath(sys.argv[idx+1])

    main(confpath, True) # this is true for now, because dbus debugging comes next, and i definitely don't want to be running a daemon until i get the reload stuff working
    sys.exit(0)
