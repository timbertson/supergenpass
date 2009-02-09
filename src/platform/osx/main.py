#!/usr/bin/env python
import os
from commands import getstatusoutput
from keychain import Keychain, KeychainError
from .. import keyinfo
from ..command import require_command


__all__ = ['get_password','save_clipboard','notify','guess_url']

# contract with the main module
# get_password: get the password from the password storage
#    ask the user for it if it cannot be found, or if ask = True
# save_clipboard: save the sepcified data to the clipboard
def get_password():
	try:
		return _store().password()
	except KeychainError:
		print "Couldn't get keychain password"
		raise
	
def save_clipboard(data):
	"""
	Save data to the clipboard, using the pbcopy command-line tool.
	"""
	clipboard = os.popen('pbcopy', 'w')
	clipboard.write(data)
	status = clipboard.close()
	if status is not None:
		raise RuntimeError, "Could not save data to clipboard"
	print "  (password saved to the clipboard)"

def save_password(p):
	"""
	save password to keychain
	"""
	_store().save_password(p)

def notify(domain):
	"""
	Send a system notification that the password has been generated
	"""
	require_command('growlnotify', url='http://growl.info/documentation/growlnotify.php')
	st, output = getstatusoutput("growlnotify -m '%s - password generated' -t 'SuperGenPass'" % domain)
	if st:
		raise RuntimeError, output

def guess_url():
	"""
	Try grabbing the current URL from firefox / safari (whichever is running)
	(this is ugly...)
	For some reason including conditional "tell safari to do blah..." causes safari to open even if that branch
	of code is never even executed. So we're checking which app is open, then doing the conditional logic in python.
	"""
	app_scripts = {
		'firefox': "tell application \"Firefox\" to return (get item 3 of (properties of front window as list))",
		'safari': "tell application \"Safari\" to return (get URL of document 1)",
	}
	
	script = """
		on isRunning(appName)
			tell application "System Events"
				return ((application processes whose (name contains appName)) count) is greater than 0
			end tell
		end isRunning
		"""
	
	for app in app_scripts.keys():
		script += """
		if isRunning("%s") then
			return "%s"
		end if
		""" % (app, app)

	script += "return \"None\""
	# print script
	
	status, output = getstatusoutput("osascript -e '%s'" % script)
	if status != 0 or output == 'None':
		return None
	else:
		app_name = output
		status, output = getstatusoutput("osascript -e '%s'" % app_scripts[app_name])
		if status != 0:
			return None
		# print output
		return output

# implementation details for keychain access

_store_var = None
def _store():
	global _store_var
	if _store_var == None:
		_store_var = PasswordStore()
	return _store_var

def _ask_password():
	from getpass import getpass
	password = getpass("Enter master password: ")
	return password


class PasswordStore():
	def __init__(self, chain='login', account=None, service=None):
		if account is None:
			account = keyinfo.account
		if service is None:
			service = keyinfo.realm
		self.chain = chain
		self.account = account
		self.service = service
		self.keychain = Keychain()

	def unlock(self):
		self.keychain.unlockkeychain(self.chain)
	
	def lock(self):
		self.keychain.lockkeychain(chain)
		
	def password(self, account = None):
		if account is None:
			account = self.account
		_, password = self.keychain.getgenericpassword(self.chain, account, self.service)
		return password

	def save_password(self, password, account = None):
		if account is None:
			account = keyinfo.account
		self.keychain.setgenericpassword(self.chain, account, password, self.service)
