# cross-platform functions for interacting with the user on the console

import sys
from getpass import getpass

def _get(func):
	try:
		return func()
	except (EOFError, KeyboardInterrupt):
		print
		sys.exit(2)

def get_input(prompt):
	return _get(lambda: raw_input(prompt))

def get_password(prompt):
	return _get(lambda: getpass(prompt))
