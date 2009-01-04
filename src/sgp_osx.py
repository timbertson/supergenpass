#!/usr/bin/env python

from supergenpass import sgp
from lib import ui, domain, osx, command

def main():
	class Main(command.Main):
		def configure(self):
			# standard options
			super(self.__class__,self).configure()
		
		def run(self, opts):
			if opts.save:
				opts.force = True

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

			if opts.save:
				try:
					osx.save_password(pass_)
				except KeychainError, e:
					print "Couldn't save password to keychain: %s" % (e,)
					raise
			
			domain_ = domain.domain_for_url(url)
			generated_pass = sgp(pass_, domain_, opts.length)
	
			osx.save_clipboard(generated_pass)
			if opts.notify:
				osx.notify(domain_)
	Main()

if __name__ == '__main__':
	main()
