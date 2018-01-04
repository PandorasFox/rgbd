"""
a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9 . ?
.- / -... / -.-. / -.. / . / ..-. / --. / .... / .. / .--- / -.- / .-.. / -- / -. / --- / .--. / --.- / .-. / ... / - / ..- / ...- / .-- / -..- / -.-- / --.. / ----- / .---- / ..--- / ...-- / ....- / ..... / -.... / --... / ---.. / ----. / .-.-.- / ..--..
"""

import animations.common as common

class Anim:
	def __init__(self, zone, config):
		self.zone = zone
		self.length = self.zone.length
		self.conf = config
		self.color = common.from_hex(self.conf.get("color"))
		self.text = self.conf.get("text")
		self.iters = 0
		self.blink_pattern = self.to_morse_blinks()

	def to_morse_blinks(self):
		morse_map = {
			"a": ".-",
			"b": "-...",
			"c": "-.-.",
			"d": "-..",
			"e": ".",
			"f": "..-.",
			"g": "--.",
			"h": "....",
			"i": "..",
			"j": ".---",
			"k": "-.-",
			"l": ".-..",
			"m": "--",
			"n": "-.",
			"o": "---",
			"p": ".--.",
			"q": "--.-",
			"r": ".-.",
			"s": "...",
			"t": "-",
			"u": "..-",
			"v": "...-",
			"w": ".--",
			"x": "-..-",
			"y": "-.--",
			"z": "--..",
			"0": "-----",
			"1": ".----",
			"2": "..---",
			"3": "...--",
			"4": "....-",
			"5": ".....",
			"6": "-....",
			"7": "--...",
			"8": "---..",
			"9": "----.",
			".": ".-.-.-",
			",": "--..--",
			"'": ".----.",
			"?": "..--..",
			"!": "-.-.--",
			"/": "-..-.",
			"(": "-.--.",
			")": "-.--.-",
			"&": ".-...",
			":": "---...",
			";": "-.-.-.",
			"=": "-...-",
			"+": ".-.-.",
			"-": "-....-",
			"\"":".-..-.",
			"$": "...-..-",
			"@": ".--.-.",
			" ": "/"
		}
		# use the morse map to convert text to a morse string
		"""
			* dot: one iteration
			* dash: three iterations
			* time off between dots/dashes: one iteration
			* time off between letters: three iterations
			* time off between words:  seven iterations
		"""
		answer = []
		for letter in self.text:
			morse_str = morse_map.get(letter)
			if (morse_str == "/"):
				answer += ([False] * 7)
			elif (morse_str != None):
				for char in morse_str:
					if (char == "."):
						answer.append(True)
					elif (char == "-"):
						answer += ([True] * 3)
					answer.append(False)
				answer.append(False)
				answer.append(False)
			else:
				continue
		return answer

	def iter(self):
		if (self.blink_pattern[self.iters]):
			col = self.color
		else:
			col = 0
		for i in range(self.length):
			self.zone.setpixel(i, col)
		self.iters = (self.iters + 1) % len(self.blink_pattern)
