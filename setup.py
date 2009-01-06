#!/usr/bin/env python

from setuptools import *
import commonsetup

name='supergenpass'

setup(
	name=name,
	version='0.1.2',
	description='python implementation of the supergenpass.com password generation algorithm',
	author=commonsetup.author,
	author_email=commonsetup.author_email,
	packages=commonsetup.main_packages,
	
	long_description="""\
	supergenpass.com implemented in python - with convenient OS integration hooks
	into standard password stores and browsers.
	""",
	classifiers=[
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
	],
	keywords='supergenpass password generation hash md5',
	license='GPL',
	install_requires=[
		'setuptools',
		'eggloader',
		'mandy',
		'supergenpass-core',
	],

	entry_points = {
		'console_scripts': [
			'supergenpass = supergenpass.sgp.auto_main',
		],
	},
	
	zip_safe=True,

)
