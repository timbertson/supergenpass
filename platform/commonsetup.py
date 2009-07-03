#!/usr/bin/env python

import setuptools
import os

common_props = {
	'classifiers': [
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
	],
	'keywords': 'supergenpass password generation hash md5',
	'license': 'GPLv2',
	'url': 'https://launchpad.net/pysgp',
	'package_dir': {'': '.'},
	'include_package_data': True,
}

if __name__ == '__main__':
	for k,v in globals().items():
		if k.startswith('_') or k in ('common_props', 'os','setuptools'):
			continue
		print "%s = %r" % (k,v)
