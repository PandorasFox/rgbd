import json
import os
import sys
import multiprocessing
import time

import anim

def opt_parse():
    opts = {
        "blank": False        
    }
    for arg in sys.argv:
        if (arg == "blank" or arg == "--blank"):
            opts["blank"] = True
    return opts

def watchdog(old_proc):
    prev = os.stat("../config.json")
    while True:
        time.sleep(1)
        curr = os.stat("../config.json")
        if (prev.st_mtime == curr.st_mtime and not old_proc.is_alive()):
            print("Child process died! Exiting...")
            sys.exit(1)
        elif (prev.st_mtime != curr.st_mtime):
            print("change detected or old thread died; restarting...")
            old_proc.terminate()

            lights = multiprocessing.Process(target=lightStart, daemon=True) # yolo?
            lights.start()

            old_proc = lights
            prev = curr        

def loadconf():
    with open("../config.json") as conf:
        return json.load(conf)

def lightStart(blank=False):
    conf = loadconf()
    if (blank):
        bzone = {
            "name": "blank",
            "animation": "blank",
            "length": conf["count"]
        }
        conf["zones"] = [bzone]
        conf["iters"] = 1
    # pass conf to the controller
    # TODO: importlib here so that as long as controller.py isn't changed, the entire everything can be reloaded
    anim.run_strip(conf)

def main(debug=False):
    if (sys.version_info.major < 3):
        raise Exception("must be running at least python 3")
    opts = opt_parse()
    if (opts["blank"]):
        lightStart(True)
        sys.exit(0)
    lights = multiprocessing.Process(target=lightStart, daemon=True) # yolo?
    lights.start()
    try:
        watchdog(lights)
    except KeyboardInterrupt as e:
        print("\n")
        lights.terminate()
        sys.exit(0)

if (__name__ == "__main__"):
    main(False)
    sys.exit(0)
