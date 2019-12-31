from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper

from macrodeck.macrodeck import get_active_deck, get_active_profile
from .action import Action

class Key:
	def __init__(self, idx,
			name = 'key', text = 'key', icon = 'help', icon_pressed = 'help/outline',
			icon_absolute = False, actions = [], f_json = None):
		self.idx = idx
		self.key_image = None

		if f_json is not None:
			self.name          = f_json['name'] if 'name' in f_json else name
			self.text          = f_json['text'] if 'text' in f_json else self.name
			self.icon          = f_json['icon'] if 'icon' in f_json else icon
			self.icon_pressed  = f_json['icon_pressed'] if 'icon_pressed' in f_json else icon_pressed
			self.icon_absolute = f_json['icon_absolute'] if 'icon_absolute' in f_json else icon_absolute
			self.actions       = [ Action(f_json=act) for act in f_json['actions'] ] if 'actions' in f_json else actions
		else:
			self.name          = name
			self.text          = text
			self.icon          = icon
			self.icon_pressed  = icon_pressed
			self.icon_absolute = icon_absolute
			self.actions       = actions

		self.update_key()


	def render_key(self):
		active_deck = get_active_deck()
		active_profile = get_active_profile()
		if active_deck is not None:
			img = PILHelper.create_image(active_deck)

			ico = Image.open(active_profile.ico_style.get_filename(self.icon)).convert('RGBA')
			ico.thumbnail((img.width, img.height - 20), Image.LANCZOS)
			ico_pos = ((img.width - ico.width) // 2, 0)

			img.paste(ico, ico_pos, ico)

			self.key_image = PILHelper.to_native_format(active_deck, img)

	def update_key(self):
		active_deck = get_active_deck()
		if active_deck is not None and self.key_image is not None:
			active_deck.set_key_image(self.idx, self.key_image)

	def __str__(self):
		return f' Key {self.idx}:\n   Name: {self.name}\n   Text: {self.text}\n   Icon: {self.icon}\n   Icon Pressed: {self.icon_pressed}\n   Actions: {len(self.actions)}\n{self.actions}'

	def __repr__(self):
		return self.__str__()
