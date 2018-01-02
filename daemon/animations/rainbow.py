import animations.common as common

"""Draw rainbow that fades across all pixels at once."""
class Anim:
    def __init__(self, zone, custom=None):
        self.zone = zone
        self.iters = 0
        self.length = zone.length
        self.gen_wheel(self.length)
    
    def gen_wheel(self, num):
        self.colors = []
        for i in range(self.length):
            self.colors.append(common.col_wheel(i, self.length))

    def iter(self):
        for pos in range(self.length):
            self.zone.setpixel(pos, self.colors[(pos + self.iters) % self.length])
        self.iters = (self.iters + 1) % self.length
