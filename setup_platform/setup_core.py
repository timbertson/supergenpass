#!/usr/bin/env python

from setuptools import *
import commonsetup

name='supergenpass-core'
setup(
	name=name,
	version='0.1.2',
	description='python implementation of the supergenpass.com password generation algorithm',
	author=commonsetup.author,
	author_email=commonsetup.author_email,
	packages=commonsetup.core_packages,
	
	long_description="""\
	supergenpass.com implemented as a python library
	see the package 'supergenpass' for an executable version with
	OS integration
	""",
	classifiers=[
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
	],
	keywords='supergenpass password generation hash md5',
	license='GPL',
	install_requires=[
		'setuptools',
	],
	zip_safe=True,

)
