#!/usr/bin/env python

import setuptools
import os
src = os.path.join(os.path.dirname(__file__), '..', 'src')
core_packages = setuptools.find_packages(src, exclude=('supergenpass_platform*',))
platform_packages = setuptools.find_packages(src, exclude=('supergenpass','supergenpass.*'))

common_props = {
	'classifiers': [
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
	],
	'keywords': 'supergenpass password generation hash md5',
	'license': 'GPLv2',
	'url': 'https://launchpad.net/pysgp',
	'package_dir': {'': src},
}

if __name__ == '__main__':
	for k,v in globals().items():
		if k.startswith('_') or k in ('common_props', 'os','setutools'):
			continue
		print "%s = %r" % (k,v)
