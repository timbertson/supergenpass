#!/usr/bin/env python
import sys
from os import path

def main():
	"""
	attempts to use a platform-specific version of sgp if available.
	otherwise, falls back to the bare-bones supergenpass implementation
	"""
	# if we have a local version of supergenpass, use that:
	if path.isfile(path.join(path.dirname(__file__), '..', 'supergenpass', '__init__.py')):
		sys.path.insert(0, path.join(path.dirname(__file__), '..'))

	_platform = sys.platform

	if _platform == 'darwin':
		import supergenpass_platform.osx as osplatform

	elif _platform.startswith('linux'):
		import supergenpass_platform.gnome as osplatform

	else:
		osplatform = None

	if osplatform:
		import supergenpass_platform.command as command
		return command.Main(osplatform)
	else:
		#TODO: fallback to the vanilla sgp:
		from sgp import main
		return main()

