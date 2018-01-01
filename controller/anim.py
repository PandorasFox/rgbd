import importlib
import time
import neopixel

import zone

class Blank:
    def __init__(self, zone, conf=None):
        self.zone = zone
        self.length = zone.length

    def iter(self):
        for i in range(self.length):
            self.zone.setpixel(i, 0)

def get_anim_class(name):
    # name = name.lower() # maybe I shouldn't do this?
    if (name == None or name == "blank"):
        ans = Blank
        if (name == None):
            print("No animation name specified - continuing with Blank anim..")
    else:
        if (name[0] != "."):
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
    # TODO: metazones, different anims based on wall clock time
    # (i.e. one to fade into sunset, then a constant one after)
    for z in conf.get("zones"):
        animName = z.get("animation")
        anim_cl = get_anim_class(animName)
        zones.append(zone.Zone(strip, offset, anim_cl, z))
        offset += int(z["length"])
        if (offset > conf.get("count")):
            print("Invalid zone info - double check count/zone sizes")
    # TODO: if offset != count - make a filler "blank" zone
   
    if (conf.get("iters") != None):
        run_zones_iter(strip, zones, conf.get("iters"))
    else:
        run_zones_inf(strip, zones)

def run_zones_inf(strip, zones):
    first = True
    while True:
        start = time.time()
        for z in zones:
            if (z.draw or first):
                z.iter()
                z.draw = False
        strip.show()
        end = time.time()
        sleep_til_next(zones, end - start)
        first = False

def run_zones_iter(strip, zones, iters):
    start = time.time()
    for i in range(iters):
        for z in zones:
            z.iter()
        strip.show()
        end = time.time()
    # no sleeping when limited iters

def sleep_til_next(zones, time_to_draw):
    # my machine takes ~9.7ms per draw iteration, which is significant enough that it should be taken into account
    # this func is insignificant enough to ignore (also, it'd be a pain to take care of properly)
    # 3 cases:
    # delay_time == -1 : do nothing (drawn once, then z.draw => false
    # delay_time == 0  : set z.draw back to true, stick "0" into the times arr
    # delay_time >  0  : decrement it, then check if it's <= 0
    times = []
    for zone in zones:
        if (zone.delay_time > 0):
            if (zone.delay_rem == 0):
                zone.delay_rem = zone.delay_time - time_to_draw
            else:
                zone.delay_rem -= (time_to_draw * 1000)
                if (zone.delay_rem <= 0):
                    zone.delay_rem = 0
                    zone.draw = True
        elif (zone.delay_time == 0):
            times.append(0)
            zone.draw = True

    if (len(times) != 0):
        sleeptime = min(times)
        if (sleeptime == 0):
            return
        time.sleep(sleeptime / 1000.0)

        for zone in zones:
            if (zone.delay_rem > 0):
                zone.delay_rem -= sleeptime
    else:
        # all animations are currently static
        # however, I might eventually have to change this if I do the "different animations based off wall-clock time" stuff
        print("No animations to animate - try iterations instead")
        sys.exit(1)
        
