""" defines a segment of pixels, from offset to offset+length, for an animation to run on """

class Zone:
    def __init__(self, strip, offset, anim_class, zone_conf):
        self._strip = strip
        self._offset = offset
        self.conf = zone_conf
        self.length = self.conf["length"]
        self.name = self.conf["name"]
        self._anim = anim_class(self, self.conf.get("animation_config"))
        # minimum number of milliseconds to wait before the next iteration
        # -1 = never redraw (i.e. static lighting)
        # 0 = redraw as soon as possible
        # >0 = <x> ms 
        # on my machine, each draw tick takes ~9.7ms, with 240 "pixels"
        self.delay_time = self.conf.get("step_delay")
        if (self.delay_time == None):
            self.delay_time = 0
        # everything is initially drawn
        self.delay_rem = 0
        self.draw = True

    def setpixel(self, i, color):
        if (i < 0 or i > self.length):
            raise Exception("Invalid index for setpixel")
        self._strip.setPixelColor(i + self._offset, color)

    def iter(self):
        self._anim.iter()
