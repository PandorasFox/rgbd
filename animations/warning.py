import json

from animations.common import from_hex

STATES = {
    'UNKNOWN': from_hex('#778899'),
    'GOOD': from_hex('#00ff00'),
    'WARNING': from_hex('#ffff00'),
    'DANGER': from_hex('#ff0000'),
}


class Anim:
	"""A 'warning' animation. It uses the deliver command to update the state.

	An example data payload would be {"state": "WARNING", "flash": true}
	This would set it to a yellow color and flash on and off at the step_delay time.

	All data should be valid JSON.

	Valid values for state are UNKNOWN, GOOD, WARNING, and DANGER.
	Flash may be true or false."""
	last_was_off = False
	flash = False
	color = STATES['UNKNOWN']

	def __init__(self, length, func, config):
		self.setpixel = func
		self.length = length

		self.update_color(STATES['UNKNOWN'])

	def update_color(self, color):
		for i in range(self.length):
			self.setpixel(i, color)

	def iter(self):
		if not self.flash:
			return

		color = self.color if self.last_was_off else 0

		self.update_color(color)
		self.last_was_off = not self.last_was_off

	def deliver(self, msg):
		update = json.loads(msg)

		if 'flash' in update:
			self.flash = update['flash']

		if 'state' in update and update['state'] in STATES:
			self.color = STATES[update['state']]
			self.update_color(self.color)
