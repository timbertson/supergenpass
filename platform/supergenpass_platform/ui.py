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

# cross-platform functions for interacting with the user on the console

import sys
from getpass import getpass

def _input(prompt, fn):
	try:
		print >> sys.stderr, prompt,
		return fn()
	except (EOFError, KeyboardInterrupt):
		print >> sys.stderr
		sys.exit(2)

def get_input(prompt):
	return _input(prompt, raw_input)

def get_password(prompt):
	return _input(prompt, lambda: getpass(''))
