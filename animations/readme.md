# Animations

Animations are done somewhat weirdly. You can glance at the template or other provided animations, but here's the rough documentation:

Each animation must have a class `Anim`, which must provide (at least) an `__init__` function, and an `iter` function.

The `__init__` function takes three arguments:

* `length` - the length of the zone for the animation
* `setpixel(pos, color)` - callback function that sets pixels to a given color.
* `config` - the animation zone config. Can be `None`.
