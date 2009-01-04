import eggs
from mandy import Command

class Main(Command):
	def configure(self):
		self.opt('length', int, short='l', default=10, desc="length of generated password")
		self.opt('force', bool, default=False, desc="Ask for the password, skipping system store (default is --no-force)")
		self.opt('save', bool, default=False, desc="Save password (in system store, default is --no-save")
		self.opt('notify', bool, default=True, desc="Notify on completion (default is --notify)")
		self.arg('url', default = None, desc="url / domain you will use the password for")
