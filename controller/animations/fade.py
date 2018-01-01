import animations.common as common
import colour

"""Animation template
Must have a parent class Anim, that has an __init__ and an iter() function"""

class Anim:
    def __init__(self, zone, config):
        self.zone = zone
        self.length = self.zone.length
        self.conf = config
        self.gen_fade()
        # entire zone is one color vs the colors are set down the line
        self.as_whole = (self.conf.get("combine_zone") == True)
        self.iters = 0

    """ generates a color wheel to use for fading """
    def gen_fade(self):
        cols = self.conf.get("colors")
        steps = self.conf.get("steps")
        if (steps == None):
            steps = self.length
        
        colors = []

        for color in cols:
            colors.append(colour.Color(color))
        # to make it loop properly
        colors.append(colors[0])

        wheel = []
        prev = colors[0]
        for color in colors[1:]:
            wheel += list(prev.range_to(color, steps))[:-1] # ignore the last one of each range to prevent overlap
            prev = color
        
        self.wheel = []
        # convert color objects to ints
        for color in wheel:
            self.wheel.append(common.from_colour(color))

    def iter(self):
        if (self.as_whole):
            ind = self.iters
        for i in range(self.length):
            if (not self.as_whole):
                ind = (i + self.iters) % len(self.wheel)
            self.zone.setpixel(i, self.wheel[ind])
        self.iters = (self.iters + 1) % len(self.wheel)

