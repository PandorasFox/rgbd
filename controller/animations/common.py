import colour

""" returns an int representing an rgb combination; 0-255 each """
def rgb(r, g, b):
    return (r << 16) + (g << 8) + (b)

""" returns an int like above, from a Color object """
def from_colour(col):
    return int(col.hex_l[1:], 16)

""" returns int val from a hex string (must be rrggbb, not rgb) """
def from_hex(col_str):
    if (col_str[0] == "#"):
        col_str = col_str[1:]
    return int(col_str, 16)

""" color wheel stuffs """
def col_wheel(pos, size):
    return from_colour(colour.Color(hsl=(pos/size, 1, 0.5)))
