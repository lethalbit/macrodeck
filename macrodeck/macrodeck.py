#!/usr/bin/env python3
from os import path, getcwd, listdir
from argparse import ArgumentParser

import sys, json

from i3ipc import Connection, Event


from StreamDeck.DeviceManager import DeviceManager

decks = DeviceManager(transport='hidapi').enumerate()
active_profile = None
active_deck = None

def get_active_deck():
	return active_deck

def get_active_profile():
	return active_profile

from .data import *
from .profile.action import Action
from .profile.deck import Deck
from .profile.icon import IconStyle
from .profile.key import Key
from .profile.profile import Profile
from .profile.window import Window



profile_search_dirs = [
	PROFILE_DIR,
	USER_PROFILE_DIR,
]

def peek_profile(profile):
	with open(path.join(profile[0], f'{profile[1]}.json'), 'r') as p:
		jsn = json.load(p)
		if 'name' in jsn and 'description' in jsn and 'enabled' in jsn:
			if jsn['enabled'] == True:
				return (jsn['name'], jsn['description'])
		else:
			return None


def dump_deck_info(deck, idx):
	flip_desc = {
        (False, False): "None",
        (True,  False): "Horizontal",
        (False, True):  "Vertical",
        (True,  True):  "Horizontal and Vertical",
    }
	if deck is not None:
		img_fmt    = deck.key_image_format()
		key_layout = deck.key_layout()

		print(f"""
Deck {idx}:
  Type:     {deck.deck_type()}
  ID:       {deck.id().decode('utf8')}
  Serial:   {deck.get_serial_number()}
  Firmware: {deck.get_firmware_version()}
  Keys:     {deck.key_count()}
    Layout: {key_layout[0]}x{key_layout[1]} grid
    Image:  {img_fmt['size'][0]}x{img_fmt['size'][1]}px
      Format:   {img_fmt['format']}
      Rotation: {img_fmt['rotation']}
      Mirror:   {flip_desc[img_fmt['flip']]}
	""")


def initialize_deck():
	if active_deck is not None:
		active_deck.open()

def main():
	global active_profile
	global active_deck
	global profile_search_dirs

	mk_user_dirs()

	p = ArgumentParser(description='Elgato Stream Deck Macro pad')

	p.add_argument('--additional-profile-dir', type=str, nargs='+', help='An additional directory to search for profiles in')
	p.add_argument('profile', type=str, nargs='?', help='The profile to load, leave blank to list available profiles')
	p.add_argument('--deck', type=str, nargs='?', help='The Elgato Stream Deck to use, set to ? for a list')
	p.add_argument('--deck-info', action='store_true', help='Shows detailed information about the deck specified by --deck')

	args = p.parse_args()

	if args.additional_profile_dir is not None:
		if len(args.additional_profile_dir) > 0:
			macropad.profile_search_dirs += args.additional_profile_dir

	possible_profiles = []
	for ppath in profile_search_dirs:
		possible_profiles += [
			(ppath, path.splitext(pf)[0]) for pf in listdir(ppath) if
				path.isfile(path.join(ppath, pf)) and path.splitext(pf)[-1].lower() == '.json'
		]


	if args.deck_info == True:
		if args.deck is not None:
			if args.deck != '?':
				try:
					deck_index = int(args.deck)
				except:
					deck_index = -255

				if deck_index > len(decks) - 1 or deck_index < len(decks) - 1:
					print(f'Invalid deck number {deck_index}, see --deck ? for a list of connected decks')
					sys.exit(1)
				deck = decks[deck_index]
				deck.open()

				dump_deck_info(deck, deck_index)

				deck.close()
				return 0
			else:
				for idx, deck in enumerate(decks):
					deck.open()

					dump_deck_info(deck, idx)

					deck.close()
				return 0
		else:
			print('Please specify a deck number with --deck')
			return 1

	if args.deck is not None:
		if args.deck == '?':
			print(f'The following {len(decks)} decks were found:')
			for idx, deck in enumerate(decks):
				deck.open()
				deck.reset()

				print(f'\t{idx:>2}: {deck.deck_type()} - {deck.key_count()} key')

				deck.close()

			return 0
		else:
			try:
				deck_index = int(args.deck)
			except:
				deck_index = -255

			if deck_index > len(decks) - 1 or deck_index < len(decks) - 1:
				print(f'Invalid deck number {deck_index}, see --deck ? for a list of connected decks')
				return 1

			active_deck = decks[deck_index]


	if args.profile is None:
		print('The following directories were searched:')
		for pdir in profile_search_dirs:
			print(f'\t{pdir}')

		print('\nThe following profiles were found:')
		for prof in possible_profiles:
			peek = peek_profile(prof)
			if peek is not None:
				print(f'\t{peek[0]:<25} - {peek[1]}')

		print(f'\nTo use a profile, run {sys.argv[0]} <PROFILE_NAME>\nFor more information see {sys.argv[0]} -h')
		return 1
	else:
		pfl = [ pf for pf in possible_profiles if args.profile == pf[1] ]
		if len(pfl) == 0:
			print(f'Unable to find the profile {args.profile} in any of the provides search directories')
			print(possible_profiles)
			return 1

		with open(path.join(pfl[0][0], f'{pfl[0][1]}.json'), 'r') as prf:
			active_profile = Profile(f_json=json.load(prf))

		initialize_deck()

	print(active_profile)

	for ky in active_profile.windows[0].keys:
		ky.render_key()
		ky.update_key()

	if active_deck is not None:
		active_deck.close()


if __name__ == "__main__":
	sys.exit(main())
