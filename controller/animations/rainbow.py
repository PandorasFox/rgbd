import animations.common as common

"""Draw rainbow that fades across all pixels at once."""

# note: need to break this out into like
# just init'ing itself
# so then instead we just call <anim>.iter() at each step
# maybe the .iter() can chain-call to .next() or something?

class Anim:
    def __init__(self, zone):
        self.zone = zone
        self.j = 0
        self.length = zone.length

    def iter(self):
        for i in range(self.length):
            self.zone.setpixel(i, common.wheel((i + self.j) & 255))
        self.j += 1
        if (self.j > 256):
            self.j = 0
