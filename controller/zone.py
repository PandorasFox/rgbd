""" defines a segment of pixels, from offset to offset+length, for an animation to run on """

class Zone:
    def __init__(self, strip, offset, anim_class, zone_conf):
        self._strip = strip
        self._offset = offset
        self.conf = zone_conf
        self.length = self.conf["length"]
        self._anim = anim_class(self, self.conf.get("animation_config"))

    def setpixel(self, i, color):
        if (i < 0 or i > self.length):
            raise Exception("Invalid index for setpixel")
        self._strip.setPixelColor(i + self._offset, color)

    def iter(self):
        self._anim.iter()

""" Groups some Zones and treats them each as a single "pixel" """

""" future thoughts: maybe "advancedZone" for zones that have gaps in them that are run off of other zones or something? """

class MetaZone:
    def __init__(self, strip, offset, zone_conf):
        self.strip = strip
        self.offset = offset
        self.conf = zone_conf
        self.zones = []

    def setpixel(self, i, color):
        if (i < 0 or i > len(self.zones)):
            raise Exception("Invalid index for setpixel")
        # needs to set all the pixels in zone[i] to color

    def iter(self):
        self.anim.iter()
