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

import os, sys
from commands import getstatusoutput
from ..command import require_command
from .. import keyinfo
import keyring

def save_clipboard(data):
	"""
	Save data to the clipboard, using the xsel command-line tool.
	"""
	try:
		import gtk
		clipboard = gtk.clipboard_get()
		clipboard.set_text(data)
		clipboard.store()
		print "  (password saved to the clipboard)"
	except StandardError, e:
		print >> sys.stderr, e
		return False

def notify(domain):
	"""
	Send a system notification that the password has been generated
	"""
	import pynotify
	pynotify.init("supergenpass")
	notification = pynotify.Notification("supergenpass",
		"password generated for %s" % (domain,))
	notification.set_hint_double('transient', 1)
	notification.show()

def guess_url():
	return None

def get_password():
	try:
		return _store().get_credentials()[1]
	except keyring.gkey.NoMatchError:
		raise RuntimeError("no password found")
	
def save_password(p):
	try:
		_store().set_credentials((keyinfo.account, p))
	except keyring.gkey.NoMatchError, e:
		raise RuntimeError("couldn't set password: %s" % (e))


_key_store = None
def _store():
	global _key_store
	if _key_store is None:
		_key_store = keyring.Keyring(keyinfo.account, keyinfo.realm, keyinfo.protocol)
	return _key_store
	
