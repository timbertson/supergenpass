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

#std
import commands
import sys
from optparse import OptionParser

# library
from supergenpass import domain, sgp

# local
import ui
import persistence

get_pass = 'get_password'
guess_url = 'guess_url'
save_pass = 'save_password'
save_clip = 'save_clipboard'
notify = 'notify'

class Main(object):
	def __init__(self, os_integration_provider):
		self.os_integration = os_integration_provider
		self.run()

	def can_do(self, action):
		return hasattr(self.os_integration, action)
	
	def do(self, action, *args, **kwargs):
		if not self.can_do(action):
			if self.opts.verbose:
				print >> sys.stderr, "Warning: os integration %s doesn't support function %s" % (getattr(self.os_integration, '__name__', '(none)'), action)
			return False
		return getattr(self.os_integration, action)(*args, **kwargs)
	
	def run(self):
		parser = OptionParser("%prog [options] [url_or_domain]")
		parser.add_option('-l', '--length', type='int', default=10, help='length of generated password (%default)')
		parser.add_option('--ask', action='store_true', default=False, help='Ask for the password, skipping system store (default is --no-ask)')
		parser.add_option('--no-ask', dest='ask', action='store_false')
		parser.add_option('--save', action='store_true', default=False, help='Save password (in system store, default is --no-save)')
		parser.add_option('--no-save', dest='save', action='store_false')
		parser.add_option('--notify', action='store_true', default=True, help='Notify on completion (default is --notify)')
		parser.add_option('-q', '--no-notify', dest='notify', action='store_false')
		parser.add_option('-r', '--remember', action='store_true', default=True, help='remember on completion (default is --remember)')
		parser.add_option('--no-remember', dest='remember', action='store_false')
		parser.add_option('--forget', action='store_true', default=False, help='forget this domain from ~/.supergenpass.domains (undo a previous --remember)')
		parser.add_option('--domains', dest='list_domains', action='store_true', default=False, help='list all remembered domains')
		parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='more information')
		parser.add_option('-p', '--print', dest='print_password', action='store_true', default=None, help='just print generated password')

		opts, args =  parser.parse_args()
		self.opts = opts
		if len(args) > 1:
			parser.print_help()
			sys.exit(1)
		else:
			url = args[0] if args else None

		if opts.list_domains:
			print '\n'.join(persistence.get_domains())
			return

		if opts.save:
			opts.ask = True

		if opts.print_password is None and not sys.stdout.isatty():
			if opts.verbose:
				print >> sys.stderr, "sgp: assuming --print since stdout is not a TTY"
			opts.print_password = True

		if not url:
			url = self.do(guess_url)
		if not url:
			url = ui.get_input('Enter domain / URL: ')

		pass_ = None
		if not opts.ask:
			try:
				pass_ = self.do(get_pass)
			except (StandardError): pass
		if not pass_:
			pass_ = ui.get_password('Enter master password: ')

		if opts.save:
			try:
				done = self.do(save_pass, pass_)
				if done is False:
					raise RuntimeError, "not supported by os integration module"
			except (StandardError), e:
				print "Couldn't save password to os store: %s" % (e,)
				raise
		
		domain_ = domain.url_to_domain(url)
		generated_pass = sgp(pass_, domain_, opts.length)
		
		if opts.print_password:
			print generated_pass
		else:
			print >> sys.stderr, "Generated password of length %s for '%s'" % (opts.length, domain_)
			try:
				save_clipboard(generated_pass)
				print >> sys.stderr, "  (password saved to the clipboard)"
			except (StandardError, ImportError):
				print >> sys.stderr, "could not save clipboard. your password is: %s" % (generated_pass)
		if opts.notify:
			self.do(notify, domain_)
		if opts.forget:
			persistence.forget(domain_)
		else:
			if opts.remember:
				persistence.remember(domain_)

def save_clipboard(content):
	from Tkinter import Tk
	r = Tk()
	r.withdraw()
	r.clipboard_clear()
	r.clipboard_append(content)
	r.destroy()

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
