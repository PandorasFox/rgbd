# Animations

Animations are done somewhat weirdly. You can glance at the template or other provided animations, but here's the rough documentation:

Each animation must have a class `Anim`, which must provide (at least) an `__init__` function, and an `iter` function.

The `__init__` function takes three arguments:

* `length` - the length of the zone for the animation
* `setpixel(pos, color)` - callback function that sets pixels to a given color.
* `config` - the animation zone config. Can be `None`.

The `iter` function takes no arguments. It is called at each draw tick.

In order for zones to work, regular for loops can't really work. Consider the following:

```
def anim():
	for j in range(100):
		for i in range(240):
			strip.setPixelColor(i, some_predefined_array[(j + i) % size])
		strip.show()
		time.sleep(10/1000)
```

This would probably give you a seizure. But more importantly, it'd be pretty difficult to run this animation, and the animation for another zone at the same time.

Consider this code:

```
def iter(self):
	for i in range(240):
		strip.setPixelColor(i, some_predefined_array[(self.j + i) % size])
	self.j = (self.j + 1) % 100
```

This code achieves essentially the same thing, because we break out one iteration of the `j` loop into its own function, and store the iteration state with the object.

## Other notes

Generally, the longer the delay, the shorter the step in color you want to take for smoother animations.

More of a jump in color => less delay in draw ticks.
