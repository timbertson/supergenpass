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

## NOTE: ##
## setup.py is not maintained, and is only provided for convenience.
## please see http://gfxmonk.net/dist/0install/index/ for
## up-to-date installable packages.
import os

from setuptools import *

common_props = {
	'classifiers': [
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
	],
	'keywords': 'supergenpass password generation hash md5',
	'license': 'GPLv2',
	'url': 'https://launchpad.net/pysgp',
	'include_package_data': True,
}

setup(name='supergenpass',
      version='0.1.1',
      description="MD5-based password generator",
      long_description="Generates a hash of a master password and domain "
        "pair, ensuring high-quality unique passwords for each site.",
      author="Matt Giuca & Tim Cuthbertson",
      author_email="tim3d.junk+sgp@gmail.com",
      packages=find_packages(exclude=('test*',)),
      scripts=['sgp'],
      install_requires=['setuptools'],
      zip_safe=True,
      **common_props
     )

