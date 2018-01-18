import json

from animations.common import from_hex

_DEFAULT_STATES = {
    'UNKNOWN': from_hex('#778899'),
    'GOOD': from_hex('#00ff00'),
    'WARNING': from_hex('#ffff00'),
    'DANGER': from_hex('#ff0000'),
}


class Anim:
	"""A 'warning' animation. It uses the deliver command to update the state.

	An example data payload would be {"state": "WARNING", "flash": true, "flash_count": 5}
	This would set it to a yellow color and flash on and off at the step_delay time 5 times.

	All data should be valid JSON.

	Default values for state are UNKNOWN, GOOD, WARNING, and DANGER.
	Flash may be true or false.
	Flash count can be any number or not set to flash forever."""
	states = _DEFAULT_STATES

	flash = False
	flash_count = None
	last_was_off = False

	color = states['UNKNOWN']

	def __init__(self, length, func, config):
		self.setpixel = func
		self.length = length

		states = config.get('states', None)
		if states:
			# Allows overwriting without having to worry about a missing UNKNOWN, etc
			self.states.update(self.states.update({k: from_hex(v) for k, v in states.items()}))

		self.update_color(self.states['UNKNOWN'])

	def update_color(self, color):
		for i in range(self.length):
			self.setpixel(i, color)

	def iter(self):
		if not self.flash:
			return

		if self.flash_count == 0:
			self.flash_count = None
			self.flash = False

			return

		color = self.color if self.last_was_off else 0

		self.update_color(color)

		if self.flash_count and self.last_was_off:
			self.flash_count -= 1

		self.last_was_off = not self.last_was_off

	def deliver(self, msg):
		update = json.loads(msg)

		if 'flash' in update:
			self.flash = update['flash']
			self.flash_count = None

		if 'flash_count' in update:
			self.flash_count = update['flash_count']

		if 'state' in update and update['state'] in self.states:
			self.color = self.states[update['state']]
			self.update_color(self.color)
