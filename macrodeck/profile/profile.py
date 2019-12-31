from .icon import IconStyle
from .deck import Deck
from .window import Window

class Profile:
	def __init__(self,
			name = 'empty profile', description = 'An empty profile', enabled = False,
			ico_style = IconStyle(), deck = Deck(), windows = [], f_json = None):
		if f_json is not None:
			self.name        = f_json['name'] if 'name' in f_json else name
			self.description = f_json['description'] if 'description' in f_json else description
			self.enabled     = f_json['enable'] if 'enabled' in f_json else enabled
			self.deck        = Deck(f_json=f_json['deck']) if 'deck' in f_json else deck
			self.ico_style   = IconStyle(f_json=f_json['icon_style']) if 'icon_style' in f_json else ico_style
			self.windows     = [ Window(f_json=win) for win in f_json['windows'] ] if 'windows' in f_json else windows
		else:
			self.name        = name
			self.description = description
			self.deck        = deck
			self.ico_style   = ico_style
			self.windows     = windows

	def __str__(self):
		return f'Profile: {self.name}\nIcon Style:\n {self.ico_style}\nDeck:\n{self.deck}\nWindows: {len(self.windows)} \n{self.windows}'

	def __repr__(self):
		return self.__str__()
