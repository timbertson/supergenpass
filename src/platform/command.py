#std
import commands

# library
from mandy import Command
from supergenpass import domain, sgp

# local
import ui
import persistence

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
		self.opt('ask', bool, default=False, desc="Ask for the password, skipping system store (default is --no-ask)")
		self.opt('save', bool, default=False, desc="Save password (in system store, default is --no-save)")
		self.opt('notify', bool, default=True, desc="Notify on completion (default is --notify)")
		self.opt('remember', bool, short='r', long='remember', default=False, desc="remember this domain in ~/.supergenpass.domains (default is --no-remember)")
		self.opt('forget', bool, default=False, opposite=False, desc="forget this domain from ~/.supergenpass.domains (undo a previous --remember)")
		self.opt('list_domains', bool, default=False, long='domains', opposite=False, desc="list all remembered domains")
		self.arg('url', default = None, desc="url / domain you will use the password for")

	def run(self, opts):
		if opts.list_domains:
			print '\n'.join(persistence.get_domains())
			return

		if opts.save:
			opts.ask = True

		url = opts.url
		if not url:
			url = self.do(guess_url)
		if not url:
			url = ui.get_input('Enter domain / URL: ')
		
		pass_ = None
		if not opts.ask:
			try:
				pass_ = self.do(get_pass)
			except RuntimeError: pass
		if not pass_:
			pass_ = ui.get_password('Enter master password: ')

		if opts.save:
			try:
				done = self.do(save_pass, pass_)
				if done is False:
					raise RuntimeError, "not supported by os integration module"
			except RuntimeError, e:
				print "Couldn't save password to os store: %s" % (e,)
				raise
		
		domain_ = domain.url_to_domain(url)
		generated_pass = sgp(pass_, domain_, opts.length)
		
		print "Generated password of length %s for '%s'" % (opts.length, domain_)
		if self.do(save_clip, generated_pass) is False:
			print "could not save clipboard. your passowrd is: %s" % (generated_pass)
		if opts.notify:
			self.do(notify, domain_)
		if opts.forget:
			persistence.forget(domain_)
		else:
			if opts.remember:
				persistence.remember(domain_)


def has_command(name):
	return commands.getstatusoutput('which %s' % (name,))[0] == 0

def require_command(name, package=None, url=None):
	if not has_command(name):
		help_str = ""
		if package is not None:
			help_str = "Try running: apt-get install %s" % (package,)
		elif url is not None:
			help_str = "To install it, see: %s" % (url)
		raise CommandNotInstalledError(name, help_str)

class CommandNotInstalledError(OSError):
	def __init__(self, name, help):
		self.name = name
		self.help = help
		self.message = "Required command `%s` is not available. %s" % (name, help)
	
	def __str__(self):
		return self.message

