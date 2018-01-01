import animations.common as common

class Anim:
    def __init__(self, zone, conf):
        self.zone = zone
        self.conf = conf
        self.length = zone.length
        self.color = common.from_hex(conf.get("color"))

    def iter(self):
        for i in range(self.length):
            self.zone.setpixel(i, self.color)

