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

from distutils.core import setup
import warnings
import os
import os.path
import shutil
import commonsetup

# XXX package_data appears not to be included in a source distribution

setup(name='supergenpass',
      version='0.1',
      description="MD5-based password generator",
      long_description="Generates a hash of a master password and domain "
        "pair, ensuring high-quality unique passwords for each site.",
      author="Matt Giuca",
      packages=commonsetup.core_packages,
      package_data={'supergenpass': ['domainlist.txt']},
      scripts=['src/sgp'],
      **commonsetup.common_props
     )
