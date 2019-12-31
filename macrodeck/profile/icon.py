from macrodeck.data import ICON_DIR

class IconStyle:
	def __init__(self, dpi = '48', colour = 'white', ico_type = 'png', f_json = None):
		if f_json is not None:
			self.dpi    = f_json['icon_dpi'] if 'icon_dpi' in f_json else dpi
			self.colour = f_json['icon_colour'] if 'icon_colour' in f_json else colour
			self.type   = f_json['icon_type'] if 'icon_type' in f_json else ico_type
		else:
			self.dpi    = dpi
			self.colour = colour
			self.type   = ico_type

	def get_filename(self, name = 'help/outline'):
		return f'{ICON_DIR}/{name}/{self.colour}/{self.dpi}dp.{self.type}'

	def __str__(self):
		return f'DPI: {self.dpi}, Colour: {self.colour}, Type: {self.type}'

	def __repr__(self):
		return self.__str__()
