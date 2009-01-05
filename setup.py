#!/usr/bin/env python

from setuptools import *

setup(
	name='supergenpass',
	version='0.1.2',
	description='python implementation of the supergenpass.com password generation algorithm',
	author='Tim Cuthbertson',
	author_email='tim3d.junk+sgp@gmail.com',
	url='http://pypi.python.org/pypi/supergenpass/',
	packages=find_packages(exclude=["test"]),
	
	long_description="""\
	supergenpass.com imlpemented in python - with convenient OS integration hooks
	into standard password stores and browsers.
	""",
	classifiers=[
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
	],
	keywords='optparse option parsing command commandline simple',
	license='GPL',
	install_requires=[
		'setuptools',
		'eggloader',
	],
)
