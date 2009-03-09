#!/usr/bin/env python

from setuptools import *
import commonsetup

setup(
	name='supergenpass-platform',
	version='0.1.3',
	description='platform integration to make supergenpass more useful for end-users',
	author='Tim Cuthbertson',
	packages=commonsetup.platform_packages,
	
	long_description="""Additional OS integration hooks for supergenpass,
	providing functionality for interacting with standard password stores and browsers.
	""",
	package_data={'supergenpass_platform.gnome': ['fresno']},
	zip_safe=False,
	install_requires=[
		'setuptools',
		'mandy',
		'supergenpass',
	],
	scripts=['src/sgp-platform'],
	**commonsetup.common_props
)
