#!/usr/bin/env python

# SGP Password Generator - Setup
# Copyright (C) 2009 Matt Giuca, Tim Cuthbertson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
		from supergenpass import main
		return main()

if __name__ == '__main__':
	sys.exit(main())