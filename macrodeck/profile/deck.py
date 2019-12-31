class Deck:
	def __init__(self, brightness = 1.0, serial = '', f_json = None):
		if f_json is not None:
			self.brightness = f_json['brightness'] if 'brightness' in f_json else brightness
			self.serial     = f_json['serial'] if 'serial' in f_json else serial
		else:
			self.brightness = brightness
			self.serial     = serial

	def __str__(self):
		return f' Brightness: {self.brightness}\n'

	def __repr__(self):
		return self.__str__()
