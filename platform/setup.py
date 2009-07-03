#!/usr/bin/env python
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

setup(
	name='supergenpass-platform',
	version='0.1.4',
	description='platform integration to make supergenpass more useful for end-users',
	author="Matt Giuca & Tim Cuthbertson",
	author_email='tim3d.junk+sgp@gmail.com',
	packages=find_packages(exclude=('test*',)),
	
	long_description="""Additional OS integration hooks for supergenpass,
	providing functionality for interacting with standard password stores and browsers.
	""",
	zip_safe=False,
	install_requires=[
		'setuptools',
		'mandy',
		'supergenpass',
	],
	scripts=['sgp-platform'],
	**common_props
)
