#!/usr/bin/env python
"""
attempts to use a platform-specific version of sgp if available.
otherwise, falls back to the bare-bones sgpcore implementation
"""

import sys

_platform = sys.platform
if _platform == 'darwin':
	from lib import osx as platform
	from sgp_osx import main

elif _platform.startswith('linux'):
	from lib import gnome as platform
	from sgp_linux import main
else:
	from sgpcore import main

if __name__ == '__main__':
	main()
