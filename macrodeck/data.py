from os import path, environ

ASSET_DIR        = path.join(path.dirname(__file__), 'assets')
ICON_DIR         = path.join(ASSET_DIR, 'icons')
PROFILE_DIR      = path.join(ASSET_DIR, 'profiles')

CONFIG_DIR       = path.join(environ['XDG_CONFIG_HOME'] if 'XDG_CONFIG_HOME' in environ else path.join(environ['HOME'], '.config'), 'macrodeck')
USER_PROFILE_DIR = path.join(CONFIG_DIR, 'profiles')
USER_ICON_DIR    = path.join(CONFIG_DIR, 'icons')

VERSION      = '0.1.0'


def mk_user_dirs():
	from pathlib import Path
	if not path.exists(USER_PROFILE_DIR):
		Path(USER_PROFILE_DIR).mkdir(parents=True, exist_ok=True)

	if not path.exists(USER_ICON_DIR):
		Path(USER_ICON_DIR).mkdir(parents=True, exist_ok=True)
