#!/usr/bin/env python3
import sys
from setuptools import setup, find_packages
from glob import iglob

from macrodeck.data import VERSION

if sys.version_info < (3, 6, 0):
	raise SystemExit(f'Error: Tried to install MacroDeck with an unsupported version of Python: {sys.version}\n'
		'Version 3.6 or greater is required')

entries = {'console_scripts': ['macrodeck=macrodeck.macrodeck:main']}

package_data = {
	'macrodeck.assets': list(iglob('macrodeck/assets/**/*', recursive=True))
}


if __name__ == '__main__':
	setup(
		name             = 'macrodeck',
		version          = VERSION,
		packages         = find_packages(),
		package_data     = package_data,
		entry_points     = entries,
		license          = 'BSD',
		setup_requires   = [
			'setuptools_scm',
			'wheel'
		],
		install_requires = [
			'hidapi',
			'pillow',
			'streamdeck',
		],
	)
