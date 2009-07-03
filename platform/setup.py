#!/usr/bin/env python
import os
from setuptools import *

import commonsetup

setup(
	name='supergenpass-platform',
	version='0.1.4',
	description='platform integration to make supergenpass more useful for end-users',
	author="Matt Giuca & Tim Cuthbertson",
	author_email='tim3d.junk+sgp@gmail.com',
	packages=setuptools.find_packages(exclude=('test*',)),
	
	long_description="""Additional OS integration hooks for supergenpass,
	providing functionality for interacting with standard password stores and browsers.
	""",
	zip_safe=False,
	install_requires=[
		'setuptools',
		'mandy',
		'supergenpass',
	],
	scripts=[os.path.join(commonsetup.src, 'sgp-platform')],
	**commonsetup.common_props
)
