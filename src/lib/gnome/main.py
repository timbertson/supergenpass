import commands, os
from ..command import require_command
from .. import keyinfo
from firefox import guess_url

def save_clipboard(data):
	"""
	Save data to the clipboard, using the xsel command-line tool.
	"""
	require_command('xsel', package='xsel')
	clipboard = os.popen('xsel -i --clipboard', 'w') # take input, place on clipboard
	clipboard.write(data)
	status = clipboard.close()
	if status is not None:
		raise RuntimeError("Could not save data to clipboard")
	print "  (password saved to the clipboard)"

def notify(domain):
	"""
	Send a system notification that the password has been generated
	"""
	require_command('mumbles-send', url='http://www.mumbles-project.org/download/')
	st, output = getstatusoutput("mumbles-send -m '%s - password generated' -t 'SuperGenPass'" % domain)
	if st:
		raise RuntimeError, output

def get_password():
	return _store().get_credentials()[1]
	
def save_password(p):
	_store.set_credentials((keyinfo.account, p))

_key_store = None
def _store():
	global _key_store
	if _key_store is None:
		from keyring import Keyring
		_key_store = Keyring(keyinfo.account, keyinfo.realm, protocol)
	return _key_store
	