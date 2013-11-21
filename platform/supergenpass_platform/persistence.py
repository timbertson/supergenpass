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
from __future__ import print_function

import user
import os
from xdg import BaseDirectory

DEPRECATED_FILENAME = '.supergenpass.domains'
domain_filename = DEPRECATED_FILENAME
CONFIG = 'supergenpass'
DOMAINS = 'domains'

def load():
	return DomainHints()

class DomainHints(object):
	def __init__(self):
		old_path = os.path.join(user.home, DEPRECATED_FILENAME)
		if os.path.exists(old_path):
			self.path = old_path
			print("NOTE: "
				"~/" + DEPRECATED_FILENAME + " is deprecated. Please move this file to\n"
				"~/.config/supergenpass/domains to use the new \"hints\" feature\n"
				"(or delete it if you don't care about its contents)\n")
			self._save = self._save_deprecated
			self.dict = self._read_file(self.path)
		else:
			self.path = None
			self.dict = self._read()
		self._loaded_data = self.dict.copy()
	
	def list_domains(self):
		return list(sorted(self.dict.keys()))
	
	def remember(self, domain, hint=None):
		if hint is None and domain in self.dict: return
		if hint is not None:
			print("remembering hint: %s" % (hint,))
		self.dict[domain] = hint or None
	
	def get_hint(self, domain):
		return self.dict.get(domain, None)
	
	def forget(self, domain):
		try:
			del self.dict[domain]
		except KeyError:pass
	
	def _read(self):
		self._save = self._save_xdg
		for d in BaseDirectory.load_config_paths(CONFIG):
			path = os.path.join(d, DOMAINS)
			if os.path.exists(path):
				return self._read_file(path)
		else:
			return {}
	
	def _save_xdg(self):
		if self.path is None:
			self.path = self.default_xdg_path
		new_path = self.path + ".new"
		with open(new_path, 'w') as f:
			for key in sorted(self.dict.keys()):
				pair = (key, self.dict[key])
				print(self._join(pair), file=f)
		os.rename(new_path, self.path)

	def _save_deprecated(self):
		with open(self.path, 'w') as f:
			for dom in self.list_domains():
				print(dom, file=f)
	
	def save(self):
		if self.dict != self._loaded_data:
			print("Saving updated domain info...")
			self._save()
	
	def _read_file(self, path):
		self.path = path
		with open(path) as inputfile:
			return dict(map(self._split, inputfile))
	
	def _split(self, line):
		parts = line.strip().split("#", 1)
		if len(parts) == 1:
			return (parts[0], None)
		return tuple(parts)
	
	def _join(self, pair):
		if pair[1] is None:
			return pair[0]
		return "#".join(pair)

	@property
	def default_xdg_path(self):
		return os.path.join(BaseDirectory.save_config_path(CONFIG), DOMAINS)

