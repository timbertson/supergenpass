#!/usr/bin/env python
"""
attempts to use a platform-specific version of sgp if available.
otherwise, falls back to the bare-bones supergenpass.py implementation
"""

import sys

platform = sys.platform
if platform == 'darwin':
	from sgp_osx import main
elif platform.startswith('linux'):
	from sgp_linux import main
else:
	from sgpcore import main

if __name__ == '__main__':
	main()
