import neopixel

def setpixel(strip, offset, position, color):
    strip.setPixel(offset + position, color)

def confget(conf, key, default):
    val = conf.get("key")
    if (val == None):
        return default
    else:
        return val

# TODO: rewrite using python colour library
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return neopixel.Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return neopixel.Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return neopixel.Color(0, pos * 3, 255 - pos * 3)


