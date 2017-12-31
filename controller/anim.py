import importlib
import time
import neopixel

import zone

class Blank:
    def __init__(self, zone):
        self.zone = zone
        self.length = zone.length

    def iter(self):
        for i in range(self.length):
            self.zone.setpixel(i, 0)

def get_anim_class(name):
    # name = name.lower() # maybe I shouldn't do this?
    if (name == None or name == "blank"):
        ans = Blank
        print("No animation name specified - continuing with Blank anim..")
    elif (name[0] != "."):
        name = "." + name
    try:
        ans = importlib.import_module(name, "animations").Anim
    except Exception as e:
        print("Failed to import animation {}: {}".format(name, str(e)))
        print("\tContinuing with Blank anim for this zone...")
        ans = Blank
    return ans

def run_strip(conf):
    brightness = conf.get("brightness")
    if ( 0 < brightness and brightness < 1):
        brightness *= 255
    stype = conf.get("strip")
    if (stype == "ws2812b"):
        stype = neopixel.ws.WS2811_STRIP_GRB
    strip = neopixel.Adafruit_NeoPixel(
            conf.get("count"),
            conf.get("pin"),
            conf.get("freq"),
            conf.get("DMA"),
            conf.get("invert"),
            brightness,
            conf.get("channel"),
            stype
    )
    strip.begin()
    importlib.invalidate_caches()
    anims_pkg = importlib.import_module("animations")
    offset = 0
    zones = []
    for z in conf.get("zones"):
        animName = z.get("animation")
        anim_cl = get_anim_class(animName)
        zones.append(zone.Zone(strip, offset, anim_cl, z))
        offset += z["length"]
        if (offset > conf.get("count")):
            print("Invalid zone info - double check count/zone sizes")
    # TODO: if offset != count - make a filler "blank" zone
    
    i = 0

    # TODO: have two different loops - one for just infinite looping til death, one for a set number of iters
    # because muh efficiency

    while True:
        for z in zones:
            z.iter()
        strip.show()
        # TODO: variable sleep time based on scheduling individual zone updates?
        # :thinking:
        time.sleep(50/1000.0)
        if (conf.get("iters") != None):
            i += 1
            if (i < conf.get("iters")):
                continue
            else:
                return
