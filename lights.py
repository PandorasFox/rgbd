import json
import os
import sys
import threading
import time

def watchdog(old_thread, kill):
    prev = os.stat("config.json")
    while True:
        time.sleep(5)
        curr = os.stat("config.json")
        if (prev.st_mtime != curr.st_mtime or not old_thread.is_alive()):
            print("change detected or old thread died; restarting...")
            kill.set()
            old_thread.join()
            kill.clear()
            lights = threading.Thread(target=lightStart, args=(kill,), daemon=True)
            lights.start()
            old_thread = lights

        prev = curr        

def loadconf():
    with open("config.json") as conf:
        return json.load(conf)

def lightStart(event):
    conf = loadconf()
    # pass conf to the controller
    # pretend busy loop below for lights controlling
    print("\tI started! My ident is " + str(threading.get_ident()))
    while True:
        print("\t\tI'm controlling lights!  " + str(threading.get_ident()))
        time.sleep(5)
        if (event.is_set()):
            sys.exit(0)

def main(debug=False):
    kill = threading.Event()
    lights = threading.Thread(target=lightStart, args=(kill,), daemon=True)
    lights.start()
    watchdog(lights, kill)

if (__name__ == "__main__"):
    main(False)
    sys.exit(0)
