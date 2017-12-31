class Zone:
    def __init__(self, strip, offset, anim_class, zone_conf):
        self.strip = strip
        self.offset = offset
        self.conf = zone_conf
        self.length = self.conf["length"]
        self.anim = anim_class(self)

    def setpixel(self, i, color):
        self.strip.setPixelColor(i + self.offset, color)

    def iter(self):
        self.anim.iter()
