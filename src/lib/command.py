#std
import commands

# library
import eggs
from mandy import Command

# local
import ui, domain

get_pass = 'get_password'
guess_url = 'guess_url'
save_pass = 'save_password'
save_clip = 'save_clipboard'
notify = 'notify'

class Main(Command):
	def __init__(self, os_integration_provider):
		self.os_integration = os_integration_provider
		super(self.__class__,self).__init__()

	def can_do(self, action):
		return hasattr(self.os_integration, action)
	
	def do(self, action, *args, **kwargs):
		if not self.can_do(action):
			print "Warning: os integration %s doesn't support function %s" % (self.os_integration.__name__, action)
			return False
		return getattr(self.os_integration, action)(*args, **kwargs)
	
	def configure(self):
		self.opt('length', int, short='l', default=10, desc="length of generated password")
		self.opt('force', bool, default=False, desc="Ask for the password, skipping system store (default is --no-force)")
		self.opt('save', bool, default=False, desc="Save password (in system store, default is --no-save")
		self.opt('notify', bool, default=True, desc="Notify on completion (default is --notify)")
		self.arg('url', default = None, desc="url / domain you will use the password for")

	def run(self, opts):
		if opts.save:
			opts.force = True

		url = opts.url
		if url is None:
			self.do(guess_url)
		if url is None:
			url = ui.get_input('Enter domain / URL: ')
		
		pass_ = None
		if not opts.force:
			try:
				pass_ = self.do(get_pass)
			except KeychainError: pass
		if pass_ is None:
			pass_ = ui.get_password('Enter master password: ')

		if opts.save:
			try:
				done = self.do(save_pass, pass_)
				if done is False:
					raise StandardError, "not supported by os integration module"
			except StandardError, e:
				print "Couldn't save password to os store: %s" % (e,)
				raise
		
		domain_ = domain.domain_for_url(url)
		generated_pass = sgp(pass_, domain_, opts.length)

		if self.do(save_clip, generated_pass) is False:
			print "could not save clipboard. your passowrd is: %s" % (generated_pass)
		if opts.notify:
			self.do(notify, domain_)


def has_command(name):
	return commands.getstatusoutput('which %s' % (name,))[0] == 0

def require_command(name, package=None, url=None):
	if not has_command(name):
		help_str = ""
		if package is not None:
			"Try running: apt-get install %s" % (package,)
		elif url is not None:
			"To install it, see: %s" % (url)
		raise CommandNotInstalledError(name, help=help_str)

class CommandNotInstalledError(OSError):
	def __init__(self, name, help_str):
		self.name = name
		self.help_str = help_str
		self.message = "Required command `%s` is not available. %s" % (name, help_str)
