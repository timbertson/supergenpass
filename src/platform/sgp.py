#!/usr/bin/env python
"""
attempts to use a platform-specific version of sgp if available.
otherwise, falls back to the bare-bones sgpcore implementation
"""

import sys
from os import path

def main():
	# if we have a local version of supergenpass, use that:
	if path.isfile(path.join(path.dirname(__file__), '..', 'supergenpass', '__init__.py')):
		sys.path.insert(0, path.join(path.dirname(__file__), '..'))

	_platform = sys.platform

	if _platform == 'darwin':
		import osx as platform

	elif _platform.startswith('linux'):
		import gnome as platform

	else:
		platform = None

	if platform:
		import command
		return command.Main(platform)
	else:
		# fallback to the vanilla sgp:
		from sgp import main
		return main()

if __name__ == '__main__':
	main()
