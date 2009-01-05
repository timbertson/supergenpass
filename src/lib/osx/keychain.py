#!/usr/bin/env python
# https://launchpad.net/keychain.py/
# -*- coding: utf-8 -*-

# Created by Stuart Colville on 2008-02-02
# Muffin Research Labs. http://muffinresearch.co.uk/

# Modified by Tim Cuthbertson on 2008-11-15
# http://gfxmonk.net
# > Added shell quoting for all shell arguments
# > Added "service" argument to getgenericpassword
# > Added exceptions for failures
# > Made return types consistent and sane

# Copyright (c) 2008, Stuart J Colville
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#			* Redistributions of source code must retain the above copyright
#				notice, this list of conditions and the following disclaimer.
#			* Redistributions in binary form must reproduce the above copyright
#				notice, this list of conditions and the following disclaimer in the
#				documentation and/or other materials provided with the distribution.
#			* Neither the name of the Muffin Research Labs nor the
#				names of its contributors may be used to endorse or promote products
#				derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Stuart J Colville ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Stuart J Colville BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os, sys, commands, re

def shell_quote(arg):
	"""
	Quote one or more shell arguments in single-quotes
	
	>>> shell_quote("it's his!")
	"'it'\\''s his!'"

	>>> print shell_quote("it's his!")
	'it'\''s his!'
	"""
	return "'%s'" % arg.replace("'","'\\''")

def quote_all(*args):
	"""
	returns a tuple of shell-quoted strings, useful for the % format operator
	"""
	return tuple([shell_quote(arg) for arg in args])

class KeychainError(RuntimeError):
	pass

class Keychain:

	DEBUG=False

	def __init__(self):
		"""
		Keychain.py is a simple class allowing access to keychain data and
		settings. Keychain.py can also setup new keychains as required. As the
		keychain is only available on MaxOSX the module will raise ImportError
		if import is attempted on anything other than Mac OSX
		"""

		if sys.platform == 'darwin':
			self.listkeychains()
		else:
			raise ImportError('Keychain is only available on Mac OSX')

	def listkeychains(self):
		""" Returns a dictionary of all of the keychains found on the system """
		k = self.shell("security list-keychains", "Could not get keychain list")
		rx = re.compile(r'".*?/([\w]*)\.keychain"', re.I | re.M)
		self.keychains = {}
		for match in rx.finditer(k):
			self.keychains[match.group(1)]=match.group().strip('"')
		return self.keychains
		
	def shell(self, command, error_reason = "An error occurred"):
		if self.DEBUG:
			print "Running: %s" % command
		result, output = commands.getstatusoutput(command)
		if self.DEBUG:
			print "Result: %s" % result
			print "Output: %s" % output
		if result != 0:
			raise KeychainError, error_reason
		return output

	def checkkeychainname(self, keychain):
		"""
		Rationalises keychain strings as to whether they have .keychain or not
		and looks them up in the dictionary of keychains created at
		instantiation. Returns a string if successful and False if keychain is
		not available
		"""
		start = keychain.find('.keychain')
		keychain = start > -1 and keychain[:start] or keychain
		if keychain in self.keychains:
			return '%s.keychain' % keychain
		else:
			raise KeychainError, "%s.keychain doesn't exist" % (keychain,)

	def getgenericpassword(self, keychain, account, service):
		""" Returns account + password pair from specified keychain item """
		keychain = self.checkkeychainname(keychain)

		data = self.shell(
			"security find-generic-password -g -a %s -s %s %s" % quote_all(account, service, keychain),
			"The specified item could not be found")
		rx1 = re.compile(r'"acct"<blob>="(.*?)"', re.S)
		rx2 = re.compile(r'password: "(.*?)"', re.S)
		account = rx1.search(data)
		password = rx2.search(data)
		if account and password:
			return (account.group(1),password.group(1))
		else:
			raise KeychainError, 'The specified item was missing an account or password'

	def setgenericpassword(self, keychain, account, password, servicename=None):
		""" Create and store a generic account and password in the given keychain """
		keychain = shell_quote(self.checkkeychainname(keychain)) if keychain else ''

		account = '-a %s' % (shell_quote(account),) if account else ''
		password = '-p %s' % (shell_quote(password),) if password else ''
		servicename = '-s %s' % (shell_quote(servicename),) if servicename else ''
		
		self.shell(
			"security add-generic-password %s %s %s %s" % (account, password, servicename, keychain),
			'The specified password could not be added to %s' % keychain)

	def lockkeychain(self, keychain):
		keychain = self.checkkeychainname(keychain)
		self.shell(
			"security lock-keychain %s" % quote_all(keychain),
			'Keychain: %s could not be locked' % (keychain, k))

	def unlockkeychain(self, keychain, password=None):
		keychain = self.checkkeychainname(keychain)
		# if password is None:
		# 	 from getpass import getpass
		# 	 password = getpass('Keychain access password:')
		self.shell("security unlock-keychain %s" % quote_all(keychain))
