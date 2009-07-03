# SGP Password Generator
# Portions Copyright (C) Chris Zarate
# Portions Copyright (C) 2008-2009 Matt Giuca, Tim Cuthbertson

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

"""
This is the top-level library module for the SGP password generator.
SGP is an algorithm (originally published by Chris Zarate under the name
SuperGenPass) for hashing a password with a domain, to create a unique
password for each site.

Note: This Python version is designed to be portable to other languages (to
serve as a reference implementation).

It's probably a better reference implementation than the original, because
it's commented and a few things are neater or more explicit.

SuperGenPass Password Hashing Algorithm Copyright (C) Chris Zarate
Python port and comments by Matt Giuca and Tim Cuthbertson
Based on JavaScript version from
http://supergenpass.com/mobile/
(Should generate the exact same strings as the original JavaScript version)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2,
as published by the Free Software Foundation.
"""

from main import main
from sgp import sgp
__all__ = ['sgp', 'main']

