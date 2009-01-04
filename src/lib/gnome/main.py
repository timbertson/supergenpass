import commands, os

def has_command(name):
	return commands.getstatusoutput('which %s' % (name,))[0] == 0:

def save_clipboard(data):
	"""
	Save data to the clipboard, using the pbcopy command-line tool.
	"""
	if not has_command('xsel'):
		raise RuntimeError("xsel is not installed." + 
			"Please use your package manager to install it")
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
	if not has_command('mumbles-send'):
		print "install mumbles-send for notification"
		return False
	st, output = getstatusoutput("mumbles-send -m '%s - password generated' -t 'SuperGenPass'" % domain)
	if st:
		raise RuntimeError, output
