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

import user
import os

domain_filename = '.supergenpass.domains'

def remember(domain):
	domains = get_domains()
	if not domain in domains:
		domains.append(domain)
		set_domains(sorted(domains))

def forget(domain):
	domains = get_domains()
	if domain in domains:
		domains.remove(domain)
		set_domains(sorted(domains))
	
## implementation ##

def unique(lst):
	return list(set(lst))

def read_file_lines(filename):
	f = open(filename)
	lines = [line.strip() for line in f.readlines()]
	lines = filter(lambda s: len(s) > 0, lines)
	f.close()
	return unique(lines)

def write_file_lines(filename, lines):
	f = open(filename, 'w')
	f.writelines('\n'.join(lines))
	f.write('\n')
	f.close()

def get_domain_file():
	return os.path.join(user.home, domain_filename)

def get_domains():
	try:
		return read_file_lines(get_domain_file())
	except IOError:
		return []

def set_domains(domains):
	write_file_lines(get_domain_file(), domains)

