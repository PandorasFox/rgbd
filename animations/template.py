import animations.common as common

"""Animation template
Must have a parent class Anim, that has an __init__ and an iter() function"""

class Anim:
    def __init__(self, zone, config):
        self.zone = zone
        self.length = self.zone.length
        self.conf = config

    def iter(self):
        for i in range(self.length):
            self.zone.setpixel(i, common.rgb(255, 0, 255))
