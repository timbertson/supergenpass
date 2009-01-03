#!/usr/bin/env python

from supergenpass import sgp
from lib import ui, domain, osx

import lib.eggs
from mandy import Command

def main():
	class Main(Command):
		def configure(self):
			self.opt('length', int, long='length', short='l', default=10, desc="length of generated password")
			self.opt('force', bool, default=False, desc="Force a new password (ignore keychain)")
			self.arg('url', default = None, desc="url / domain you will use the password for")
		
		def run(self, opts):
			url = opts.url
			if url is None:
				url = osx.guess_url()
			if url is None:
				url = ui.get_input('Enter domain / URL: ')
			
			pass_ = None
			if not opts.force:
				try:
					pass_ = osx.get_password()
				except KeychainError: pass
			if pass_ is None:
				pass_ = ui.get_password('Enter master password: ')
	
			domain_ = domain.domain_for_url(url)
			generated_pass = sgp(pass_, domain_, opts.length)
	
			osx.save_clipboard(generated_pass)
			osx.notify(domain_)
	Main()

if __name__ == '__main__':
	main()
