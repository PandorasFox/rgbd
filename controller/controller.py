import json
import os
import sys
import multiprocessing
import time

import anim

def watchdog(old_proc):
    prev = os.stat("../config.json")
    while True:
        time.sleep(1)
        curr = os.stat("../config.json")
        if (prev.st_mtime != curr.st_mtime or not old_proc.is_alive()):
            print("change detected or old thread died; restarting...")
            old_proc.terminate()

            lights = multiprocessing.Process(target=lightStart, daemon=True) # yolo?
            lights.start()

            old_proc = lights
            prev = curr        

def loadconf():
    with open("../config.json") as conf:
        return json.load(conf)

def lightStart():
    conf = loadconf()
    # pass conf to the controller
    anim.run_strip(conf)

def main(debug=False):
    if (sys.version_info.major < 3):
        raise Exception("must be running at least python 3")
    lights = multiprocessing.Process(target=lightStart, daemon=True) # yolo?
    lights.start()
    watchdog(lights)

if (__name__ == "__main__"):
    main(False)
    sys.exit(0)
